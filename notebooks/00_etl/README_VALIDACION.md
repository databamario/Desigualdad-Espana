# Arquitectura Modular de Validación de Datos

## 📁 Estructura del Proyecto

```
desigualdad_social_etl/
├── notebooks/
│   ├── 00_etl/
│   │   ├── 01_desigualdad_etl.ipynb          # ETL principal
│   │   ├── 02a_validacion_INE.ipynb          # ✅ Validación tablas INE
│   │   ├── 02b_validacion_EUROSTAT.ipynb     # ✅ Validación tablas EUROSTAT
│   │   ├── 02c_validacion_integracion.ipynb  # ✅ Validación integración
|
│   ├── 02_run_validation.py                  # 🎯 ORQUESTADOR
│   ├── 01_analisis_nacional/
│   ├── 02_analisis_regional/
│   └── 03_comparativa_europa/
├── utils/
│   ├── validation_framework.py               # Framework reutilizable
│   ├── validation_rules.py                   # Reglas declarativas
│   └── config.py                             # Configuración global
├── data/
│   └── validated/
│       ├── logs/                             # 📄 Reportes JSON/CSV
│       └── README.md
└── scripts/
    ├── cleanup_validated_tables.sql
    └── cleanup_validated_tables.py
```

---

## 🎯 ¿Cómo Ejecutar la Validación?

### Opción 1: Ejecutar todo automáticamente (RECOMENDADO)

```bash
cd notebooks
python 02_run_validation.py
```

Este script ejecutará automáticamente:
1. `02a_validacion_INE.ipynb`
2. `02b_validacion_EUROSTAT.ipynb`
3. `02c_validacion_integracion.ipynb`

Y generará reportes consolidados.

### Opción 2: Ejecutar notebooks individualmente

Abre y ejecuta cada notebook en VS Code/Jupyter en este orden:

1. **`02a_validacion_INE.ipynb`** - Validar tablas INE
2. **`02b_validacion_EUROSTAT.ipynb`** - Validar tablas EUROSTAT
3. **`02c_validacion_integracion.ipynb`** - Validar coherencia entre fuentes

---

## 📊 Módulos de Validación

### 1. `02a_validacion_INE.ipynb`

**Objetivo**: Validar calidad de todas las tablas INE

**Validaciones**:
- ✅ Esquema y tipos de datos
- ✅ Unicidad de claves primarias
- ✅ Valores faltantes
- ✅ Rangos lógicos (0-100%)
- ✅ Coherencia temporal
- ⚠️ Identificación de categorías a excluir

**Salida**:
- Reportes JSON/CSV por cada tabla en `data/validated/logs/`
- Resumen consolidado de todas las tablas INE

---

### 2. `02b_validacion_EUROSTAT.ipynb`

**Objetivo**: Validar calidad de todas las tablas EUROSTAT

**Validaciones**:
- ✅ Esquema y tipos de datos
- ✅ Unicidad de claves primarias
- ✅ Valores faltantes
- ✅ Rangos lógicos
- ✅ Coherencia temporal

**Salida**:
- Reportes JSON/CSV por cada tabla en `data/validated/logs/`
- Resumen consolidado de todas las tablas EUROSTAT

---

### 3. `02c_validacion_integracion.ipynb`

**Objetivo**: Validar coherencia entre tablas INE y EUROSTAT

**Validaciones**:
- 🔗 Coherencia temporal (años comunes)
- 🔗 Coherencia de valores (AROPE España INE vs EUROSTAT)
- 🔗 Compatibilidad de indicadores
- 🔗 Consistencia geográfica

**Salida**:
- Reporte de integración en `data/validated/logs/`
- Análisis de diferencias entre fuentes

---

## 🔧 Framework de Validación

### `utils/validation_framework.py`

Funciones reutilizables:
- `ValidationReport`: Clase para gestionar reportes
- `check_schema()`: Validar estructura y tipos
- `check_uniqueness()`: Validar unicidad
- `check_nulls()`: Validar valores faltantes
- `check_range()`: Validar rangos lógicos
- `check_year_continuity()`: Validar continuidad temporal

**Salida de reportes**:
- `report.save_json()`: Guarda reporte en JSON
- `report.save_csv()`: Guarda reporte en CSV
- `report.print_report()`: Imprime en consola

---

### `utils/validation_rules.py`

Reglas declarativas por tabla:

```python
INE_VALIDATION_RULES = {
    "INE_AROPE_Hogar": {
        "expected_columns": [...],
        "primary_key": ["Año", "Tipo_Hogar", "Indicador"],
        "critical_columns": [...],
        "range_checks": {...},
        "exclude_categories": {...},
        "expected_years": range(2008, 2024),
    },
    # ... más tablas
}

EUROSTAT_VALIDATION_RULES = {
    # ... tablas EUROSTAT
}
```

---

## 📄 Reportes de Validación

### Formato JSON

```json
{
  "table_name": "INE_AROPE_Hogar",
  "timestamp": "2025-11-13T14:30:52",
  "records_original": 352,
  "records_excluded": 44,
  "records_clean": 308,
  "errors": [],
  "warnings": ["Encontrados 44 registros de 'No consta'..."],
  "info": ["Esquema correcto: 4 columnas"],
  "error_count": 0,
  "warning_count": 1,
  "status": "PASSED"
}
```

### Formato CSV

| type | message | table_name | timestamp |
|------|---------|------------|-----------|
| INFO | Esquema correcto: 4 columnas | INE_AROPE_Hogar | 2025-11-13T14:30:52 |
| WARNING | Encontrados 44 registros... | INE_AROPE_Hogar | 2025-11-13T14:30:52 |

---

## ✅ Ventajas de la Arquitectura Modular

### 1. **Escalabilidad**
- Fácil agregar nuevas fuentes de datos
- Cada módulo es independiente
- Crece sin degradar performance

### 2. **Mantenibilidad**
- Código separado por responsabilidad
- Fácil localizar y corregir errores
- Cambios aislados no afectan otros módulos

### 3. **Trazabilidad**
- Reporte por tabla + reporte consolidado
- Timestamp de cada validación
- Historial de validaciones en logs/

### 4. **Flexibilidad**
- Ejecutar todo o solo un módulo
- Configuración declarativa en validation_rules.py
- Fácil personalizar reglas por tabla

### 5. **Reusabilidad**
- Framework reutilizable para nuevos proyectos
- Funciones genéricas aplicables a cualquier tabla
- Reglas declarativas fáciles de compartir

---

## 🚀 Flujo de Trabajo Completo

```
1. ETL (01_desigualdad_etl.ipynb)
   ↓
2. Validación modular:
   - 02a_validacion_INE.ipynb
   - 02b_validacion_EUROSTAT.ipynb
   - 02c_validacion_integracion.ipynb
   ↓
3. Revisión de reportes (data/validated/logs/)
   ↓
4. Análisis exploratorio:
   - 01_analisis_nacional/
   - 02_analisis_regional/
   - 03_comparativa_europa/
```

---

## 🔍 Interpretación de Resultados

### Estados de Validación

- **PASSED**: ✅ Tabla validada sin errores críticos
- **FAILED**: ❌ Errores críticos detectados (requiere acción)
- **NO_RULES**: ⚠️ No hay reglas configuradas (revisar si es necesario)
- **ERROR**: 🚫 Error al cargar/procesar tabla (problema técnico)

### Priorización

1. **Errores críticos (FAILED)**: Corregir INMEDIATAMENTE
2. **Advertencias (warnings)**: Revisar y decidir acción
3. **NO_RULES**: Evaluar si requiere reglas de validación
4. **PASSED**: Continuar con análisis

---

## 📚 Documentación Adicional

- **`data/validated/README.md`**: Guía completa del sistema refactorizado
- **`validation_framework.py`**: Docstrings de todas las funciones
- **`validation_rules.py`**: Comentarios sobre cada regla

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué no crear tablas VALIDATED_* en SQL Server?**

R: La validación NO debe modificar datos. Las tablas originales son la fuente de verdad. Las exclusiones se aplican en memoria durante el análisis.

**P: ¿Cómo agrego reglas para una nueva tabla?**

R: Edita `utils/validation_rules.py` y agrega un diccionario con las reglas en `INE_VALIDATION_RULES` o `EUROSTAT_VALIDATION_RULES`.

**P: ¿Puedo ejecutar solo un módulo?**

R: Sí, abre el notebook individual en VS Code y ejecútalo. No necesitas el orquestador.

**P: ¿Qué hago si una tabla tiene status FAILED?**

R: Revisa el reporte JSON/CSV en `data/validated/logs/` para ver los errores específicos. Corrige los datos en origen o ajusta las reglas si son incorrectas.

**P: ¿Los reportes se sobrescriben?**

R: No. Cada ejecución crea un nuevo reporte con timestamp único, permitiendo rastrear el historial de validaciones.

---

**Autor**: Proyecto Desigualdad Social ETL  
**Fecha**: 2025-11-13  
**Versión**: 2.0 (Arquitectura Modular)
