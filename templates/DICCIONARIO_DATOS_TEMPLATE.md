# Plantilla para Diccionario de Datos

Este documento debe acompañar cada proyecto profesional y ser actualizado conforme evolucionen los datos y variables utilizadas.

## Estructura Sugerida

| Variable         | Tipo de dato | Descripción / Significado | Fuente / Origen | Rango esperado | Observaciones |
|------------------|--------------|--------------------------|-----------------|----------------|--------------|
| ejemplo_var      | numérico     | Breve descripción        | INE             | 0-100          | ...          |
| ejemplo_cat      | categórico   | Breve descripción        | Encuesta X      | A, B, C        | ...          |

## Instrucciones
- Documenta cada variable utilizada en el proyecto.
- Especifica el tipo de dato (numérico, categórico, fecha, texto, etc.).
- Explica el significado y contexto de cada variable.
- Indica la fuente original y el rango esperado de valores.
- Añade observaciones relevantes (transformaciones, codificaciones, advertencias, etc.).

## Ejemplo de Registro
| Variable         | Tipo de dato | Descripción / Significado | Fuente / Origen | Rango esperado | Observaciones |
|------------------|--------------|--------------------------|-----------------|----------------|--------------|
| edad             | numérico     | Edad del individuo       | Encuesta Pobl.  | 0-120          | Revisar outliers |
| sexo             | categórico   | Sexo biológico           | Encuesta Pobl.  | M, F           | Codificación estándar |
| ingreso          | numérico     | Ingreso anual (€)        | INE             | 0-200000       | Valores extremos posibles |

---

Este archivo debe ser revisado y validado en cada iteración importante del proyecto.