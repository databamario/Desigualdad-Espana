# Desigualdad Social en España - Pipeline ETL

## 📖 Descripción

Pipeline ETL modular para análisis de desigualdad social en España. Extrae datos del INE y Eurostat, los transforma, valida y carga en SQL Server para análisis.

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

## 📂 Estructura del Proyecto

```
desigualdad_social_etl/
├── notebooks/
│   └── 00_etl/
│       ├── 01a_extract_transform_INE.ipynb      # Extracción INE (16 tablas)
│       ├── 01b_extract_transform_EUROSTAT.ipynb # Extracción Eurostat (12 tablas)
│       ├── 01c_load_to_sql.ipynb                # Carga a SQL Server (28 tablas)
│       ├── 02a_validacion_INE.ipynb             # Validación INE
│       ├── 02b_validacion_EUROSTAT.ipynb        # Validación Eurostat
│       ├── 02c_validacion_integracion.ipynb     # Validación integración
│       ├── 01_run_etl.py                        # Orquestador ETL
│       └── 02_run_validation.py                 # Orquestador validación
├── utils/
│   ├── config.py                  # Configuración global (usa .env)
│   ├── validation_framework.py    # Framework de validación
│   └── validation_rules.py        # Reglas de validación por tabla
├── data/
│   └── validated/
│       └── logs/                  # Logs de validación (CSV/JSON)
├── outputs/
│   ├── pickle_cache/              # Cache intermedio (excluido del repo)
│   ├── figuras/                   # Gráficos generados
│   └── tablas/                    # Tablas exportadas
├── .env.example                   # Plantilla de configuración
├── .gitignore                     # Excluye .env, logs, cache
└── README.md                      # Este archivo
```

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

## 📊 Tablas Generadas

### INE (16 tablas)
- `INE_AROPE_CCAA`, `INE_AROPE_Edad_Sexo`, `INE_AROPE_Hogar`, `INE_AROPE_Laboral`
- `INE_Carencia_Material_Decil`, `INE_Gasto_Medio_Hogar_Quintil`
- `INE_Gini_S80S20_CCAA`, `INE_IPC_Nacional`, `INE_IPC_Sectorial_ECOICOP`
- `INE_Poblacion_Edad_Sexo_CCAA`, `INE_Poblacion_Edad_Sexo_Nacionalidad`
- `INE_Renta_Media_Decil`, `INE_Umbral_Pobreza_Hogar`

### Eurostat (12 tablas)
- `EUROSTAT_AROP_Espana`, `EUROSTAT_AROP_Ranking`, `EUROSTAT_AROP_UE27`
- `EUROSTAT_Brecha_Pobreza_Espana`, `EUROSTAT_Brecha_Pobreza_Ranking`, `EUROSTAT_Brecha_Pobreza_UE27`
- `EUROSTAT_Gini_Espana`, `EUROSTAT_Gini_Ranking`, `EUROSTAT_Gini_UE27`
- `EUROSTAT_Impacto_Redistributivo_Espana`, `EUROSTAT_Impacto_Redistributivo_UE27`
- `EUROSTAT_S80S20_Espana`, `EUROSTAT_S80S20_Ranking`, `EUROSTAT_S80S20_UE27`

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

- `notebooks/00_etl/README_ETL.md` - Guía detallada del ETL
- `notebooks/00_etl/README_PIPELINE_MODULAR.md` - Arquitectura modular
- `notebooks/00_etl/README_VALIDACION.md` - Sistema de validación

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

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.
