# Documentación para desarrolladores

## Estructura del proyecto

- `src/app.py`: punto de entrada de la aplicación.
- `src/views.py`: contiene la interfaz de usuario con Tkinter y la lógica de interacción con el controlador.
- `src/models.py`: define las entidades `Task` y `Event` y su comportamiento asociado.
- `src/controllers.py`: maneja la lógica de negocio, crea y actualiza tareas y eventos.
- `tests/`: contiene pruebas unitarias para validar los modelos y la lógica de negocio.

## Detalles de implementación

### Modelos

- `Task`
  - Campos: `id`, `title`, `description`, `due_date`, `status`, `priority`, `created_at`.
  - Métodos:
    - `mark_completed()`: marca la tarea como completada.
    - `is_overdue(current_date=None)`: determina si la tarea está vencida según la fecha actual.

- `Event`
  - Campos: `id`, `title`, `event_date`, `start_time`, `end_time`, `description`.
  - Métodos:
    - `duration_minutes()`: calcula la duración en minutos.
    - `overlaps(other)`: comprueba si el evento se solapa con otro evento en la misma fecha.

### Controlador

- `TaskCalendarController`
  - Maneja IDs automáticos para tareas y eventos.
  - Provee operaciones CRUD para tareas (`add_task`, `update_task`, `delete_task`, `mark_task_completed`).
  - Provee operaciones para eventos (`add_event`, `delete_event`, `list_events_for_date`).
  - Genera listados de tareas y elementos por fecha.

### Vista

- `TaskCalendarView`
  - Utiliza `tkinter` y `ttk`.
  - Tiene dos pestañas: `Tareas` y `Calendario`.
  - Permite crear, actualizar, completar y eliminar tareas.
  - Permite crear eventos y ver tareas/eventos por fecha.
  - Actualiza vistas al guardar cambios.

## Requisitos de ejecución

- Python 3.11+.
- Tkinter disponible en la instalación de Python.

## Flujo de desarrollo

1. Modificar `src/models.py` para cambiar o extender el esquema de datos.
2. Ajustar `src/controllers.py` para actualizar la lógica de negocio.
3. Actualizar `src/views.py` para reflejar cambios en la interfaz o nuevas operaciones.
4. Agregar o modificar pruebas en `tests/` para asegurar el comportamiento.

## Notas para el desarrollador

- Mantener la separación entre la lógica de la aplicación (`controllers.py`) y la interfaz (`views.py`).
- No incluir lógica de negocio compleja directamente en la UI.
- Las pruebas deben centrarse en `controllers.py` y `models.py`.
