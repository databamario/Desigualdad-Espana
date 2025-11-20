# Checklist para Incorporación de Nueva Tabla o Variable

Este procedimiento debe seguirse cada vez que se añade una nueva tabla o variable al proyecto, para garantizar trazabilidad, validación y documentación completa.

## Pasos Obligatorios

1. **ETL y Carga de Datos**
   - [ ] Añadir la tabla/variable al pipeline ETL.
   - [ ] Documentar la fuente y el proceso de importación.

2. **Validación Automática**
   - [ ] Definir criterios y umbrales de validación para la nueva variable.
   - [ ] Añadir la variable a los scripts/notebooks de validación automática.
   - [ ] Revisar y registrar warnings generados.

3. **Diccionario de Datos**
   - [ ] Documentar la nueva variable en el diccionario de datos (nombre, tipo, significado, fuente, rango, observaciones).

4. **Criterios y Umbrales**
   - [ ] Actualizar el archivo de criterios y umbrales de validación.
   - [ ] Justificar los nuevos umbrales y documentar la fuente.

5. **Análisis y Reporting**
   - [ ] Incluir la variable en los notebooks de análisis y visualización si corresponde.
   - [ ] Documentar su uso y relevancia en las conclusiones/limitaciones.

6. **Revisión Independiente**
   - [ ] Registrar la incorporación y validación en el archivo de revisión independiente.
   - [ ] Solicitar revisión cruzada si es relevante.

## Observaciones y Tareas Pendientes
- [ ] ...

---

Este checklist debe archivarse y actualizarse con cada incorporación significativa para mantener el estándar profesional.