# Desigualdad Social en España - Pipeline ETL

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 📖 Descripción

Pipeline ETL modular y profesional para análisis de desigualdad social en España. Extrae, transforma, valida y carga **30 tablas** desde el INE (Instituto Nacional de Estadística) y EUROSTAT en SQL Server, garantizando reproducibilidad y trazabilidad completa.

**Características principales:**
- ✅ **Reproducible**: Configuración centralizada con `.env`, scripts automatizados
- ✅ **Validado**: Framework de validación con logs automáticos (JSON/CSV)
- ✅ **Modular**: Separación clara entre extracción, transformación, carga y validación
- ✅ **Documentado**: Diccionario de datos completo, decisiones metodológicas explícitas
- ✅ **Profesional**: Arquitectura limpia, control de versiones, buenas prácticas científicas

**Indicadores analizados:** AROPE, AROP, Gini, S80/S20, Carencia Material, Renta Media, IPC, Población

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.11+
- SQL Server (local o remoto)
- ODBC Driver 17 for SQL Server

### 2. Configuración del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Desigualdad-en-España.git
cd Desigualdad-en-España

# Crear entorno virtual
python -m venv desigualdad
source desigualdad/bin/activate  # Linux/Mac
# o
desigualdad\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración de la Base de Datos

**Importante**: Este proyecto usa variables de entorno para la configuración de la base de datos.

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita `.env` con tu configuración local:
   ```bash
   # Para Windows con autenticación integrada
   DB_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=desigualdad;Trusted_Connection=yes;
   
   # Para SQL Server con usuario y contraseña
   DB_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=desigualdad;UID=tu_usuario;PWD=tu_contraseña;
   ```

3. **Nunca subas tu archivo `.env` al repositorio** - está excluido en `.gitignore`

### ODBC Driver en Windows (Chocolatey)

Si trabajas en Windows y usas runners `windows-latest` en GitHub Actions, puedes instalar el ODBC Driver para SQL Server con Chocolatey:

```powershell
choco install sqlserver-odriver -y --no-progress
```

En el workflow de CI hemos añadido un paso para instalar el driver en runners Windows y verificar que `pyodbc` detecta el driver.

## 📂 Estructura del Proyecto

```
desigualdad_social_etl/
├── notebooks/
│   ├── 00_etl/                              # Pipeline ETL y validación
│   │   ├── 01a_extract_transform_INE.ipynb      # Extracción INE (13 fuentes → 16 tablas)
│   │   ├── 01b_extract_transform_EUROSTAT.ipynb # Extracción Eurostat (API SDMX → 14 tablas)
│   │   ├── 01c_load_to_sql.ipynb                # Carga a SQL Server (30 tablas)
│   │   ├── 02a_validacion_INE.ipynb             # Validación calidad INE
│   │   ├── 02b_validacion_EUROSTAT.ipynb        # Validación calidad Eurostat
│   │   ├── 02c_validacion_integracion.ipynb     # Validación coherencia INE↔EUROSTAT
│   │   ├── 01_run_etl.py                        # Orquestador ETL automatizado
│   │   └── 02_run_validation.py                 # Orquestador validación automatizado
│   ├── 01_analisis_nacional/                # [Futuros notebooks de análisis]
│   ├── 02_analisis_regional/                # [Futuros notebooks de análisis]
│   └── 03_comparativa_europa/               # [Futuros notebooks de análisis]
├── docs/
│   ├── DICCIONARIO_DATOS.md             # 📚 REFERENCIA COMPLETA: 30 tablas, variables, fuentes
│   ├── ARQUITECTURA.md                  # Diseño técnico del pipeline
│   └── RESUMEN_TRANSFORMACION.md        # Transformaciones aplicadas
├── utils/
│   ├── config.py                        # Configuración global (carga .env)
│   ├── validation_framework.py          # Framework validación automática
│   └── validation_rules.py              # Reglas de validación por tabla
├── data/
│   └── validated/
│       └── logs/                        # Logs de validación (CSV/JSON timestamped)
├── outputs/
│   ├── pickle_cache/                    # Cache intermedio (excluido del repo)
│   ├── figuras/                         # Gráficos generados
│   └── tablas/                          # Tablas exportadas (CSV/Excel)
├── .env.example                         # Plantilla de configuración
├── .env                                 # Configuración local (NO SUBIR A GIT)
├── .gitignore                           # Excluye .env, logs, cache
├── requirements.txt                     # Dependencias Python
└── README.md                            # Este archivo
```

**📚 Documentación clave:**
- **`docs/DICCIONARIO_DATOS.md`** ← Consulta aquí todas las tablas, variables y decisiones metodológicas
- **`docs/ARQUITECTURA.md`** ← Diseño técnico del pipeline
- **`notebooks/00_etl/README_ETL.md`** ← Guía detallada del ETL

## 🔄 Uso del Pipeline

### Ejecución Manual (Notebooks)

1. **Extracción y transformación**:
   - Ejecuta `01a_extract_transform_INE.ipynb`
   - Ejecuta `01b_extract_transform_EUROSTAT.ipynb`
   - Ejecuta `01c_load_to_sql.ipynb`

2. **Validación**:
   - Ejecuta `02a_validacion_INE.ipynb`
   - Ejecuta `02b_validacion_EUROSTAT.ipynb`
   - Ejecuta `02c_validacion_integracion.ipynb`

### Ejecución Automatizada (Scripts)

```bash
cd notebooks/00_etl

# Ejecutar pipeline ETL completo (extracción, transformación, carga)
python 01_run_etl.py

# Ejecutar pipeline de validación completo
python 02_run_validation.py
```

### CI / GitHub Actions

Para que la ejecución automática en GitHub Actions pueda ejecutar la carga a SQL Server y las validaciones que requieren base de datos, debes configurar las credenciales como secretos en el repositorio:

1. Ve a _Settings_ → _Secrets and variables_ → _Actions_ en GitHub.
2. Crea un nuevo secret con nombre: `DB_CONNECTION_STRING` y como valor pon la cadena ODBC (ej.: `DRIVER={ODBC Driver 17 for SQL Server};SERVER=mi-servidor;DATABASE=desigualdad;UID=usuario;PWD=contraseña;`).

Nota: si no defines `DB_CONNECTION_STRING` en los secrets, el pipeline **no fallará**: el paso de Carga SQL (`01c_load_to_sql`) será omitido en CI y la validación basada en BD no se ejecutará. Esto es útil para Pull Requests y pruebas sin credenciales.

La pipeline sube por defecto los artefactos generados (pickles) al final del job para depuración. Estos se almacenan temporalmente por 3 días y están disponibles en la interfaz de Actions si quieres descargarlos y revisarlos.

## 📊 Tablas Generadas (30 Total)

**Consulta [`docs/DICCIONARIO_DATOS.md`](docs/DICCIONARIO_DATOS.md) para documentación completa de cada tabla.**

### INE (16 tablas finales)
| Tabla | Descripción | Periodo |
|-------|-------------|---------|
| `INE_AROPE_CCAA` | AROPE por Comunidad Autónoma | 2008-2023 |
| `INE_AROPE_Edad_Sexo` | AROPE por edad y sexo | 2008-2023 |
| `INE_AROPE_Hogar` | **AROP** por tipo de hogar *(usado en validación)* | 2008-2023 |
| `INE_AROPE_Laboral` | AROPE por situación laboral | 2008-2023 |
| `INE_Carencia_Material_Decil` | Carencia material por decil | 2013-2023 |
| `INE_Gasto_Medio_Quintil_EPF` | Gasto medio por quintil (EPF) | 2008-2023 |
| `INE_Gini_S80S20_CCAA` | **Gini y S80/S20** por CCAA *(validado vs EUROSTAT)* | 2008-2023 |
| `INE_IPC_General` | IPC nacional (base 2021=100) | 2008-2023 |
| `INE_IPC_Sectorial_ECOICOP` | IPC por grupos de consumo | 2008-2023 |
| `INE_Poblacion_CCAA` | Población por CCAA, edad, sexo | 2008-2023 |
| `INE_Poblacion_Edad_Sexo_Nacionalidad` | Población por edad, sexo, nacionalidad | 2008-2023 |
| `INE_Renta_Media_Decil` | Renta media por decil | 2008-2023 |
| `INE_Umbral_Pobreza_Hogar` | Umbral de pobreza por tipo hogar | 2008-2023 |
| *+ 3 tablas adicionales INE* | | |

### EUROSTAT (14 tablas finales)
| Tabla | Descripción | Periodo |
|-------|-------------|---------|
| `EUROSTAT_AROP_Espana` | **AROP** España *(coherencia con INE validada)* | 2010-2023 |
| `EUROSTAT_AROP_Ranking` | AROP todos los países UE | 2010-2023 |
| `EUROSTAT_AROP_UE27` | AROP promedio UE27 | 2010-2023 |
| `EUROSTAT_Brecha_Pobreza_Espana` | Brecha relativa de pobreza España | 2010-2023 |
| `EUROSTAT_Brecha_Pobreza_Ranking` | Brecha todos los países | 2010-2023 |
| `EUROSTAT_Brecha_Pobreza_UE27` | Brecha promedio UE27 | 2010-2023 |
| `EUROSTAT_Gini_Espana` | **Gini** España *(coherencia con INE validada)* | 2010-2023 |
| `EUROSTAT_Gini_Ranking` | Gini todos los países | 2010-2023 |
| `EUROSTAT_Gini_UE27` | Gini promedio UE27 | 2010-2023 |
| `EUROSTAT_S80S20_Espana` | **S80/S20** España *(coherencia con INE validada)* | 2010-2023 |
| `EUROSTAT_S80S20_Ranking` | S80/S20 todos los países | 2010-2023 |
| `EUROSTAT_S80S20_UE27` | S80/S20 promedio UE27 | 2010-2023 |
| *+ 2 tablas adicionales EUROSTAT* | | |

**✅ Validación INE ↔ EUROSTAT:**
- **AROP:** Coherencia perfecta (<0.5% diferencia)
- **Gini:** Coherencia perfecta (<0.5% diferencia)  
- **S80/S20:** Coherencia excelente (<3% diferencia, atribuible a redondeo)

Ver `data/validated/logs/` para reportes completos.

## 🔍 Sistema de Validación

El framework de validación verifica:
- **Esquema**: Columnas esperadas y tipos de datos
- **Unicidad**: Claves primarias sin duplicados
- **Calidad**: Valores nulos, outliers, rangos esperados
- **Coherencia temporal**: Variaciones año a año
- **Integridad referencial**: Consistencia entre tablas INE/Eurostat

Los logs se guardan en `data/validated/logs/` (formato CSV y JSON).

## 🛠️ Mantenimiento y Actualización

### Actualizar datos periódicamente

```bash
cd notebooks/00_etl
python 01_run_etl.py       # Extrae nuevos datos
python 02_run_validation.py # Valida calidad
```

### Limpiar base de datos

```bash
python limpiar_db.py  # Elimina todas las tablas del proyecto
```

## 📝 Documentación Adicional

### Documentación Técnica del Pipeline
- **[`docs/DICCIONARIO_DATOS.md`](docs/DICCIONARIO_DATOS.md)** - 📚 **REFERENCIA PRINCIPAL:** Todas las tablas, variables, fuentes y decisiones metodológicas
- **[`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md)** - Diseño técnico del pipeline y arquitectura modular
- **[`docs/RESUMEN_TRANSFORMACION.md`](docs/RESUMEN_TRANSFORMACION.md)** - Transformaciones aplicadas a los datos
- **`notebooks/00_etl/README_ETL.md`** - Guía detallada del ETL
- **`notebooks/00_etl/README_PIPELINE_MODULAR.md`** - Arquitectura modular del pipeline
- **`notebooks/00_etl/README_VALIDACION.md`** - Sistema de validación y logs

### 🆕 Documentación de Calidad y Coherencia Analítica
- **[`docs/INFORME_COHERENCIA_ANALITICA.md`](docs/INFORME_COHERENCIA_ANALITICA.md)** - Análisis completo de 7 issues críticos de calidad de datos (P0-P4)
- **[`docs/METODOLOGIA_DEFLACION.md`](docs/METODOLOGIA_DEFLACION.md)** - Especificación de valores nominales/reales, fórmulas de deflación, base IPC 2021
- **[`docs/BREAKS_METODOLOGICOS.md`](docs/BREAKS_METODOLOGICOS.md)** - Rupturas en series temporales (EU-SILC 2013, COVID 2020-2021, cambio base IPC)
- **[`docs/CAVEATS_INCERTIDUMBRE.md`](docs/CAVEATS_INCERTIDUMBRE.md)** - Guía de niveles de confianza para conclusiones (sin intervalos de confianza publicados)

**Para entender el proyecto, comienza por:**
1. Este README (visión general)
2. [`docs/DICCIONARIO_DATOS.md`](docs/DICCIONARIO_DATOS.md) (tablas y decisiones metodológicas)
3. [`docs/INFORME_COHERENCIA_ANALITICA.md`](docs/INFORME_COHERENCIA_ANALITICA.md) (calidad y limitaciones)
4. Notebooks en `notebooks/00_etl/` (implementación)

## ✅ Checklist de Revisión y Validación del Proyecto

### 📋 Antes de Usar los Datos en Análisis

- [ ] **Pipeline ETL ejecutado completamente**
  - [ ] `01a_extract_transform_INE.ipynb` ejecutado sin errores
  - [ ] `01b_extract_transform_EUROSTAT.ipynb` ejecutado sin errores
  - [ ] `01c_load_to_sql.ipynb` ejecutado - 30 tablas cargadas en SQL Server
  - [ ] Verificar que `outputs/pickle_cache/` contiene 28 archivos pickle

- [ ] **Validación completada exitosamente**
  - [ ] `02a_validacion_INE.ipynb` ejecutado - sin errores críticos
  - [ ] `02b_validacion_EUROSTAT.ipynb` ejecutado - sin errores críticos
  - [ ] `02c_validacion_integracion.ipynb` ejecutado - coherencia INE↔EUROSTAT confirmada
  - [ ] Logs de validación disponibles en `data/validated/logs/`
  - [ ] Revisar reportes JSON/CSV: 0 errores críticos, warnings justificados

- [ ] **Base de datos SQL Server**
  - [ ] Conexión `.env` configurada correctamente
  - [ ] 30 tablas creadas (16 INE + 14 EUROSTAT)
  - [ ] Query de prueba: `SELECT COUNT(*) FROM INE_Gini_S80S20_CCAA` devuelve datos

- [ ] **Coherencia de datos validada**
  - [ ] AROP INE vs EUROSTAT: diferencia <0.5% ✅
  - [ ] Gini INE vs EUROSTAT: diferencia <0.5% ✅
  - [ ] S80/S20 INE vs EUROSTAT: diferencia <3% ✅
  - [ ] Sin valores nulos inesperados en columnas clave
  - [ ] Rango temporal coherente (INE: 2008-2023, EUROSTAT: 2010-2023)

### 📊 Antes de Publicar un Notebook de Análisis

- [ ] **Documentación del notebook**
  - [ ] Cabecera completa (nombre, objetivo, fuentes, fecha, autor)
  - [ ] Contexto e hipótesis/preguntas de investigación claramente definidos
  - [ ] Referencias a `docs/DICCIONARIO_DATOS.md` cuando sea relevante

- [ ] **Calidad del código**
  - [ ] Notebook ejecutable de principio a fin sin errores
  - [ ] Celdas markdown explican el "por qué" de cada paso
  - [ ] Comentarios en código complejo o no obvio
  - [ ] Variables con nombres descriptivos

- [ ] **Validación de datos en el notebook**
  - [ ] Verificar coherencia de datos cargados (ej: merge INE-EUROSTAT)
  - [ ] Documentar decisiones metodológicas (ej: "usar INE por serie más larga")
  - [ ] Identificar y documentar outliers o anomalías

- [ ] **Visualizaciones**
  - [ ] Gráficos con títulos descriptivos
  - [ ] Ejes con etiquetas claras (unidades, años, etc.)
  - [ ] Leyendas cuando hay múltiples series
  - [ ] Guardados en `outputs/figuras/` con nombres descriptivos

- [ ] **Contextualización histórica**
  - [ ] Eventos relevantes marcados (crisis 2008, COVID-19, etc.)
  - [ ] Interpretación de cambios bruscos en los datos
  - [ ] Comparación con periodos anteriores cuando sea relevante

- [ ] **Conclusiones**
  - [ ] Hallazgos principales con **evidencia numérica específica** (no solo "aumentó", sino "aumentó X%")
  - [ ] Limitaciones metodológicas y de datos explícitas
  - [ ] Próximos pasos y análisis sugeridos

### 🔍 Revisión Manual Independiente

- [ ] **Primera revisión (por el autor)**
  - [ ] Re-ejecutar todo el notebook en kernel limpio
  - [ ] Verificar que todas las cifras son correctas
  - [ ] Revisar coherencia narrativa entre celdas markdown

- [ ] **Segunda revisión (idealmente por otra persona)**
  - [ ] Código comprensible sin necesidad de explicación verbal
  - [ ] Gráficos auto-explicativos
  - [ ] Conclusiones justificadas por los datos mostrados

- [ ] **Tercera revisión (validación final)**
  - [ ] Comparar resultados clave con fuentes oficiales (INE, EUROSTAT)
  - [ ] Verificar que no hay contradicciones con análisis anteriores
  - [ ] Confirmar que el análisis responde a las preguntas de investigación planteadas

### 📤 Antes de Commit y Push a GitHub

- [ ] **Archivos a incluir**
  - [ ] Notebooks de análisis (.ipynb)
  - [ ] Gráficos generados (`outputs/figuras/`)
  - [ ] Documentación actualizada (README, diccionario si aplica)
  - [ ] Requirements.txt actualizado si se añadieron librerías

- [ ] **Archivos a EXCLUIR (verificar .gitignore)**
  - [ ] `.env` (configuración sensible)
  - [ ] `outputs/pickle_cache/` (cache intermedio, muy pesado)
  - [ ] `data/validated/logs/` con timestamps específicos (opcional: subir solo últimos)
  - [ ] `__pycache__/` y archivos `.pyc`

- [ ] **Mensaje de commit descriptivo**
  - [ ] Formato: `tipo: descripción breve`
  - [ ] Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - [ ] Ejemplo: `feat: Añadir análisis evolución Gini 2008-2023`

### 🎯 Checklist de Reproducibilidad

**Otro investigador debería poder:**

- [ ] Clonar el repositorio
- [ ] Configurar `.env` con su propia base de datos
- [ ] Ejecutar `pip install -r requirements.txt`
- [ ] Ejecutar `python 01_run_etl.py` y `python 02_run_validation.py`
- [ ] Reproducir exactamente las **mismas 30 tablas** en SQL Server
- [ ] Ejecutar cualquier notebook de análisis y obtener **las mismas conclusiones**
- [ ] Entender **todas las decisiones metodológicas** leyendo la documentación

**Si alguno de estos pasos falla, el proyecto NO es reproducible. Corregir antes de publicar.**

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🔒 Seguridad y Privacidad

- **Nunca** incluyas credenciales en el código
- Usa siempre el archivo `.env` para configuración sensible
- El `.env` está excluido del repositorio vía `.gitignore`
- Los datos públicos de INE y Eurostat son de acceso libre

## 📧 Contacto y Contribuciones

**Autor:** Mario (databamario)  
**Repositorio:** [github.com/databamario/Desigualdad-Espana](https://github.com/databamario/Desigualdad-Espana)  
**Fecha de creación:** Noviembre 2025

Para preguntas, sugerencias o reportar problemas, abre un issue en GitHub.
