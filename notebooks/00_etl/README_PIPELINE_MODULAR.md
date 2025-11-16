# 📊 Pipeline ETL Modular - Desigualdad Social

## 🎯 Visión General

Sistema ETL modular para extracción, transformación y carga de datos de desigualdad social desde INE y Eurostat a SQL Server.

## 📁 Estructura del Pipeline

```
notebooks/00_etl/
├── 01_run_etl.py                        # ⚙️  ORQUESTADOR PRINCIPAL
├── 01a_extract_transform_INE.ipynb       # 📊 Módulo INE (14 tablas)
├── 01b_extract_transform_EUROSTAT.ipynb  # 🌍 Módulo Eurostat (14 tablas)
├── 01c_load_to_sql.ipynb                 # 📤 Módulo de Carga SQL
└── 02_run_validation.py                  # ✅ Validación post-carga
```

## 🚀 Cómo Ejecutar el Pipeline

### Opción 1: Ejecutar Pipeline Completo (RECOMENDADO)

```powershell
cd notebooks/00_etl
python 01_run_etl.py
```

**Qué hace:**
1. Ejecuta `01a_extract_transform_INE.ipynb` → Extrae 14 tablas INE
2. Ejecuta `01b_extract_transform_EUROSTAT.ipynb` → Extrae 14 tablas Eurostat
3. Ejecuta `01c_load_to_sql.ipynb` → Carga 28 tablas a SQL Server

**Ventajas:**
- ✅ Control centralizado de errores
- ✅ Logs claros de ejecución
- ✅ Si falla un módulo, se detiene todo el pipeline
- ✅ Fácil integración con Airflow/Cron

### Opción 2: Ejecutar Módulos Individual

Si necesitas re-ejecutar solo un módulo:

```powershell
# Solo INE
jupyter nbconvert --to notebook --execute --inplace 01a_extract_transform_INE.ipynb

# Solo Eurostat
jupyter nbconvert --to notebook --execute --inplace 01b_extract_transform_EUROSTAT.ipynb

# Solo Carga SQL
jupyter nbconvert --to notebook --execute --inplace 01c_load_to_sql.ipynb
```

**Cuándo usar:**
- Falló la API del INE → Re-ejecutar solo `01a`
- Necesitas actualizar solo datos Eurostat → Re-ejecutar `01b` + `01c`

## 📦 Caché de Datos (Pickles)

Los módulos `01a` y `01b` generan archivos pickle en:

```
outputs/pickle_cache/
├── df_ipc_anual.pkl
├── df_umbral_limpio.pkl
├── df_gini_todos.pkl
└── ... (28 archivos total)
```

**Ventajas:**
- ⚡ Rápido: Cargar pickles es instantáneo vs re-descargar de APIs
- 🔧 Debugging: Si falla la carga SQL, puedes investigar los DataFrames sin re-ejecutar extracción
- 🔄 Reproducibilidad: Mismos datos garantizados entre ejecuciones

## 🔍 Validación

Después de ejecutar el ETL, valida que los datos se cargaron correctamente:

```powershell
python 02_run_validation.py
```

**Qué valida:**
- ✅ Las 28 tablas existen en SQL Server
- ✅ No hay duplicados
- ✅ Rangos de años correctos (2015-2024)
- ✅ Valores numéricos coherentes

## 📋 Tablas Generadas (28 total)

### INE (14 tablas)

| Tabla | Descripción | Registros Aprox |
|-------|-------------|----------------|
| `INE_IPC_Nacional` | IPC mensual → anual | ~40 años |
| `INE_Umbral_Pobreza_Hogar` | Umbral por tipo hogar | ~150 registros |
| `INE_Carencia_Material_Decil` | Carencia por decil | ~200 registros |
| `INE_AROPE_Edad_Sexo` | AROPE por edad/sexo | ~400 registros |
| `INE_AROPE_Hogar` | AROPE por tipo hogar | ~300 registros |
| `INE_AROPE_Laboral` | AROPE por situación laboral | ~250 registros |
| `INE_AROPE_CCAA` | AROPE por CCAA | ~300 registros |
| `INE_Gini_S80S20_CCAA` | Gini y S80/S20 por CCAA | ~400 registros |
| `INE_Renta_Media_Decil` | Renta media por decil | ~200 registros |
| `INE_Poblacion_Edad_Sexo_Nacionalidad` | Población detallada | ~8000 registros |
| `INE_Poblacion_Tipo_Hogar` | Población por hogar | ~500 registros |
| `INE_Poblacion_Edad_Sexo_CCAA` | Población por CCAA | ~2000 registros |
| `INE_Gasto_Medio_Hogar_Quintil` | Gasto por quintil (EPF) | ~300 registros |
| `INE_IPC_Sectorial_ECOICOP` | IPC sectorial | ~1500 registros |

### Eurostat (14 tablas)

| Tabla | Descripción | Registros |
|-------|-------------|-----------|
| `EUROSTAT_Gini_Espana` | Gini España | 10 años |
| `EUROSTAT_Gini_UE27` | Gini UE27 | 10 años |
| `EUROSTAT_Gini_Ranking` | Gini todos países | ~365 registros |
| `EUROSTAT_AROP_Espana` | AROP España | 10 años |
| `EUROSTAT_AROP_UE27` | AROP UE27 | 10 años |
| `EUROSTAT_AROP_Ranking` | AROP todos países | ~365 registros |
| `EUROSTAT_S80S20_Espana` | S80/S20 España | 10 años |
| `EUROSTAT_S80S20_UE27` | S80/S20 UE27 | 10 años |
| `EUROSTAT_S80S20_Ranking` | S80/S20 todos países | ~365 registros |
| `EUROSTAT_Brecha_Pobreza_Espana` | Brecha España | 10 años |
| `EUROSTAT_Brecha_Pobreza_UE27` | Brecha UE27 | 10 años |
| `EUROSTAT_Brecha_Pobreza_Ranking` | Brecha todos países | ~365 registros |
| `EUROSTAT_Impacto_Redistributivo_Espana` | Impacto Gini España | 10 años |
| `EUROSTAT_Impacto_Redistributivo_UE27` | Impacto Gini UE27 | 10 años |

## 🛠️ Troubleshooting

### Error: "API del INE no responde"

```powershell
# Re-ejecutar solo módulo INE después de esperar
jupyter nbconvert --to notebook --execute --inplace 01a_extract_transform_INE.ipynb
# Luego cargar a SQL
jupyter nbconvert --to notebook --execute --inplace 01c_load_to_sql.ipynb
```

### Error: "Duplicados en EUROSTAT_Gini_Ranking"

Este problema fue resuelto en la modularización. El módulo `01b` ahora:
- ✅ Filtra correctamente `age='TOTAL'` y `sex='T'`
- ✅ Elimina columnas `age` y `sex` de las tablas Ranking

### Error: "No se puede conectar a SQL Server"

Verifica:
1. SQL Server está corriendo
2. La base de datos `Desigualdad_Social` existe
3. Tienes permisos de escritura

```sql
-- Crear base de datos si no existe
CREATE DATABASE Desigualdad_Social;
```

## 📊 Ventajas del Sistema Modular

| Aspecto | Antes (Monolítico) | Ahora (Modular) |
|---------|-------------------|-----------------|
| **Debugging** | Difícil identificar dónde falla | Error aislado por módulo |
| **Mantenimiento** | Cambio en INE afecta todo | Solo editar `01a` |
| **Tiempo ejecución** | 5-10 min siempre | 1-2 min si solo re-cargas SQL |
| **Logs** | Mezclados | Separados por módulo |
| **Reusabilidad** | No | Pickles reutilizables |
| **Orquestación** | Manual | Airflow/Cron compatible |

## 🔄 Ciclo de Actualización Recomendado

```
1. Mensual: Ejecutar pipeline completo (01_run_etl.py)
2. Semanal: Solo re-ejecutar 01b + 01c (datos Eurostat más recientes)
3. Ad-hoc: Si falla validación, revisar módulo específico
```

## 📝 Logs de Ejecución

El orquestador `01_run_etl.py` genera logs con formato:

```
[2025-11-15 14:30:00] [INFO] 🚀 INICIANDO PIPELINE ETL
[2025-11-15 14:30:05] [INFO] Iniciando módulo: 01a - Extracción INE
[2025-11-15 14:32:10] [SUCCESS] ✅ 01a - Extracción INE completado
[2025-11-15 14:32:15] [INFO] Iniciando módulo: 01b - Extracción Eurostat
[2025-11-15 14:34:20] [SUCCESS] ✅ 01b - Extracción Eurostat completado
[2025-11-15 14:34:25] [INFO] Iniciando módulo: 01c - Carga SQL Server
[2025-11-15 14:35:30] [SUCCESS] ✅ 01c - Carga SQL Server completado
[2025-11-15 14:35:30] [INFO] ✅ PIPELINE COMPLETADO (Duración: 5.5 min)
```

## 🎯 Próximos Pasos

1. Ejecutar `python 01_run_etl.py` para primera carga
2. Verificar `python 02_run_validation.py`
3. Si todo pasa, ¡datos listos para análisis!

---

**Autor:** Proyecto Desigualdad Social ETL  
**Última actualización:** 2025-11-15
