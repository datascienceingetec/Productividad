# Documentación del Script de Productividad

## Archivos de Entrada

- **`Productividad_Google.xlsx`**: Archivo principal con datos de productividad diaria.
- **`INFORME_PERSONAL.xlsx`**: Contiene información de los empleados (email y categoría).
- **`chats_source.csv`**: Registros de chats de los empleados.
- **`VPN.csv`**: Datos de conexiones VPN.
- **`Autodesk.xlsx`**: Datos de uso de software Autodesk.
- **`Meetings.xlsx`**: Registro de reuniones.

## Archivos de Configuración

- **`initial_parameters.json`**: Contiene:
  - Lista de correos a excluir (`EMAILS_TO_DELETE`)
  - Año y mes de análisis (`YEAR`, `MONTH`)
  - Coeficientes de productividad para diferentes categorías de empleados

## Estructura de Carpetas Esperada

- La ruta base se pasa como parámetro (por ejemplo: `C:\Productividad\2025-03\`).
- Todos los archivos de entrada deben estar ubicados en esta ruta.

## Formato de Datos Esperado

### `INFORME_PERSONAL.xlsx`

Debe contener al menos las siguientes columnas:

- `Email`: Correo electrónico del empleado
- `Cat`: Categoría del empleado

### `data_cleaned.xlsx`

Se genera a partir de `Productividad_Google.xlsx`. Debe contener hojas nombradas por fecha (formato `YYYY-MM-DD`) que incluyan las siguientes métricas:

- Sent emails
- Email last use
- Edited files
- Viewed files
- Drive last use
- Added files
- Other added files

## Fuentes de Datos por Métrica

| Métrica             | Filename            | Fuente                     |
|---------------------|---------------------|-----------------------------|
| Correo electrónico  | `data_cleaned.xlsx` | Datos de correo electrónico (Drive) |
| Uso de archivos     | `data_cleaned.xlsx` | Actividad en archivos (Drive)      |
| Chats               | `chats_source.csv`  | Registros de chat    (Drive)       |
| Reuniones           | `Meetings.xlsx`     | Calendario y reuniones  (Drive)    |
| Uso de Autodesk     | `Autodesk.xlsx`     | [Actividad en Software](https://manage.autodesk.com/login?t=/reports)|
| Conexiones VPN      | `VPN.csv`           | Accesos remotos vía VPN  (Drive)   |

---
# CI/CD 
## **CI – Integración Continua** (cada vez que se hace push o PR)

#### Automatizaciones críticas:

* **Linting** (formato y estilo del código)
* **Tests unitarios** (deben pasar todos)
* **Build automático** (si aplica: frontend, contenedores, etc.)
* **Validación de seguridad** (por ejemplo: escaneo de dependencias)

#### ¿Cuándo corre?

* En cada `push` y `pull request` a cualquier rama (`dev`, `main`, `feature/*`, etc.)

---

## 2. **Entorno de QA automatizado**

#### Qué debe hacer:

* **Deploy automático a QA** cada vez que se hace merge a `dev`
* URL de QA o entorno accesible para pruebas
* Opcional pero útil: limpieza/reinicialización automática de base de datos para pruebas consistentes

#### Herramientas típicas:

* GitHub Actions / GitLab CI / Jenkins
* Docker + Compose / Kubernetes
* Infra como código (Terraform, Ansible)

---

## 3. **Deploy controlado a Producción**

#### Qué debe cubrir:

* El deploy a `main` debe ser **manual o con aprobación** (según el flujo de confianza)
* Debe estar protegido por:

  * Tests que pasaron
  * Validaciones de PR y revisión
* Ideal: despliegue seguro (blue/green, canary, feature flags)

---

## 🛡️ 4. **Protecciones en el repositorio (branch protections)**

#### Para `main` y `dev`, configura:

* **No permitir push directo** (solo a través de PR)
* **Revisión obligatoria** por al menos 1 revisor
* **Checks automáticos obligatorios** (tests, linters, build)

---

## 5. **Testing mínimo indispensable**

* Tests unitarios (ideal con cobertura automatizada)
* Tests de integración (al menos básicos)
* Opcional (pero recomendado):

  * Tests end-to-end (con Cypress, Playwright, etc.)
  * Validación de performance

---

## Esquema resumido del flujo

```plaintext
Push a feature/* PR
        ↓
✅ CI: Lint + Tests + Build
        ↓
Merge a dev → Deploy automático a QA
        ↓
✅ Pruebas manuales o automáticas
        ↓
Merge a main → Deploy controlado a Producción
        ↓
✅ Monitoreo post-release
```

---

## ¿Qué habilita este flujo?

* Detectar errores **antes** del merge
* Desplegar automáticamente a QA para pruebas funcionales
* Mantener producción estable y protegida
* Construir cultura de colaboración con confianza y responsabilidad

---

# Despliegue

Existen dos repositorios separados:

- `frontend/` – Aplicación web desplegada en Vercel.
- `backend/` – API REST, desplegada en Google Cloud Platform (GCP) mediante contenedores Docker.
## Backend (GCP + Docker)

#### Repositorio: `backend/`

Desplegado a **Cloud Run** en GCP usando contenedores Docker.

* `push` o `merge` a `dev` = Deploy automático a QA (**Ship/Show** según el tipo de cambio).
* `push` o `merge` a `main` = Deploy a producción (**Show/Ask**, según el impacto del cambio).

Workflow CI/CD en `.github/workflows/backend-ci-cd.yml`:

* Linter y tests
* Build y push de la imagen a Artifact Registry
* Deploy automático a Cloud Run

Credenciales de GCP se gestionan a través del secreto `GCP_CREDENTIALS`.

La URL del backend dev y producción se define en variables de entorno para consumo por parte del frontend.

---

## Frontend (Vercel)

#### Repositorio: `frontend/`

Este repositorio está conectado directamente a Vercel.

* `push` a `dev` = Deploy automático al entorno de desarrollo en Vercel (**Ship/Show**).
* `push` a `main` = Deploy a producción (**Show/Ask**).

Variables de entorno (`NEXT_PUBLIC_API_URL`) se configuran en Vercel para apuntar al backend correspondiente.

---

## Entornos

| Rama   | Backend (GCP)                | Frontend (Vercel)             |
| ------ | ---------------------------- | ----------------------------- |
| `dev`   | `https://backend-dev.run.app` | `https://dev.tuapp.vercel.app` |
| `main` | `https://backend.tuapp.com`  | `https://tuapp.vercel.app`    |

---

## Recursos

* [Conventional Commits](https://www.conventionalcommits.org)
* [GitHub Actions Docs](https://docs.github.com/en/actions)
