# Guía de Contribución y Despliegue

Este documento describe las reglas y el flujo de trabajo que se deben seguir para colaborar en este proyecto, que está compuesto por dos repositorios separados:

- `frontend/` – Aplicación web desplegada en Vercel.
- `backend/` – API REST, desplegada en Google Cloud Platform (GCP) mediante contenedores Docker.

## Estructura General

Cada repositorio tiene un entorno de pruebas QA y uno de producción, y sigue una estrategia de ramas basada en:

- `main`: código estable en producción.
- `dev`: código aprobado y desplegado para pruebas funcionales.
- `feature/*`, `bugfix/*`, `hotfix/*`: ramas temporales para trabajo individual, se eliminan después del merge

---

## Creación de Ramas

Todo el trabajo debe realizarse en ramas a partir de `dev`. Las ramas deben seguir el formato:

- `feature/123-descripcion-clara`
- `bugfix/456-ajuste-en-header`
- `hotfix/fix-env-prod-db-url`


Incluye el número de issue o tarea en el nombre si es posible.

---

## Buenas prácticas de commits

### Formato recomendado:

```
<tipo>(<área>): <mensaje corto en presente>
```

### Tipos comunes:

* `feat`: nueva funcionalidad
* `fix`: corrección de bug
* `docs`: cambios en documentación
* `refactor`: mejoras de código sin cambiar comportamiento
* `style`: cambios de estilo (indentación, formato)
* `test`: agregar o modificar tests

### Ejemplos:

* `feat(auth): agregar login con Google`
* `fix(api): corregir error 500 al subir archivo`
* `refactor(ui): separar componente Header`

### Reglas:

* Usa **mensajes descriptivos pero breves**.
* Commits pequeños y frecuentes > uno gigante.
* Usa inglés si el equipo es mixto (opcional).

---

## Pull Requests (PRs)

### Buenas prácticas:

#### Al abrir un PR:

* Usa título claro: `Agrega login con Google (#123)`
* Describe qué hace el PR, cómo probarlo, y si impacta otras partes.
* Añade capturas si es un cambio visual.
* Asigna reviewers.

#### Checklist típico en la descripción:

```markdown
### ¿Qué hace este PR?
- Agrega login con Google a frontend y backend

### ¿Cómo probar?
1. Ejecutar app
2. Ir a /login
3. Ver botón de Google

### ¿Impacta producción?
No, aún está bajo feature flag.
```

#### Al revisar un PR:

* Comenta dudas o mejoras sugeridas.
* No critiques personas, revisa código.
* Usa sugerencias si es algo menor:

  ```suggestion
  Cambiar a `let` ya que se reasigna
  ```

---

## Buenas prácticas adicionales

* Siempre **revisa antes de hacer merge** (`git diff`).
* Usa `git pull --rebase` para mantener historial limpio.
* Nunca hagas `force push` en ramas compartidas sin avisar.
* Elimina ramas remotas después de merge:

  ```bash
  git push origin --delete feature/123-login-con-google
  ```

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

## Flujo de Trabajo básico

1. **Sincroniza `main` y `dev`**:

   ```bash
   git checkout main
   git pull origin main
   git checkout dev
   git pull origin dev
   ```

2. **Crea tu rama desde `dev`**:

   ```bash
   git checkout dev
   git checkout -b feature/123-login-con-google
   ```

3. **Desarrolla y haz commits frecuentes** (ver sección de commits)

4. **Haz push a tu rama**:

   ```bash
   git push origin feature/123-login-con-google
   ```

5. **Abre un Pull Request (PR) hacia `dev` (si aplica)** con título claro y descripción.

6. **Al aprobarse, se hace merge.** QA se prueba, y luego se abre PR de `dev` → `main`.

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

* En general, no se hace `push` directo a `dev` o `main`.
  * **Excepción:** cambios de bajo riesgo clasificados como **Ship** (por ejemplo, ajustes de copy, comentarios, typos) pueden ir directo a `dev`, siempre que pasen CI.
* Toda integración relevante debe pasar por PR y revisión.
* Las ramas deben eliminarse una vez mergeadas.
* Todos los commits deben pasar tests y linter en CI.
* Se recomienda mantener los PRs pequeños, enfocados y clasificados correctamente según *Ship / Show / Ask*.

---

## Recursos

* [Conventional Commits](https://www.conventionalcommits.org)
* [GitHub Actions Docs](https://docs.github.com/en/actions)
* [Vercel Docs](https://vercel.com/docs)
* [Google Cloud Run Docs](https://cloud.google.com/run/docs)


