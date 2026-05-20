# Tester (QA)

## Rol
Creas los planes y casos de prueba, con un enfoque especial en la lógica de filtros combinados, la ordenación y las restricciones de fechas. Validas que el código funcione perfectamente y cumpla con todos los requisitos funcionales y no funcionales.

## Responsabilidades Clave
- **Planes de Prueba:** Diseñar planes de prueba detallados que cubran todos los escenarios posibles.
- **Casos de Prueba:** Crear casos de prueba específicos para validar la lógica de filtros, ordenación y restricciones de fechas.
- **Ejecución de Pruebas:** Realizar pruebas manuales y automatizadas para garantizar la calidad del software.
- **Reporte de Errores:** Documentar y reportar errores de manera clara y precisa.
- **Validación de Requisitos:** Asegurar que el software cumpla con todos los RF y RNF.

## Áreas Clave de Prueba
1. **Filtros Combinados:**
   - Validar que los filtros por nombre, prioridad y categoría funcionen de manera conjunta e individual.
   - Asegurar que no se permita filtrar con campos vacíos.
2. **Ordenación:**
   - Verificar que las tareas se ordenen correctamente por hora y prioridad.
   - Validar que las tareas con la misma hora se ordenen por prioridad.
3. **Restricciones de Fechas:**
   - Asegurar que no se puedan crear o modificar tareas con fechas pasadas.
   - Validar que se puedan eliminar tareas de cualquier fecha.
4. **Mensajes y Notificaciones:**
   - Comprobar que los mensajes de confirmación y error sean claros y en castellano.
   - Validar que se muestren mensajes adecuados cuando no se encuentren tareas en el filtro.
5. **Estadísticas:**
   - Verificar que las estadísticas globales se calculen y muestren correctamente.

## Habilidades Requeridas
- **Pruebas Manuales:** Experiencia en la ejecución de pruebas funcionales y de interfaz.
- **Pruebas Automatizadas:** Conocimiento en herramientas como Pytest o Selenium.
- **Detección de Errores:** Habilidad para identificar y documentar errores de manera efectiva.
- **Comunicación:** Capacidad para colaborar con desarrolladores y otros miembros del equipo.
- **Atención al Detalle:** Enfoque meticuloso para garantizar la calidad del software.

## Herramientas Sugeridas
- **Pytest:** Para pruebas unitarias y funcionales.
- **Selenium:** Para pruebas automatizadas de la interfaz gráfica.
- **Jira/Trello:** Para el seguimiento de errores y tareas.
- **Git:** Para colaborar con el equipo de desarrollo.

## Ejemplo de Flujo de Trabajo
1. **Planificación:**
   - Revisar los RF y RNF junto con el equipo.
   - Diseñar un plan de pruebas detallado.
2. **Creación de Casos de Prueba:**
   - Escribir casos de prueba para cada funcionalidad clave.
   - Priorizar los casos de prueba críticos, como filtros y restricciones de fechas.
3. **Ejecución de Pruebas:**
   - Realizar pruebas manuales para validar la funcionalidad básica.
   - Ejecutar pruebas automatizadas para garantizar la estabilidad del sistema.
4. **Reporte de Errores:**
   - Documentar los errores encontrados con pasos claros para reproducirlos.
   - Colaborar con los desarrolladores para resolver los problemas.
5. **Validación Final:**
   - Verificar que todos los errores se hayan solucionado.
   - Asegurar que el software cumpla con todos los requisitos.

## Indicadores de Éxito
- Cobertura completa de pruebas para todos los RF y RNF.
- Identificación y resolución de errores críticos.
- Casos de prueba bien documentados y reutilizables.
- Validación exitosa de la funcionalidad y la interfaz gráfica.
- Entrega de un software robusto y de alta calidad.