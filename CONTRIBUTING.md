# Guía de Contribución y Despliegue

Este documento describe las reglas y el flujo de trabajo que se deben seguir para colaborar en este proyecto, que está compuesto por dos repositorios separados:

- `frontend/` – Aplicación web desplegada en Vercel.
- `backend/` – API REST, desplegada en Google Cloud Platform (GCP) mediante contenedores Docker.

## Estructura General

Cada repositorio tiene un entorno de pruebas QA y uno de producción, y sigue una estrategia de ramas basada en:

- `main`: código estable en producción.
- `dev`: código aprobado y desplegado para pruebas funcionales.
- `feature/*`, `bugfix/*`: ramas temporales para trabajo individual.

---

## Flujo de Trabajo por Repositorio

### 1. Creación de Ramas

Todo el trabajo debe realizarse en ramas a partir de `dev`. Las ramas deben seguir el formato:

- `feature/123-descripcion-clara`
- `bugfix/456-ajuste-en-header`


Incluye el número de issue o tarea en el nombre si es posible.

---

### 2. Commits

Usa mensajes de commit claros, consistentes y en tiempo presente. Se recomienda seguir el formato:


`<tipo>(\<módulo>): <mensaje corto>`


Ejemplos:

- `feat(auth): agrega autenticación con Google`
- `fix(api): corrige error en validación de entrada`
- `refactor(ui): mejora estructura del componente Header`

Tipos comunes: `feat`, `fix`, `docs`, `refactor`, `style`, `test`.

---

### 3. Pull Requests (PRs)

#### Apertura de PR

- El código se debe subir a una rama y abrir un PR contra `dev`.
- Asigna al menos un revisor.
- Incluye una descripción clara del cambio, pasos para probarlo, y contexto si aplica.

Ejemplo de plantilla:

### ¿Qué hace este PR?
Implementa el flujo de recuperación de contraseña.

### ¿Cómo probar?
1. Ir a /forgot-password
2. Ingresar un correo válido
3. Confirmar que se envía el correo de recuperación

### ¿Impacta producción?
No. Solo se despliega a QA inicialmente.

#### Revisión

* Todo PR debe ser aprobado por al menos un miembro del equipo.
* Comenta cualquier duda o sugerencia de mejora.
* Usa sugerencias automáticas (`suggestion`) para cambios menores.

---

## Ship / Show / Ask – Estrategia de Toma de Decisiones

Adaptamos el modelo propuesto por Martin Fowler para definir **cómo se toman decisiones técnicas y de despliegue** en el equipo:

### Estilos de decisión:

| Tipo     | Cuándo usarlo                      | Requiere aprobación previa | Comunicación posterior |
| -------- | ---------------------------------- | -------------------------- | ---------------------- |
| **Ship** | Cambios triviales o de bajo riesgo | ❌                          | ❌                      |
| **Show** | Cambios moderados, no críticos     | ❌                          | ✅                      |
| **Ask**  | Cambios de alto impacto o riesgo   | ✅                          | ✅                      |

#### Ejemplos:

* **Ship** → corrección de typo, fix menor de UI, copy, comentarios.
* **Show** → refactor que no cambia funcionalidad, cambio visual visible.
* **Ask** → eliminar funcionalidad, cambios en arquitectura o APIs públicas.

---

## Despliegue

### Backend (GCP + Docker)

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

### Frontend (Vercel)

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

## Ciclo de Release

1. Se finaliza una feature y se mergea a `dev`.
2. Se despliega automáticamente en entorno de pruebas.
3. Se evalúa el cambio: **Ship** si es trivial, **Show** si es funcional.
4. Se notifica si aplica.
5. Para despliegues a producción:

   * Cambios de alto impacto requieren revisión (**Ask**).
   * Otros cambios se pueden avanzar con visibilidad (**Show**).

---

## Reglas Generales

* **En general, no se hace `push` directo a `dev` o `main`.**
  * **Excepción:** cambios de bajo riesgo clasificados como **Ship** (por ejemplo, ajustes de copy, comentarios, typos) pueden ir directo a `dev`, siempre que pasen CI.
* Toda integración relevante debe pasar por PR y revisión.
* Las ramas deben eliminarse una vez mergeadas.
* Todos los commits deben pasar tests y linter en CI.
* Se recomienda mantener los PRs pequeños, enfocados y clasificados correctamente según *Ship / Show / Ask*.

---

## Recomendaciones Técnicas

* Usa `rebase` en lugar de `merge` para mantener historial limpio (`git pull --rebase`).
* Revisa tus cambios antes de hacer PR: `git diff` y `npm run lint`.
* Configura correctamente tus variables de entorno en local y en los entornos remotos.

---

## Recursos

* [Conventional Commits](https://www.conventionalcommits.org)
* [GitHub Actions Docs](https://docs.github.com/en/actions)
* [Vercel Docs](https://vercel.com/docs)
* [Google Cloud Run Docs](https://cloud.google.com/run/docs)


