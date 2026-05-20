# README - Manual de Usuario: Task Calendar

## 1. Stack Tecnológico y Arquitectura

La aplicación está diseñada bajo un enfoque modular de separación de responsabilidades (UI, Lógica de Negocio y Persistencia) para garantizar el desacoplamiento y facilitar futuras migraciones de infraestructura.

* **Lenguaje de Programación:** Python 3.10+
* **Interfaz Gráfica (GUI):** `Tkinter`.
* **Persistencia Local / Base de Datos:** Formato estructurado `JSON`.

## 2. Modelo de datos

Cada registro almacenado en la colección del archivo tareas.json debe cumplir estrictamente con la siguiente estructura de tipos:

 * ID -> Integer -> Clave primaria -> Autoincremental
 * nombre -> String -> **Obligatorio** -> nombre descriptivo de la actividad
 * fecha -> String -> **Obligatorio** -> Formato YYYY-MM-DD -> Debe ser igual o posterior a la fecha actual en creación
 * hora -> String -> **Obligatorio** -> Formato HH:MM -> Usado para la ordenación cronológica diaria
 * descripcion -> String -> Detalle extendido de la tarea
 * categoria -> String -> Enum: ALTA, MEDIA, BAJA -> categorias fijadas por el cliente
 * prioridad -> String -> Enum: Estudio, Trabajo, Personal -> prioridades fijadas por el cliente
 * completada -> Boolean -> default: false -> Estado de la tarea


 ## 3. Configuración del Entorno de Desarrollo

 1. git clone [github](https://github.com/raulsb034/task-calendary-)
 2. cd task-calendar
 3. Windows: python -m venv venv & .\\venv\\Scripts\\activate
 4. linux: python3 -m venv venv & source venv/bin/activate
 5. pip install -r requirements.txt
 6. python src/main.py


## 4. Lógica de los Módulos

Aquí se detallan las lógicas por las que se rige la aplicación:

* **Algoritmo de Ordenación**: Las tareas se recuperan aplicando un criterio de ordenación cronologico ascendente por hora y, ante horas iguales, se aplica una ordenación por prioridad

* **Gestión del Spinner**: Todas las funcionalidades de la app que necesitan un tiempo de carga, debe activarse un spinner. Debe lanzar un error si la carga de una funcionalidad supera los 60 segundos.


## 5. Plan de pruebas

Este repositorio incluye un conjunto de pruebas clasificadas bajo las siguientes metodologías:

1. **Pruebas Funcionales**: Validan la correcta persistencia del flujo
2. **Pruebas No Funcionales**: Verificación de las restricciones visuales de la paleta de colores para accesibilidad y simulación de latencia para activar la interrupción por Timeout de 1 minuto.
3. **Pruebas unitarias**: Pruebas independientes parametrizadas sobre los Requisitos Funcionales mínimos.
4. **Pruebas de Regresión**: Pruebas encargadas de la comprobación de la estabilidad del software no tocado.


## 6. Mantenimiento a futuro

El diseño se ha realizado de manera desaclopada para poder permitir las siguientes expansiones sin alterar el núcleo de la app:

* **Migración de Base de Datos**: Se puede realizar de manera eficiente un cambio en la gestión de los datos del usuario, cambiando el archivo tareas.json, donde se guardan actualmente las tareas, por una base de datos creando simplemente la conexión.


* **Implementación de seguirdad**: La arquitectura en la que se ha construido la aplicación permite contruir en el main.py una capa mas de seguridad añadiendo un Login o un register antes de llamar a la pantalla principal.

