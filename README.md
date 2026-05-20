# README - Manual de Usuario: Task Calendary

## 1. Stack Tecnológico y Arquitectura

La aplicación está diseñada bajo un enfoque modular con separación de responsabilidades entre la interfaz de usuario, los modelos y la lógica de negocio.

* **Lenguaje de Programación:** Python 3.12
* **Interfaz Gráfica (GUI):** `Tkinter`
* **Persistencia Actual:** en memoria durante la ejecución
* **Punto de entrada:** `src/app.py`

## 2. Modelo de datos

Cada tarea se modela con los siguientes campos principales:

 * `id` -> Integer -> Autoincremental
 * `title` -> String -> **Obligatorio**
 * `due_date` -> Date -> **Obligatorio** -> Formato YYYY-MM-DD
 * `due_time` -> Time -> **Obligatorio** -> Formato HH:MM
 * `description` -> String -> Detalle extendido de la tarea
 * `category` -> Enum: Estudio, Trabajo, Personal
 * `priority` -> Enum: Alta, Media, Baja
 * `status` -> Enum: Pendiente, Completada

## 3. Configuración del Entorno de Desarrollo

 1. git clone [github](https://github.com/raulsb034/task-calendary-)
 2. cd task-calendary
 3. Windows: python -m venv venv & .\\venv\\Scripts\\activate
 4. Linux: python3 -m venv venv & source venv/bin/activate
 5. Instalar dependencias si se añaden en el futuro
 6. Ejecutar la app: `python src/app.py`

## 4. Lógica de los Módulos

* **Ordenación de tareas:** por hora ascendente y luego por prioridad.
* **Filtrado de calendario:** por nombre, prioridad y categoría.
* **Carga inicial:** se precargan tareas de ejemplo en `TaskCalendarController._seed_sample_tasks()`.

## 5. Plan de pruebas

Las pruebas del proyecto cubren las siguientes categorías:

1. **Pruebas unitarias:** validan el modelo `Task`, `Event` y la lógica de `TaskCalendarController`.
2. **Pruebas funcionales:** validan el flujo de creación, edición, eliminación y filtrado de tareas.
3. **Pruebas de regresión:** aseguran que los casos corregidos previamente se mantengan estables.
4. **Pruebas no funcionales:** validan performance básica y la configuración de prioridades.

## 6. Ejecución de pruebas

```bash
python -m unittest discover -s tests
```

## 7. Mantenimiento a futuro

* **Migración de Base de Datos:** el diseño permite agregar persistencia en disco sin cambiar la lógica de negocio principal.
* **Seguridad:** se puede añadir una capa de autenticación antes de lanzar la interfaz.

