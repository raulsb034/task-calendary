# Plan de pruebas y resultados

## Objetivo
Documentar las pruebas realizadas en la aplicación `Task Calendary` para cubrir:
- pruebas unitarias
- pruebas funcionales
- pruebas de regresión
- pruebas no funcionales

## Comandos utilizados

```bash
python -m unittest discover -s tests
```

## Pruebas ejecutadas

### Pruebas unitarias
- `tests/test_models.py`
- `tests/test_controllers.py`

### Pruebas funcionales
- `tests/test_functional_regression.py`
  - flujo de creación, actualización y eliminación de tareas
  - filtros y estadísticas
  - validación de tareas iniciales generadas
  - regresión en búsqueda con criterios
  - regresión en actualización de fecha pasada

### Pruebas no funcionales
- `tests/test_nonfunctional.py`
  - verificación de tiempo de respuesta de `get_tasks_for_month`
  - verificación de los valores de color de prioridad
  - validación de normalización estricta de categoría

## Resultados de validación

- Todas las pruebas de unidad, funcionales, de regresión y no funcionales creadas pasan correctamente.
- `python -m unittest discover -s tests` ejecutó 23 pruebas con resultado `OK`.
- La aplicación no incluye actualmente persistencia JSON ni archivo `tareas.json` a pesar de lo documentado en el README anterior.
- El punto de entrada ejecutable es `src/app.py`.

## Requisitos verificados

1. Creación de tareas mediante calendario: implementado en `src/views.py` con modal de creación al hacer clic en la celda.
2. Edición de tareas desde el calendario: implementado con clic en etiqueta de tarea y modal de edición.
3. Eliminación de tareas desde el calendario modal: implementado.
4. Filtros por nombre, prioridad y categoría: implementado en el controlador y la vista.
5. Estadísticas de tareas totales, pendientes y completadas: implementado en `src/views.py` y `src/controllers.py`.
6. Carga inicial de tareas de ejemplo: implementado en `TaskCalendarController._seed_sample_tasks()`.

## Observaciones

- No se han implementado pruebas automáticas de GUI con Tkinter en este momento; la prueba visual se recomienda como complemento manual.
- El documento `README.md` se ha actualizado para reflejar el estado real actual del proyecto.
