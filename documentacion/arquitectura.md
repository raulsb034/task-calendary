# Arquitectura de Task Calendary

## Objetivo del proyecto
Aplicación de escritorio en Python con interfaz gráfica Tkinter para crear, filtrar y visualizar tareas en un calendario mensual.

## Estructura del proyecto

- `src/`
  - `app.py`: Punto de entrada ejecutable.
  - `views.py`: Interfaz gráfica con pestañas, filtros, calendario y estadísticas.
  - `models.py`: Modelos de datos para `Task`, categorías, prioridades y eventos.
  - `controllers.py`: Lógica de negocio, validaciones, filtros y estadísticas.

- `tests/`
  - `test_models.py`: Validaciones y comportamientos de las entidades.
  - `test_controllers.py`: Validaciones de tareas, filtros y estadísticas.

- `documentacion/`
  - `arquitectura.md`: Documentación del diseño actual.
  - `desarrollador.md`: Guía técnica para desarrolladores.
  - `tester.md`: Guía de pruebas y criterios de aceptación.

## Diseño de la aplicación

### Interfaz de usuario

- Pestañas principales:
  - `Tareas`: formulario para crear, editar, completar y eliminar tareas.
  - `Calendario`: calendario mensual con navegación entre meses, filtro por nombre/prioridad/categoría y visualización de tareas por día.
  - `Estadísticas`: resumen global de tareas creadas, pendientes y completadas.

- Filtros:
  - Input blanco para nombre.
  - Botón de búsqueda azul.
  - Filtrado por nombre, prioridad y categoría de forma individual o conjunta.
  - Mensaje de error si se intenta filtrar sin criterios.

- Calendario:
  - Vista mensual con celdas por día.
  - Dentro de cada celda aparece el nombre de la tarea y el color según su prioridad.
  - Las tareas del mismo día se ordenan por hora y, si coinciden, por prioridad.
  - Se muestra un mensaje cuando no hay tareas disponibles para el filtro actual.

### Modelo de datos

- `Task`
  - Campos: `id`, `title`, `description`, `due_date`, `due_time`, `category`, `priority`, `status`, `created_at`.
  - Categorías fijas: `Estudio`, `Trabajo`, `Personal`.
  - Prioridades fijas: `Alta`, `Media`, `Baja` con colores rojo, verde y azul.
  - Todas las tareas son visibles para el usuario.

- `Event`
  - Se mantiene como modelo auxiliar para eventos con fecha, hora de inicio, hora de fin y descripción.

### Controlador

- `TaskCalendarController`
  - Validaciones de creación y edición de tareas.
  - No permite crear ni editar tareas con fecha pasada.
  - Búsqueda de tareas por nombre, prioridad y categoría.
  - Generación de estadísticas globales.
  - Ordenación de tareas por hora y prioridad.

## Requisitos cumplidos

- RF-01: filtro con botón de búsqueda encima del calendario mensual.
- RF-02: tareas con nombre, fecha, hora, descripción, prioridad y categoría.
- RF-03: tareas dentro de la celda del día con color según prioridad.
- RF-04: filtrado por nombre, prioridad y categoría.
- RF-05: spinner visual en acciones que requieren respuesta.
- RF-06: input de filtro blanco y botón de búsqueda azul.
- RF-07: ordenación por hora, luego prioridad.
- RF-08: todos los campos visibles.
- RF-09: 3 colores de prioridad: rojo, verde y azul.
- RF-10: categorías `Estudio`, `Trabajo`, `Personal`.
- RF-11: categorías fijas.
- RF-12: mensajes de confirmación y error en castellano.
- RF-13: mensajes en castellano.
- RF-14: confirmación antes de eliminar.
- RF-15: mensaje si no hay tareas en el filtro.
- RF-16: no permite filtrar sin criterios.
- RF-17: no permite crear/modificar tareas con fecha anterior.
- RF-18: permite eliminar tareas pasadas.
- RF-19: pestaña de estadísticas globales.
- RF-20: estadísticas de tareas pendientes, no completadas y completadas.
- RF-21: estadísticas globales de todas las tareas.

## Requisitos no funcionales

- RNF-01: la búsqueda no se ejecuta si no hay criterio.
- RNF-02: idioma castellano en la interfaz.
- RNF-03: prioridades destacan con colores consistentes.
- RNF-04: interfaz clara y usable.
- RNF-05: colores de prioridad accesibles.
- RNF-06: diseño modular para añadir funciones futuras.
