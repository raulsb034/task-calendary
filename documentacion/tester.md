# Documentación para testers

## Objetivo de las pruebas
Verificar que la aplicación `Task Calendary` funcione correctamente y que todos los requisitos solicitados estén implementados y validados.

## Archivos de pruebas actuales

- `tests/test_models.py`
  - Valida el comportamiento de las entidades `Task` y `Event`.
- `tests/test_controllers.py`
  - Valida la lógica de negocio de `TaskCalendarController`.
- `tests/test_functional_regression.py`
  - Valida los flujos funcionales y pruebas de regresión de tareas.
- `tests/test_nonfunctional.py`
  - Valida aspectos no funcionales como performance básica y valores constantes.

## Tipos de pruebas cubiertos

### Pruebas unitarias
- Validación de `Task` y sus propiedades.
- Validación de `Event` y su lógica de duración/solapamiento.
- Validación de creación, actualización, eliminación y estado de tareas.
- Validación de búsqueda y estadísticas.

### Pruebas funcionales
- Flujo completo: crear, editar y eliminar tareas.
- Verificación de filtros por nombre, prioridad y categoría.
- Verificación de la existencia de tareas iniciales cargadas.

### Pruebas de regresión
- Búsqueda sin criterios que debe fallar.
- Actualización con fecha pasada que debe fallar.
- Verificación de que los casos corregidos no vuelvan a fallar.

### Pruebas no funcionales
- Evaluación básica de rendimiento de `get_tasks_for_month()` con más de 300 tareas.
- Verificación de los valores de color asociados a cada prioridad.
- Verificación de normalización estricta de categoría.

## Cómo ejecutar las pruebas

Desde la raíz del proyecto:

```bash
python -m unittest discover -s tests
```

## Resultados esperados

- Todas las pruebas deben pasar con `OK`.
- No debe haber errores de sintaxis en los archivos Python.
- El punto de entrada `src/app.py` debe ejecutarse sin errores de importación.

## Notas importantes

- El código actual no persiste tareas en disco; la persistencia es en memoria durante la ejecución.
- El punto de entrada correcto es `python src/app.py`.
- La prueba de interfaz Tkinter debe complementarse con verificación manual de la creación, edición y eliminación desde el calendario.
