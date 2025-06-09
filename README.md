# APP Productividad

Este es un proyecto diseñado para calcular y visualizar la productividad de los empleados. Esto se logra mediante:

- **Recopilación de datos de diversas fuentes:** Esto incluye el uso de Autodesk, registros de reuniones, registros de chat, actividad de VPN e interacciones con otros archivos.
- **Ponderación de actividades:** El sistema permite asignar diferentes pesos a distintas actividades, reflejando su importancia relativa en las métricas generales de productividad.
- **Visualización de datos:** Los datos de productividad se presentan a través de un panel de control (dashboard) web fácil de usar, lo que permite un seguimiento y análisis sencillos.

## Frontend

El frontend es un panel de control (dashboard) basado en React responsable de visualizar los datos de productividad procesados. Está construido utilizando `frontend/index.html` y `frontend/dashboard.js`.

Las características clave del dashboard incluyen:

### Gráficos
El dashboard utiliza varios gráficos para representar información sobre la productividad:
- **Productividad a lo Largo del Tiempo (Productivity Over Time):** Un Gráfico de Líneas (Line Chart) que muestra las tendencias de productividad.
- **Distribución de la Productividad (Distribution of Productivity):** Un Gráfico Circular (Pie Chart) que ilustra la dispersión de los niveles de productividad.
- **Productividad Promedio (Average Productivity):** Un Gráfico de Área (Area Chart) que representa la productividad promedio.
- **Desglose de Actividad (Activity Breakdown):** Un Gráfico de Radar (Radar Chart) que desglosa las actividades para un empleado seleccionado.
- **Productividad por Categoría (Productivity by Category):** Un Gráfico de Barras (Bar Chart) que compara la productividad entre diferentes categorías.

### Tablas
Los datos tabulares proporcionan vistas detalladas:
- **Tabla de Promedio Mensual (Monthly Average Table):** Muestra la productividad promedio mensualmente.
- **Tabla de Empleados con Baja Conectividad (Low Connectivity Employees Table):** Lista los empleados que experimentan baja conectividad, lo que podría afectar la productividad.

### Filtros
Para refinar los datos mostrados, el dashboard ofrece varios filtros:
- División
- Departamento
- Categoría
- Empleado
- Rango de Fechas

### Tecnologías
El frontend está construido con un stack moderno de JavaScript:
- **React:** Para construir los componentes de la interfaz de usuario.
- **Recharts:** Una biblioteca de gráficos componible utilizada para renderizar los diversos gráficos.
- **TailwindCSS:** Un framework CSS "utility-first" para estilizar la aplicación.
- **Lodash:** Una biblioteca de utilidades de JavaScript que proporciona funciones útiles.
- **D3.js:** Una potente biblioteca para la visualización de datos, probablemente utilizada junto con Recharts o para visualizaciones personalizadas.

## Backend y Procesamiento de Datos

El backend es responsable de recopilar, limpiar y procesar datos de diversas fuentes para calcular las métricas de productividad de los empleados. La lógica central reside en scripts de Python ubicados en el directorio `scripts/`.

### Scripts Clave y Flujo de Trabajo

1.  **`scripts/main.py`**: Este script orquesta todo el pipeline de procesamiento de datos.
    *   Se presume que primero llama a `scripts/clean_main_file.py` (aunque su contenido específico no se detalla aquí, su nombre sugiere un rol en el preprocesamiento o limpieza de un conjunto de datos inicial).
    *   Después del preprocesamiento, ejecuta `scripts/calculate_productivity.py` para realizar los cálculos centrales de productividad.

2.  **`scripts/calculate_productivity.py`**: Este es el script central para calcular la productividad.
    *   **Funcionalidad**: Calcula las puntuaciones de productividad diarias y mensuales agregadas para los empleados.
    *   **Entradas (Inputs)**:
        *   Datos de Excel limpios (probablemente `data_cleaned.xlsx`, un resultado de `scripts/clean_main_file.py`).
        *   Datos de uso de Autodesk (`Autodesk.xlsx`).
        *   Datos de reuniones (`Meetings.xlsx`).
        *   Datos de chat (`chats_source.csv`).
        *   Datos de conexión VPN (`VPN.csv`).
        *   Información de empleados (`INFORME_PERSONAL.xlsx`), que incluye detalles como la categoría del empleado.
    *   **Ponderación de Actividades**: El script utiliza coeficientes definidos en `scripts/initial_parameters.json` para ponderar diferentes actividades (por ejemplo, uso de Autodesk, participación en reuniones) según la categoría del empleado (por ejemplo, modeladores, cat12345, otros). Esto permite un cálculo matizado de la productividad que refleja la importancia variable de las tareas en los diferentes roles.
    *   **Salidas (Outputs)**:
        *   `productivity_by_day.xlsx`: Contiene puntuaciones de productividad diarias para cada empleado.
        *   `final_table_with_results.xlsx`: Presenta resultados mensuales agregados de productividad, adecuados para la revisión final y visualización.

3.  **`scripts/initial_parameters.json`**: Este archivo JSON es crucial para configurar el procesamiento de datos y el cálculo de la productividad.
    *   **`EMAILS_TO_DELETE`**: Una lista de direcciones de correo electrónico que se excluirán del procesamiento.
    *   **`YEAR`**, **`MONTH`**: Definen el período específico para el cual se calcula la productividad. Esto permite un análisis específico de diferentes marcos de tiempo.
    *   **`COEFFICIENTS`**: Contiene los factores de ponderación para diferentes actividades (por ejemplo, `AUTODESK_TIME_COEFFICIENT`, `MEETINGS_COEFFICIENT`, `CHATS_COEFFICIENT`) y cómo se aplican a diversas categorías de empleados. Esto es fundamental para adaptar la métrica de productividad a la naturaleza específica del trabajo dentro de la organización.

El pipeline de procesamiento de datos está diseñado para transformar datos brutos de actividad en información de productividad accionable, con parámetros configurables que aseguran flexibilidad en la lógica de cálculo.

## Cómo Ejecutar el Proyecto

Esta sección proporciona instrucciones sobre cómo configurar y ejecutar el proyecto IngetecProductivity.

### 1. Prerrequisitos

*   **Python:** Asegúrese de tener Python 3.x instalado.
*   **Bibliotecas de Python:** Instale las bibliotecas de Python necesarias usando pip:
    ```bash
    pip install pandas xlsxwriter
    ```
*   **Archivos de Datos de Entrada:**
    *   Todos los archivos de Excel (`.xlsx`) y CSV (`.csv`) de entrada detallados en la sección "Backend y Procesamiento de Datos" (por ejemplo, `Autodesk.xlsx`, `Meetings.xlsx`, `chats_source.csv`, `VPN.csv`, `INFORME_PERSONAL.xlsx`, y el archivo de datos inicial limpiado) deben estar disponibles en la carpeta de Drive configurada.
    *   Durante la ejecución estos archivos se descargarán automáticamente a una carpeta temporal antes de ser procesados.

### 2. Procesamiento de Datos (Backend)

1.  **Configurar Parámetros:**
    *   Abra `scripts/initial_parameters.json`.
    *   Establezca las variables `YEAR` y `MONTH` para que coincidan con el período de los datos que desea procesar.
    *   Actualice `EMAILS_TO_DELETE` con cualquier dirección de correo electrónico que deba excluirse del análisis.
    *   Verifique y ajuste las rutas de archivo para todas las fuentes de datos de entrada si difieren de los valores predeterminados.
    *   Revise y modifique los `COEFFICIENTS` para la ponderación de actividades si es necesario, para alinearlos con las métricas de productividad de su organización.

2.  **Ejecutar el Script Principal:**
    *   Navegue al directorio raíz del proyecto en su terminal.
    *   Ejecute el script de procesamiento principal:
        ```bash
        python scripts/main.py
        ```
    *   Este script realizará la limpieza de datos (implícitamente a través de `scripts/clean_main_file.py`) y luego calculará la productividad (a través de `scripts/calculate_productivity.py`).

3.  **Revisar Salidas:**
    *   Tras una ejecución exitosa, el script generará archivos de salida en la carpeta temporal utilizada durante el proceso.
    *   Los archivos de salida clave incluyen:
        *   `productivity_by_day.xlsx`: Puntuaciones de productividad diarias.
        *   `final_table_with_results.xlsx`: Resultados de productividad mensuales agregados.

### 3. Visualización del Dashboard (Frontend)

*   **Estado Actual (Datos de Prueba - Mock Data):** El dashboard del frontend (`frontend/index.html` y `frontend/dashboard.js`) está actualmente configurado para usar datos de prueba (mock data) para fines de demostración.
    *   Para verlo, simplemente abra `frontend/index.html` directamente en un navegador web.

*   **Visualización de Datos Reales (Mejora Futura):**
    *   Para conectar el dashboard a los datos reales generados por el backend de Python, se requerirían modificaciones en `frontend/dashboard.js`.
    *   Esto implicaría:
        *   Obtener los datos de los archivos Excel de salida (por ejemplo, convirtiéndolos a un formato JSON que el frontend pueda consumir).
        *   Alternativamente, desarrollar una API de backend simple (quizás usando Flask o FastAPI, potencialmente aprovechando el placeholder `app/main.py`) para servir los datos de productividad al frontend.
    *   Este paso de integración aún no está implementado en la versión actual.

## Estructura del Proyecto

El repositorio está organizado en varios directorios clave:

-   **`app/`**: Este directorio está destinado a una aplicación API de backend.
    -   `main.py`: Archivo principal de la aplicación (actualmente un placeholder).
    -   `api/v1/endpoints.py`: Definiciones de los endpoints de la API (actualmente un placeholder).
-   **`frontend/`**: Contiene todos los archivos relacionados con el dashboard frontend basado en React.
    -   `index.html`: El archivo HTML principal para el dashboard.
    -   `dashboard.js`: El archivo JavaScript central que contiene la aplicación React y la lógica de los gráficos.
    -   `styles.css`: Estilos CSS para el dashboard.
-   **`scripts/`**: Alberga los scripts de Python responsables del procesamiento de datos y los cálculos de productividad.
    -   `main.py`: Orquesta el flujo de trabajo de limpieza de datos y cálculo.
    -   `calculate_productivity.py`: Realiza los cálculos centrales de productividad basados en diversas entradas y pesos configurados.
    -   `clean_main_file.py`: (Asumido) Maneja el preprocesamiento y la limpieza de los datos iniciales.
    -   `initial_parameters.json`: Archivo de configuración para los scripts del backend, que define el período de procesamiento, las rutas de los archivos y los coeficientes de ponderación de actividades.
-   **`.github/`**: Contiene configuraciones específicas de GitHub.
    -   `settings.yml`: Configuraciones a nivel de repositorio para GitHub.
    -   `workflows/`: Define los pipelines de CI/CD.
        -   `lint.yml`: Flujo de trabajo para el linting de código.
        -   `test.yml`: Flujo de trabajo para ejecutar pruebas automatizadas.
-   **`CONTRIBUTING.md`**: Proporciona directrices detalladas para contribuir al proyecto, incluyendo la estrategia de ramas, convenciones para los mensajes de commit y procesos de Pull Request.
-   **`README.md`**: Este archivo – proporcionando una visión general y documentación para el proyecto.

## Contribuciones

Para obtener información detallada sobre cómo contribuir, por favor consulte el archivo `CONTRIBUTING.md`. Este documento incluye directrices sobre:

-   Estrategia de creación de ramas (Branching strategy)
-   Convenciones para los mensajes de commit (Commit message conventions)
-   Proceso de Pull Request (PR)
-   Estándares de codificación (Coding standards)
-   Flujo de trabajo general de desarrollo (General development workflow)

Adherirse a estas directrices ayudará a asegurar un proceso de colaboración fluido y efectivo.
