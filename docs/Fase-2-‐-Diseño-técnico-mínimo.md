# Diseño Técnico Mínimo  
**Historia de Usuario: HU-AUTO-001**  
**Título**: Automatización de extracción y procesamiento de datos de productividad desde Google Drive

---

## 1. Objetivo

Desarrollar un sistema automatizado que:

- Se conecte a una carpeta en Google Drive.
- Descargue archivos específicos necesarios para el reporte.
- Valide que los archivos estén presentes y correctamente formateados.
- Procese los datos y genere un archivo `.xlsx` de productividad.
- Genere un log de ejecución y errores.
- Realice todo este flujo sin intervención manual.

---
## 2. Componentes del Sistema

### 2.1. DriveConnector

**Responsabilidad**: Conectarse a Google Drive vía API, identificar y descargar archivos requeridos.  
**Tecnología sugerida**: Python + `google-api-python-client` o `pydrive2`  
**Entradas**: `folder_id`, lista de archivos requeridos  
**Salidas**: Archivos descargados a carpeta local temporal

**Funciones clave**:

- `authenticate()`
- `list_files(folder_id)`
- `download_file(file_id, destination)`

---

### 2.2. FileValidator

**Responsabilidad**: Verificar que los archivos requeridos estén presentes, tengan el formato correcto y las columnas necesarias  
**Entradas**: Rutas locales de los archivos descargados  
**Salidas**: Validación booleana + errores al log

**Funciones clave**:

- `check_presence()`
- `check_format()`
- `check_columns()`

---

### 2.3. DataProcessor

**Responsabilidad**: Leer y combinar los datos desde los archivos descargados  
**Tecnología sugerida**: `pandas`  
**Entradas**: Diccionario `{nombre_archivo: DataFrame}`  
**Salida**: DataFrame consolidado con métricas de productividad

**Funciones clave**:

- `load_data()`
- `transform_data()`
- `calculate_metrics()`

---

### 2.4. ReportGenerator

**Responsabilidad**: Crear el archivo Excel de salida (`reporte_productividad.xlsx`)  
**Entradas**: DataFrame procesado  
**Salidas**: Archivo `.xlsx` en carpeta de salida o Google Drive

**Funciones clave**:

- `generate_xlsx(dataframe)`
- `save_to_drive()` *(opcional)*

---

### 2.5. Logger

**Responsabilidad**: Registrar errores, advertencias y logs de ejecución en `log.txt`  
**Entradas**: Mensajes desde cualquier componente  
**Salida**: `log.txt` en local o Google Drive

---

## 3. Ejecución y Automatización

**Opciones de ejecución automática**:

- Script programado localmente (`cron`, `Task Scheduler`)
- Job en nube (Google Cloud Function, AWS Lambda)

**Configuración**:

- Ejecutar diariamente a una hora fija
- Usar archivo `.env` o `config.json` para credenciales y parámetros

---

## 4. Seguridad

- Autenticación vía OAuth 2.0 o cuenta de servicio
- Uso de variables de entorno para manejar claves
- Nunca almacenar credenciales directamente en el código

---

## 5. Manejo de Errores

**Todos los errores y eventos se registran en `log.txt`**


# Diseño Técnico Mínimo  
**Historia de Usuario: HU-API-001**  
**Título**: Exposición de métricas de productividad mediante API REST

---

## 1. Objetivo

Desarrollar una API RESTful que:

- Exponga datos de productividad por empleado, fecha y categoría.
- Permita integrar los datos con otros sistemas o visualizaciones (dashboards, apps, etc.).
- Aplique buenas prácticas de diseño de API: verbos HTTP, rutas claras, formatos consistentes.
- Garantice seguridad mediante autenticación por token o clave de acceso.

---

## 2. Componentes del Sistema

### 2.1. API REST

**Responsabilidad**: Exponer endpoints que devuelvan métricas de productividad.  
**Formato de salida**: JSON estructurado y documentado.  
**Framework sugerido**: FastAPI, Flask, Django REST (Python) o Express (Node.js).

**Endpoints requeridos**:

| Método | Ruta                              | Descripción                                                      |
|--------|-----------------------------------|------------------------------------------------------------------|
| GET    | `/empleados`                      | Retorna lista de empleados analizados                            |
| GET    | `/empleado/{email}`               | Retorna el resumen de productividad del empleado especificado    |
| GET    | `/metricas`                       | Retorna métricas por filtros: fecha, categoría, empleado         |

**Parámetros comunes**:
- `email`: correo del empleado
- `fecha_inicio`, `fecha_fin`: rango de fechas
- `categoria`: tipo de métrica (chat, reuniones, tareas, etc.)

---

### 2.2. Control de Acceso

**Autenticación**:
- Token de acceso en header HTTP (`Authorization: Bearer <token>`)
- Alternativa: clave API (`x-api-key`)

**Autorización**:
- Validación del token/clave contra lista blanca en base de datos o archivo de configuración

---

### 2.3. Validación de Peticiones

- Validación de parámetros requeridos
- Verificación de formato correcto (email, fecha, etc.)
- Respuestas con códigos HTTP estándar:

| Código | Descripción                        |
|--------|------------------------------------|
| 200    | OK (respuesta exitosa)             |
| 400    | Bad Request (parámetros inválidos) |
| 401    | Unauthorized (sin token válido)    |
| 404    | Not Found (empleado no existe)     |
| 500    | Internal Server Error              |

---

## 3. Diseño del Modelo de Datos (Ejemplo)

```json
{
  "email": "usuario@empresa.com",
  "nombre": "Juan Pérez",
  "productividad": {
    "chat": 142,
    "reuniones": 4,
    "tareas_completadas": 7,
    "autodesk": 3,
    "vpn_conexiones": 5
  },
  "periodo": {
    "inicio": "2025-05-01",
    "fin": "2025-05-28"
  }
}
```

## 4. Seguridad

- **Autenticación**:
  - Usar token en el encabezado HTTP (`Authorization: Bearer <token>`).
- **Protección adicional**:
  - Habilitar CORS con restricciones por dominio.
- **Manejo de credenciales**:
  - Nunca almacenar tokens directamente en el código fuente.
  - Utilizar `.env` o servicios de gestión de secretos (AWS Secrets Manager, Google Secret Manager).

---

## 5. Requisitos Mínimos para el MVP

- Exponer una API REST funcional con los siguientes endpoints:
  - `/empleados` (GET)
  - `/empleado/{email}` (GET)
  - `/metricas` (GET con filtros)
- Validación de parámetros y respuestas:
  - Parámetros requeridos validados antes de ejecutar la lógica.
  - Respuestas en JSON con estructura clara.
- Seguridad:
  - Autenticación básica con token
  - Manejo correcto de códigos de estado HTTP.
- Logging básico:
  - Registro de errores, validaciones fallidas o llamadas mal formadas.

---

## 6. Patrones de Diseño Aplicables

| Componente           | Patrón                     | Propósito                                                                 |
|----------------------|----------------------------|--------------------------------------------------------------------------|
| Controladores        | Controller                 | Separa el manejo de rutas HTTP de la lógica de negocio.                  |
| Servicio de negocio  | Service Layer              | Aísla la lógica de negocio para facilitar mantenimiento y pruebas.       |
| Validación de entrada| Decorator                  | Permite validaciones reutilizables antes del procesamiento principal.    |
| Autenticación        | Strategy                   | Permite implementar diferentes mecanismos de autenticación de forma flexible. |

# Diseño Técnico Mínimo  
**Historia de Usuario: HU-DASH-001**  
**Título**: Dashboard interactivo para monitoreo de productividad por empleado

---

## 1. Objetivo

Desarrollar un dashboard web interactivo que:

- Permita a supervisores visualizar y analizar métricas clave de conectividad por empleado.
- Se alimente dinámicamente desde la API REST definida en la historia HU-API-001.
- Incluya filtrado, visualizaciones dinámicas, alertas visuales y estilo institucional.

---

## 2. Mockup de Referencia

**Mockup tomado como base**:

- Filtros por fecha, división, departamento, categoría y empleado.
- Indicadores numéricos de conectividad general, alto rendimiento, alertas y total de empleados.
- Línea de conectividad por empleado (gráfico de evolución temporal).
- Barra de conectividad por división.
- Tabla de conectividad promedio mensual.
- Alerta visual para empleados con conectividad < 30%.

---
## 3. Componentes del Sistema

### 3.1. Interfaz de Usuario (Frontend)

**Tecnologías sugeridas**:  
- React + Chart.js / Recharts  
- Vue.js + ECharts (alternativa)

**Funciones clave**:

- Filtros dinámicos: Fecha, división, departamento, categoría, empleado.
- Visualizaciones:
  - Línea de conectividad diaria.
  - Barra comparativa por división.
  - Tabla de resumen por empleado.
- Indicadores:
  - Total de empleados.
  - Conectividad promedio.
  - Alertas (< 30%).
  - Alto rendimiento (> 80%).

**Requisitos visuales**:

- Diseño coherente con identidad institucional.
- Responsivo para dispositivos móviles.
- Accesible desde navegadores modernos.

---

### 3.2. Integración con API

**Origen de datos**: API REST implementada en HU-API-001.

**Endpoints consumidos** (ejemplos):

- `GET /empleados`: listado general
- `GET /empleado/{email}`: resumen individual
- `GET /metricas?fecha_inicio=&fecha_fin=&categoria=&email=`: datos filtrados

**Formato esperado**: JSON estructurado con métricas y metadatos.

---

### 3.3. Interactividad

- Actualización automática de visualizaciones al cambiar filtros, sin recargar la página.
- Alerta visual inmediata si hay empleados con baja conectividad.
- Botones para exportar o actualizar el dashboard.
- Visualización clara del histórico mensual de conectividad.

---

## 4. Requisitos Mínimos para el MVP

- Filtros funcionales por división, departamento, categoría, empleado y fecha.
- Gráfica de línea de conectividad diaria por empleado (último mes).
- Tabla de conectividad promedio mensual.
- Alerta visual para empleados con conectividad < 30%.
- Llamadas dinámicas a la API (sin recarga).
- Diseño responsivo y coherente con identidad visual institucional.

---

## 5. Seguridad y Configuración

- La API debe estar protegida mediante token o clave API.
- El dashboard debe enviar el token en los headers.
- Configurar CORS correctamente en el backend.
- Cargar configuraciones (API URL, token) desde archivo `.env` o variables de entorno.

---