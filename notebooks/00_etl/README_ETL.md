# 📊 Pipeline ETL - Desigualdad Social

Sistema **modular y ordenado** para extraer, transformar y cargar datos de desigualdad social desde INE y Eurostat.

## 🎯 Estructura

```
00_etl/
├── 01a_extract_transform_INE.ipynb      ← Extrae 14 tablas del INE
├── 01b_extract_transform_EUROSTAT.ipynb ← Extrae 14 tablas de Eurostat  
├── 01c_load_to_sql.ipynb                ← Carga 28 tablas a SQL Server
└── run_etl.py                           ← Ejecuta todo automáticamente
```

## ⚙️ Funcionamiento

### **Paso 1: Extracción INE** (01a_extract_transform_INE.ipynb)
- Extrae 14 tablas de la API del INE
- Transforma y limpia los datos
- Guarda en `outputs/pickle_cache/*.pkl`

**Tablas:**
- IPC Nacional
- Umbral de Pobreza por Hogar
- Carencia Material por Decil
- AROPE (Edad/Sexo, Hogar, Laboral, CCAA)
- Gini y S80/S20 por CCAA
- Renta Media por Decil
- Población (Edad/Sexo/Nacionalidad, Tipo Hogar, CCAA)
- Gasto Medio por Quintil
- IPC Sectorial

### **Paso 2: Extracción Eurostat** (01b_extract_transform_EUROSTAT.ipynb)
- Extrae 14 tablas de la API de Eurostat (SDMX-JSON)
- Para cada indicador: España, UE27 y Ranking
- **Bug corregido**: Filtro `age` usando `is not None` (evita duplicados)
- Guarda en `outputs/pickle_cache/*.pkl`

**Indicadores:**
- Gini (España, UE27, Ranking)
- AROP - At Risk of Poverty (España, UE27, Ranking)
- S80/S20 - Ratio quintiles (España, UE27, Ranking)
- Brecha de Pobreza (España, UE27, Ranking)
- Impacto Redistributivo (España, UE27)

### **Paso 3: Carga SQL** (01c_load_to_sql.ipynb)
- Carga los 28 pickles a SQL Server
- Reemplaza tablas existentes
- Verifica que las 28 tablas estén cargadas

## 🚀 Ejecución

### Opción A: Ejecución Automática (Recomendado)
```bash
cd notebooks/00_etl
python run_etl.py
```

### Opción B: Ejecución Manual (paso a paso)
1. Abrir y ejecutar `01a_extract_transform_INE.ipynb`
2. Abrir y ejecutar `01b_extract_transform_EUROSTAT.ipynb`
3. Abrir y ejecutar `01c_load_to_sql.ipynb`

## 📦 Salidas

### Archivos Pickle (intermedios)
```
outputs/pickle_cache/
├── df_ipc_anual.pkl
├── df_umbral_limpio.pkl
├── df_carencia_limpio.pkl
├── ...
├── df_gini_es.pkl
├── df_gini_ue27.pkl
└── df_gini_todos.pkl
```

### Tablas SQL Server
```
Desigualdad_Social (28 tablas)
├── INE_IPC_Nacional
├── INE_Umbral_Pobreza_Hogar
├── INE_Carencia_Material_Decil
├── ...
├── EUROSTAT_Gini_Espana
├── EUROSTAT_Gini_UE27
└── EUROSTAT_Gini_Ranking
```

## 🔧 Requisitos

- Python 3.11+
- Jupyter Notebook
- Librerías: pandas, requests, pyodbc, sqlalchemy
- SQL Server (MARIOBAN\SQLEXPRESS)
- Base de datos: `Desigualdad_Social`

## ✅ Validación

Después de ejecutar el ETL, validar los datos:

```bash
cd notebooks/00_etl
python 02_run_validation.py
```

## 🐛 Bugs Corregidos

### Bug 1: Filtro de edad en Eurostat
**Problema:** `if filter_age and code != filter_age` no funciona cuando `filter_age='TOTAL'` (truthy)  
**Solución:** `if filter_age is not None and code != filter_age`  
**Impacto:** Evita duplicados en tablas de ranking (688 → 344 registros)

### Bug 2: Diccionario duplicado
**Problema:** Dos definiciones de `dataframes_a_cargar` (líneas 2745 y 3227)  
**Solución:** Una sola definición con las 28 tablas  
**Impacto:** Carga las 28 tablas completas (no solo 24)

## 📊 Ventajas de este Sistema

✅ **Modular**: Cada notebook hace UNA cosa (Extract, Extract, Load)  
✅ **Ordenado**: Nombres claros 01, 02, 03  
✅ **Separación clara**: Nada interfiere con otra parte  
✅ **Fácil debug**: Si falla Eurostat, solo re-ejecutas `02_extract_EUROSTAT.ipynb`  
✅ **Cache intermedio**: Pickles permiten saltar pasos ya completados  
✅ **Sin complejidad**: No hay clases, herencia, ni sobre-ingeniería  

## 🔄 Flujo Completo

```
┌─────────────────────┐
│  01_extract_INE     │
│  API INE → Pickles  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 02_extract_EUROSTAT │
│ API Eurostat→Pickles│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   03_load_SQL       │
│ Pickles → SQL Server│
└─────────────────────┘
```

---

**Última actualización:** 2025-01-15  
**Autor:** Mario  
**Proyecto:** Desigualdad Social - Análisis España y Europa
