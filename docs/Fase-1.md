# Historias de Usuario

## Automatización
**Gaps Detectados:** Sin extracción automática de datos. Proceso manual de generación de informes

### Historia de Usuario - Automatización de Procesamiento

**ID**: HU-AUTO-001  
**Título**: Automatización de extracción y procesamiento de datos de productividad

**Como** gerente,  
**quiero** que el sistema extraiga y procese automáticamente los archivos de entrada desde una ruta predefinida,  
**para** generar los informes de productividad sin intervención manual y de forma recurrente.

---

### Criterios de Aceptación

- [ ] El sistema debe escanear automáticamente una carpeta en drive configurada para detectar archivos nuevos o actualizados.
- [ ] El sistema debe generar un archivo de reporte (`.xlsx`) con métricas de productividad por empleado, en la ruta de salida definida.
- [ ] En caso de errores (archivos faltantes, formatos inválidos, columnas incorrectas), el sistema debe registrar logs detallados en un archivo (`log.txt`) dentro de la misma ruta base.
- [ ] El sistema debe validar que el archivo necesario (`data_cleaned.xlsx`) esté presentes antes de procesar.
- [ ] El sistema debe validar que el archivo necesario (`chat_source.csv`) esté presentes antes de procesar.
- [ ] El sistema debe validar que el archivo necesario (`Meetings.xlsx`) esté presentes antes de procesar.
- [ ] El sistema debe validar que el archivo necesario (`Autodesk.xlsx`) esté presentes antes de procesar.
- [ ] El sistema debe validar que el archivo necesario (`VPN.csv`) esté presentes antes de procesar.

---

### Notas Técnicas

- Lenguaje: Python 3.x  
- Requiere módulos: `pandas`, `openpyxl`, `os`, `logging`, `schedule` (o similar para programación)  
- Estructura de carpetas y nombres de archivos deben mantenerse según documentación actual  
- Debe permitir configuración externa vía `initial_parameters.json`

---

## API REST

**Gaps Detectados**: Falta de acceso programático a los datos. Limitaciones para integrar con otras herramientas o plataformas.


### Historia de Usuario - Exposición de Datos vía API

**ID**: HU-API-001  
**Título**: Exposición de métricas de productividad mediante API REST

**Como** desarrollador de sistemas,    
**quiero** que el sistema exponga los datos de productividad a través de una API REST segura y estructurada,    
**para** poder integrarlos fácilmente con dashboards, aplicaciones móviles u otros sistemas corporativos.

---

### Criterios de Aceptación

* [ ] La API debe permitir consultar métricas de productividad por empleado, fecha y categoría.
* [ ] La API debe seguir estándares REST (uso de verbos HTTP, rutas claras y uso de códigos de estado).
* [ ] La API debe devolver los datos en formato JSON con estructura documentada.
* [ ] Debe existir un endpoint para obtener un listado de todos los empleados analizados.
* [ ] Debe existir un endpoint para obtener el resumen de productividad de un empleado específico dado su correo electrónico.
* [ ] La API debe contar con autenticación (por ejemplo, token o clave API) para limitar el acceso no autorizado.
* [ ] En caso de error (parámetros faltantes o inválidos), debe retornar mensajes claros y estandarizados.
* [ ] La documentación de los endpoints debe estar accesible (por ejemplo, usando Swagger o archivo `.md`).

---

### Notas Técnicas

* Lenguaje: Python 3.x
* Framework recomendado: `Flask` o `FastAPI`
* Formato de respuesta: JSON
* Requiere acceso a la base de datos o estructura de archivos generados (.xlsx)
* Debe incluir configuración para puerto y seguridad en `initial_parameters.json`
* La autenticación puede usar API Key definida en parámetros de configuración

---

## Dashboard Interactivo

**Gaps Detectados**: Visualización poco accesible, análisis limitado a archivos estáticos, sin capacidad de filtrado dinámico ni actualización en tiempo real.


### Historia de Usuario - Visualización de Productividad en Dashboard

**ID**: HU-DASH-001 
**Título**: Dashboard interactivo para monitoreo de productividad por empleado

**Como** supervisor de equipo,  
**quiero** acceder a un dashboard web interactivo conectado a la API de productividad,  
**para** visualizar métricas clave de conectividad, identificar patrones y tomar decisiones de manera oportuna.

---

### Criterios de Aceptación

* [ ] El dashboard debe permitir filtrar la información por división, departamento, categoría y empleado.
* [ ] Debe mostrar una gráfica de línea con la conectividad diaria por empleado para un mes seleccionado.
* [ ] Debe incluir una tabla con el promedio mensual de conectividad por empleado.
* [ ] Debe resaltar o listar los empleados con conectividad mensual inferior al 30%.
* [ ] La información debe obtenerse dinámicamente desde la API REST definida en la historia HU-API-001.
* [ ] El dashboard debe actualizar la visualización al cambiar cualquier filtro sin necesidad de recargar la página.
* [ ] Debe ser responsivo y accesible desde navegadores modernos (y adaptable a dispositivos móviles).
* [ ] El diseño visual debe mantener un estilo coherente con la identidad institucional.

---

### Mockup / Referencia Visual

Se adjunta a continuación una vista preliminar (versión beta) del dashboard interactivo propuesto:

[Mockup del Dashboard](https://kzmopyy1o5mc869a46rn.lite.vusercontent.net/)

---
### Notas Técnicas

* **Frontend**: React.js (preferiblemente con `hooks` y `useEffect` para la carga de datos)
* **Gráficas**: Uso sugerido de librerías como `Chart.js` o `Recharts`
* **Consumo de datos**: Mediante `axios` o `fetch`, desde los endpoints de la API
* **Estado**: Se recomienda usar `React Context` o `Redux` si la app crece en complejidad
* **Autenticación**: Si la API requiere token, incluir en headers de la solicitud
* **Mejoras futuras**: Exportación a PDF/Excel, gráficos comparativos por categorías, notificaciones automáticas
