# 🚀 Guía de Ejecución del Pipeline de Análisis

## Arquitectura de 3 Capas

Este proyecto sigue una arquitectura modular de 3 capas:

```
0. ETL (Ingeniería) → 1. Validación → 2. Análisis → 3. Reporte
```

## Ejecución Rápida

### Ejecutar todo el pipeline

```bash
make all
```

Esto ejecutará en orden:
1. ETL y preparación de datos
2. Validación de calidad
3. Análisis de indicadores (Gini, AROPE, Inflación)
4. Generación del reporte final

### Ejecutar pasos individuales

```bash
# Solo ETL
make etl

# Solo validación
make validate

# Solo análisis
make analyze

# Solo reporte
make report
```

## Estructura de Archivos Intermedios

```
data/
  ├── processed/
  │   └── df_limpio.parquet          # DataFrame limpio (salida de ETL)
  ├── validated/
  │   └── validation_report.txt      # Reporte de validación
outputs/
  ├── resultados_gini_s80s20.parquet # Resultados de análisis principal
  ├── resultados_inflacion_diferencial.parquet
  └── figuras/                       # Gráficos generados
```

## Esquema de Datos

Ver `config/schema.yaml` para la especificación completa del DataFrame limpio.

Columnas principales:
- `Año`: Año de observación (2008-2023)
- `Gini`: Coeficiente de Gini
- `S80S20`: Ratio renta ricos/pobres
- `AROPE_%`: Tasa de riesgo de pobreza
- `Umbral_Real_€_Base`: Umbral ajustado por inflación

## Tests Automáticos

### Ejecutar tests

```bash
# Todos los tests
pytest

# Solo tests unitarios rápidos
pytest -m unit

# Con cobertura
pytest --cov=src --cov-report=html
```

### Tests disponibles

- **Deflactación**: Verifica cálculo correcto de valores reales
- **Validación**: Comprueba detección de nulos y rangos
- **Indicadores**: Valida cálculo de Gini, S80/S20, AROPE
- **Consistencia**: Verifica correlaciones entre indicadores
- **Integridad**: Comprueba continuidad temporal y ausencia de duplicados

## Notebooks por Capa

### Capa 0: ETL (00_etl/)
- `01_run_etl.py`: Script principal de extracción y transformación
- Salida: `data/processed/df_limpio.parquet`

### Capa 1: Validación
- `01_validacion_datos.ipynb`: Validación de calidad de datos
- Salida: `data/validated/validation_report.txt`

### Capa 2: Análisis
- `02_analisis_indicadores_principales.ipynb`: Gini, S80/S20, AROPE
- `03_analisis_inflacion_diferencial.ipynb`: Análisis detallado de inflación
- Salida: Archivos parquet en `outputs/`

### Capa 3: Reporte
- `99_reporte_final.ipynb`: Narrativa y visualización (sin cálculos)

## Actualización de Datos

Cuando los datos fuente cambien:

```bash
# Limpiar archivos intermedios
make clean

# Re-ejecutar todo el pipeline
make all
```

## Troubleshooting

### Error: "df_limpio.parquet no encontrado"
→ Ejecuta primero `make etl`

### Error: "Validación falló"
→ Revisa `data/validated/validation_report.txt` para detalles

### Tests fallan
→ Ejecuta `pytest -v` para ver detalles específicos

## Dependencias de Ejecución

Asegúrate de tener instalado:
- Python >= 3.9
- Paquetes: pandas, numpy, matplotlib, seaborn, pyarrow, pytest
- Jupyter Notebook

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Buenas Prácticas

✅ **Siempre ejecuta el pipeline completo** después de cambios en ETL
✅ **Revisa el reporte de validación** antes de confiar en los resultados
✅ **Ejecuta los tests** antes de hacer commit de cambios
✅ **Documenta** cualquier cambio en `config/schema.yaml` si modificas el esquema

## Contacto y Soporte

Para preguntas sobre el pipeline: consultar `docs/ARQUITECTURA.md`
