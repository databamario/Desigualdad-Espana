# Makefile para Pipeline de Análisis de Desigualdad en España
# Uso: make all (ejecuta todo el pipeline)

PYTHON = python
JUPYTER = jupyter nbconvert --to notebook --execute --inplace

# Directorios
DATA_PROCESSED = data/processed
DATA_VALIDATED = data/validated
OUTPUTS = outputs

# Archivos intermedios
DF_LIMPIO = $(DATA_PROCESSED)/df_limpio.parquet
VALIDATION_REPORT = $(DATA_VALIDATED)/validation_report.txt
RESULTS_GINI = $(OUTPUTS)/resultados_gini_s80s20.parquet
RESULTS_INFLACION = $(OUTPUTS)/resultados_inflacion_diferencial.parquet

.PHONY: all clean etl validate analyze report help

# Pipeline completo
all: etl validate analyze report
	@echo "✅ Pipeline completo ejecutado"

# Paso 1: ETL y preparación de datos
etl: $(DF_LIMPIO)
$(DF_LIMPIO): notebooks/00_etl/*.py
	@echo "🔄 Ejecutando ETL..."
	cd notebooks/00_etl && $(PYTHON) 01_run_etl.py
	@echo "✅ ETL completado - Datos limpios guardados en $(DF_LIMPIO)"

# Paso 2: Validación de datos
validate: $(VALIDATION_REPORT)
$(VALIDATION_REPORT): $(DF_LIMPIO)
	@echo "🔍 Validando datos..."
	$(JUPYTER) notebooks/01_analisis_nacional/01_validacion_datos.ipynb
	@echo "✅ Validación completada"

# Paso 3: Análisis principales
analyze: $(RESULTS_GINI) $(RESULTS_INFLACION)

$(RESULTS_GINI): $(DF_LIMPIO) $(VALIDATION_REPORT)
	@echo "📊 Ejecutando análisis de Gini, S80/S20, AROPE..."
	$(JUPYTER) notebooks/01_analisis_nacional/02_analisis_indicadores_principales.ipynb
	@echo "✅ Análisis principales completados"

$(RESULTS_INFLACION): $(DF_LIMPIO) $(VALIDATION_REPORT)
	@echo "📈 Ejecutando análisis de inflación diferencial..."
	$(JUPYTER) notebooks/01_analisis_nacional/03_analisis_inflacion_diferencial.ipynb
	@echo "✅ Análisis de inflación completado"

# Paso 4: Reporte final
report: $(RESULTS_GINI) $(RESULTS_INFLACION)
	@echo "📄 Generando reporte final..."
	$(JUPYTER) notebooks/01_analisis_nacional/99_reporte_final.ipynb
	@echo "✅ Reporte generado en notebooks/01_analisis_nacional/99_reporte_final.ipynb"

# Limpiar archivos intermedios
clean:
	@echo "🗑️  Limpiando archivos intermedios..."
	rm -f $(DF_LIMPIO) $(VALIDATION_REPORT) $(RESULTS_GINI) $(RESULTS_INFLACION)
	@echo "✅ Limpieza completada"

# Limpiar todo (incluye outputs)
clean-all: clean
	@echo "🗑️  Limpiando todos los outputs..."
	rm -rf $(OUTPUTS)/*
	@echo "✅ Limpieza total completada"

# Ayuda
help:
	@echo "Pipeline de Análisis de Desigualdad en España"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make all       - Ejecuta todo el pipeline (ETL -> Validación -> Análisis -> Reporte)"
	@echo "  make etl       - Solo ejecuta ETL y preparación de datos"
	@echo "  make validate  - Solo ejecuta validación de datos"
	@echo "  make analyze   - Solo ejecuta análisis (Gini, AROPE, Inflación)"
	@echo "  make report    - Solo genera el reporte final"
	@echo "  make clean     - Limpia archivos intermedios"
	@echo "  make clean-all - Limpia todo (intermedios + outputs)"
	@echo "  make help      - Muestra esta ayuda"
