# 🏗️ Arquitectura Profesional del Pipeline ETL

## 📋 Visión General

Sistema ETL modular y profesional basado en **Clean Architecture** y **SOLID principles**.

```
┌─────────────────────────────────────────────────────────────────┐
│                     NOTEBOOKS (UI Layer)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ 01a_INE.ipynb│  │01b_EURO.ipynb│  │01c_LOAD.ipynb│          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SRC (Business Logic Layer)                    │
│  ┌────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │ INEExtractor│  │EurostatExtract│  │ SQLRepository │          │
│  │   (Class)  │  │    (Class)    │  │   (Class)     │          │
│  └─────┬──────┘  └───────┬───────┘  └───────┬───────┘          │
│        └─────────────┬───────────────────────┘                  │
│                      ▼                                           │
│  ┌──────────────────────────────────────────────────┐           │
│  │         UTILS (Common Functions)                 │           │
│  │  • parsear_eurostat_sdmx()                       │           │
│  │  • fetch_api_data()                              │           │
│  │  • validar_dataframe()                           │           │
│  │  • guardar_pickle() / cargar_pickle()            │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CONFIG (Configuration Layer)                   │
│  • SQL_CONFIG                                                   │
│  • INE_TABLES                                                   │
│  • EUROSTAT_DATASETS                                            │
│  • YEAR_RANGE, GEO_CODES                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Estructura de Directorios

```
desigualdad_social_etl/
├── src/                              # 🎯 CÓDIGO FUENTE (Lógica de negocio)
│   ├── __init__.py
│   ├── config.py                     # ⚙️  Configuración centralizada
│   ├── utils.py                      # 🛠️  Utilidades comunes
│   ├── extractors/                   # 📥 Extractores de datos
│   │   ├── __init__.py
│   │   ├── eurostat_extractor.py    # Clase EurostatExtractor
│   │   └── ine_extractor.py         # Clase INEExtractor (TODO)
│   └── loaders/                      # 📤 Cargadores a SQL
│       ├── __init__.py
│       └── sql_repository.py        # Clase SQLRepository (TODO)
│
├── notebooks/                        # 📓 NOTEBOOKS (Orquestación)
│   └── 00_etl/
│       ├── 01a_extract_INE_v2.ipynb         # Usa INEExtractor
│       ├── 01b_extract_EUROSTAT_v2.ipynb    # Usa EurostatExtractor
│       ├── 01c_load_to_sql_v2.ipynb         # Usa SQLRepository
│       └── 01_run_etl_v2.py                 # Orquestador modular
│
├── tests/                            # 🧪 TESTS UNITARIOS
│   ├── test_utils.py
│   ├── test_eurostat_extractor.py
│   └── test_sql_repository.py
│
├── outputs/                          # 📊 DATOS GENERADOS
│   ├── pickle_cache/                 # Caché de DataFrames
│   ├── logs/                         # Logs de ejecución
│   ├── figuras/                      # Gráficos de análisis
│   └── tablas/                       # Tablas exportadas
│
└── docs/                             # 📖 DOCUMENTACIÓN
    ├── ARQUITECTURA.md               # Este archivo
    ├── API_REFERENCE.md              # Documentación de APIs
    └── CONTRIBUTING.md               # Guía de contribución
```

---

## 🎯 Principios de Diseño

### 1. **Separation of Concerns** ✅
- **Notebooks**: Solo orquestación y presentación
- **src/**: Lógica de negocio reutilizable
- **config.py**: Configuración centralizada

### 2. **DRY (Don't Repeat Yourself)** ✅
- Funciones comunes en `utils.py`
- No duplicar lógica de parseo, validación, logging

### 3. **Single Responsibility Principle** ✅
- `EurostatExtractor`: Solo extrae datos de Eurostat
- `SQLRepository`: Solo operaciones de base de datos
- `utils.py`: Solo funciones auxiliares

### 4. **Dependency Injection** ✅
- Configuración inyectada desde `config.py`
- No hardcodear valores en clases

### 5. **Testable Code** ✅
- Clases con métodos pequeños y testeables
- Tests unitarios en directorio separado

---

## 🔧 Componentes Principales

### 1️⃣ **config.py** - Configuración Centralizada

**Responsabilidad**: Almacenar toda la configuración del proyecto en un solo lugar.

**Contenido**:
```python
# SQL Server
SQL_CONFIG = {
    'servidor': 'MARIOBAN\\SQLEXPRESS',
    'base_datos': 'Desigualdad_Social',
    ...
}

# APIs
INE_BASE_URL = "https://servicios.ine.es/..."
EUROSTAT_BASE_URL = "https://ec.europa.eu/eurostat/..."

# Tablas
SQL_TABLE_NAMES = {
    'ine': [...],      # 14 tablas
    'eurostat': [...]  # 14 tablas
}
```

**Ventajas**:
- ✅ Cambios en un solo lugar
- ✅ Fácil migración entre entornos (dev, prod)
- ✅ Validación centralizada

---

### 2️⃣ **utils.py** - Utilidades Comunes

**Responsabilidad**: Funciones reutilizables sin estado.

**Funciones Clave**:
```python
# Logging
setup_logger(nombre_modulo: str) -> logging.Logger

# Caché
guardar_pickle(df: pd.DataFrame, nombre: str) -> Path
cargar_pickle(nombre: str) -> pd.DataFrame

# Validación
validar_dataframe(df, columnas_requeridas, nombre_tabla) -> Tuple[bool, List[str]]

# Parseo Eurostat (CRÍTICO)
parsear_eurostat_sdmx(
    data_json, value_name,
    filter_age='TOTAL',    # Evita duplicados
    filter_sex='T'         # Evita duplicados
) -> pd.DataFrame

# HTTP
fetch_api_data(url, params, max_retries=3) -> Dict
```

**Características**:
- ✅ Type hints en todos los parámetros
- ✅ Docstrings estilo Google
- ✅ Manejo robusto de errores
- ✅ Tests unitarios

---

### 3️⃣ **EurostatExtractor** - Extractor Profesional

**Archivo**: `src/extractors/eurostat_extractor.py`

**Responsabilidad**: Extraer y transformar datos de Eurostat.

**Arquitectura**:
```python
@dataclass
class IndicadorEurostat:
    """Value Object para encapsular un indicador"""
    nombre: str
    df_espana: pd.DataFrame
    df_ue27: pd.DataFrame
    df_ranking: pd.DataFrame


class EurostatExtractor:
    """Extractor profesional de Eurostat"""
    
    def __init__(self):
        self.logger = setup_logger('EurostatExtractor')
        self.indicadores: Dict[str, IndicadorEurostat] = {}
    
    def extraer_indicador(self, dataset_key: str) -> IndicadorEurostat:
        """Extrae un indicador específico"""
        ...
    
    def extraer_todos_los_indicadores(self) -> Dict[str, IndicadorEurostat]:
        """Extrae todos los indicadores configurados"""
        ...
    
    def guardar_cache(self) -> List[str]:
        """Guarda todos los DataFrames en pickle"""
        ...
    
    def obtener_resumen(self) -> pd.DataFrame:
        """Genera resumen de extracción"""
        ...
```

**Ventajas vs Código Antiguo**:

| Aspecto | Antiguo (Monolítico) | Nuevo (Clase) |
|---------|---------------------|---------------|
| **Reutilizable** | ❌ No | ✅ Sí (importable) |
| **Testeable** | ❌ Difícil | ✅ Fácil (unit tests) |
| **Logging** | ❌ Mezclado | ✅ Estructurado |
| **Validación** | ❌ Manual | ✅ Automática |
| **Documentación** | ❌ Escasa | ✅ Docstrings completos |
| **Manejo errores** | ❌ Basic | ✅ Robusto con reintentos |

---

### 4️⃣ **Notebooks** - Capa de Presentación

**Responsabilidad**: Orquestación y visualización, NO lógica de negocio.

**Ejemplo** (`01b_extract_EUROSTAT_v2.ipynb`):
```python
# ❌ MAL (Antiguo): Lógica mezclada con presentación
def parsear_eurostat_sdmx(...):  # Definir función en notebook
    ...

df = parsear_eurostat_sdmx(...)   # Usar en notebook
# ... 200 líneas más de código mezclado


# ✅ BIEN (Nuevo): Notebook solo orquesta
from src.extractors import EurostatExtractor

extractor = EurostatExtractor()
indicadores = extractor.extraer_todos_los_indicadores()
extractor.guardar_cache()

# Notebook se enfoca en:
# 1. Importar clases
# 2. Ejecutar métodos
# 3. Mostrar resultados
# 4. Validar visualmente
```

---

## 🔄 Flujo de Datos

### Pipeline Completo

```
┌─────────────────┐
│ API Eurostat    │
│ (SDMX-JSON)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ EurostatExtractor.extraer_*()   │
│ ─────────────────────────────── │
│ • fetch_api_data()              │
│ • parsear_eurostat_sdmx()       │
│   - Filter: age='TOTAL'         │
│   - Filter: sex='T'             │
│ • validar_dataframe()           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ IndicadorEurostat               │
│ (Value Object)                  │
│ ─────────────────────────────── │
│ • df_espana (10 registros)      │
│ • df_ue27 (10 registros)        │
│ • df_ranking (365 registros)    │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ EurostatExtractor.guardar_cache()│
│ ─────────────────────────────── │
│ • guardar_pickle() × 14 veces   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ outputs/pickle_cache/           │
│ • df_gini_es.pkl                │
│ • df_gini_ue27.pkl              │
│ • df_gini_todos.pkl  (Ranking)  │
│ • ... (11 más)                  │
└─────────────────────────────────┘
```

---

## 🧪 Testing

### Estrategia de Tests

```python
# tests/test_eurostat_extractor.py

def test_parsear_eurostat_sdmx_filtra_age():
    """Verifica que parsear_eurostat_sdmx filtra age='TOTAL' correctamente"""
    # Mock de datos con age='TOTAL' y age='Y_LT18'
    data_mock = {...}
    
    df = parsear_eurostat_sdmx(data_mock, 'Gini', filter_age='TOTAL')
    
    # No debe haber columna 'age' en resultado
    assert 'age' not in df.columns
    
    # No debe haber duplicados
    assert not df.duplicated().any()


def test_eurostat_extractor_gini():
    """Verifica que extractor de Gini funciona correctamente"""
    extractor = EurostatExtractor()
    gini = extractor.extraer_indicador('Gini')
    
    # España debe tener ~10 registros
    assert 8 <= len(gini.df_espana) <= 12
    
    # Ranking debe tener columnas correctas
    assert set(gini.df_ranking.columns) == {'Gini', 'geo_code', 'geo_name', 'Año'}
    
    # NO debe tener columnas age/sex
    assert 'age' not in gini.df_ranking.columns
    assert 'sex' not in gini.df_ranking.columns
```

---

## 📊 Comparativa: Antiguo vs Nuevo

### Código Antiguo (Monolítico)

```python
# ❌ 2824 líneas en 1 notebook
# ❌ Funciones mezcladas con ejecución
# ❌ Sin clases reutilizables
# ❌ Configuración hardcodeada
# ❌ Sin tests
# ❌ Difícil debugging

# Línea 1400: Definir función
def parsear_eurostat_sdmx(...):
    ...

# Línea 1583: Usar función
df_gini = parsear_eurostat_sdmx(...)

# Línea 2745: Diccionario de carga (PRIMERA definición)
dataframes_a_cargar = {
    'EUROSTAT_Gini_Ranking': df_gini_todos,
    # ... 28 tablas
}

# Línea 3227: Diccionario de carga (SEGUNDA definición - BUG!)
dataframes_a_cargar = {  # ❌ Sobreescribe el anterior!
    'EUROSTAT_Gini_Espana': df_gini_es,
    # ... solo 24 tablas, SIN Ranking
}
```

### Código Nuevo (Profesional)

```python
# ✅ src/: Código reutilizable y testeable
# ✅ notebooks/: Solo orquestación
# ✅ config.py: Configuración centralizada
# ✅ Clases bien diseñadas
# ✅ Tests unitarios
# ✅ Fácil debugging

# src/config.py - Configuración
EUROSTAT_DATASETS = {
    'Gini': {...},
    'AROP': {...},
    ...
}

# src/extractors/eurostat_extractor.py - Lógica
class EurostatExtractor:
    def extraer_todos_los_indicadores(self):
        ...

# notebooks/01b_extract_EUROSTAT_v2.ipynb - Orquestación
from src.extractors import EurostatExtractor

extractor = EurostatExtractor()
indicadores = extractor.extraer_todos_los_indicadores()
extractor.guardar_cache()
```

---

## 🎯 Beneficios de la Nueva Arquitectura

### 1. **Mantenibilidad** 📈
- Cambios localizados (un cambio en `config.py` afecta todo el sistema)
- Código organizado por responsabilidad
- Fácil encontrar bugs

### 2. **Reutilización** ♻️
- `EurostatExtractor` usable desde cualquier notebook o script
- `utils.py` con funciones importables
- No duplicar código

### 3. **Testabilidad** 🧪
- Clases y funciones pequeñas y testeables
- Tests unitarios aislados
- Mock de APIs para tests rápidos

### 4. **Escalabilidad** 🚀
- Fácil agregar nuevos extractores (ej: `ONUExtractor`)
- Fácil agregar nuevos indicadores
- Fácil cambiar de base de datos (MySQL, PostgreSQL)

### 5. **Documentación** 📖
- Docstrings en todas las funciones/clases
- Type hints para autocompletado
- Ejemplos de uso en docstrings

---

## 🔮 Próximos Pasos

### Fase 1: Completar Extractores ✅ (En progreso)
- [x] `EurostatExtractor` - Completado
- [ ] `INEExtractor` - Clase para extraer datos INE
- [ ] Tests unitarios para extractores

### Fase 2: Loader Profesional
- [ ] `SQLRepository` - Clase para operaciones SQL
- [ ] Transacciones atómicas
- [ ] Validación pre-carga

### Fase 3: Orquestación
- [ ] `ETLPipeline` - Clase orquestadora principal
- [ ] Manejo de errores robusto
- [ ] Logs estructurados (JSON)

### Fase 4: CI/CD
- [ ] GitHub Actions para tests automáticos
- [ ] Pre-commit hooks
- [ ] Coverage >80%

---

**Autor**: Proyecto Desigualdad Social ETL  
**Versión**: 2.0.0  
**Fecha**: 2025-11-15
