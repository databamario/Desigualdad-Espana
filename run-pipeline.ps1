# Pipeline de Análisis de Desigualdad en España
# Script de orquestación para Windows PowerShell

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

$PYTHON = "C:/Users/mario/Desktop/Projects/desigualdad_social_etl/desigualdad/Scripts/python.exe"
$JUPYTER = "jupyter"

# Directorios
$DATA_PROCESSED = "data/processed"
$DATA_VALIDATED = "data/validated"
$OUTPUTS = "outputs"

# Archivos intermedios
$DF_LIMPIO = "$DATA_PROCESSED/df_limpio.parquet"
$VALIDATION_REPORT = "$DATA_VALIDATED/validation_report.txt"
$RESULTS_GINI = "$OUTPUTS/resultados_gini_s80s20.parquet"
$RESULTS_INFLACION = "$OUTPUTS/resultados_inflacion_diferencial.parquet"

function Show-Help {
    Write-Host "`nPipeline de Análisis de Desigualdad en España" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "`nComandos disponibles:" -ForegroundColor Yellow
    Write-Host "  .\run-pipeline.ps1 all       - Ejecuta todo el pipeline (ETL -> Validación -> Análisis -> Reporte)"
    Write-Host "  .\run-pipeline.ps1 etl       - Solo ejecuta ETL y preparación de datos"
    Write-Host "  .\run-pipeline.ps1 validate  - Solo ejecuta validación de datos"
    Write-Host "  .\run-pipeline.ps1 analyze   - Solo ejecuta análisis (Gini, AROPE, Inflación)"
    Write-Host "  .\run-pipeline.ps1 report    - Solo genera el reporte final"
    Write-Host "  .\run-pipeline.ps1 test      - Ejecuta tests unitarios"
    Write-Host "  .\run-pipeline.ps1 clean     - Limpia archivos intermedios"
    Write-Host "  .\run-pipeline.ps1 clean-all - Limpia todo (intermedios + outputs)"
    Write-Host "  .\run-pipeline.ps1 help      - Muestra esta ayuda`n"
}

function Run-ETL {
    Write-Host "`n🔄 Ejecutando ETL..." -ForegroundColor Cyan
    Push-Location notebooks/00_etl
    & $PYTHON 01_run_etl.py
    Pop-Location
    Write-Host "✅ ETL completado - Datos limpios guardados en $DF_LIMPIO" -ForegroundColor Green
}

function Run-Validate {
    Write-Host "`n🔍 Validando datos..." -ForegroundColor Cyan
    if (-not (Test-Path $DF_LIMPIO)) {
        Write-Host "❌ Error: $DF_LIMPIO no encontrado. Ejecuta primero: .\run-pipeline.ps1 etl" -ForegroundColor Red
        exit 1
    }
    jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_nacional/01_validacion_datos.ipynb
    Write-Host "✅ Validación completada" -ForegroundColor Green
}

function Run-Analyze {
    Write-Host "`n📊 Ejecutando análisis..." -ForegroundColor Cyan
    if (-not (Test-Path $DF_LIMPIO)) {
        Write-Host "❌ Error: $DF_LIMPIO no encontrado. Ejecuta primero: .\run-pipeline.ps1 etl" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  📈 Análisis de Gini, S80/S20, AROPE..." -ForegroundColor Yellow
    jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_nacional/02_analisis_indicadores_principales.ipynb
    
    Write-Host "  📉 Análisis de inflación diferencial..." -ForegroundColor Yellow
    jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_nacional/03_analisis_inflacion_diferencial.ipynb
    
    Write-Host "✅ Análisis completados" -ForegroundColor Green
}

function Run-Report {
    Write-Host "`n📄 Generando reporte final..." -ForegroundColor Cyan
    if (-not (Test-Path $RESULTS_GINI)) {
        Write-Host "❌ Error: Resultados no encontrados. Ejecuta primero: .\run-pipeline.ps1 analyze" -ForegroundColor Red
        exit 1
    }
    jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_nacional/99_reporte_final.ipynb
    Write-Host "✅ Reporte generado" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "`n🧪 Ejecutando tests..." -ForegroundColor Cyan
    & $PYTHON -m pytest -v
    Write-Host "✅ Tests completados" -ForegroundColor Green
}

function Clean-Intermediate {
    Write-Host "`n🗑️  Limpiando archivos intermedios..." -ForegroundColor Cyan
    if (Test-Path $DF_LIMPIO) { Remove-Item $DF_LIMPIO }
    if (Test-Path $VALIDATION_REPORT) { Remove-Item $VALIDATION_REPORT }
    if (Test-Path $RESULTS_GINI) { Remove-Item $RESULTS_GINI }
    if (Test-Path $RESULTS_INFLACION) { Remove-Item $RESULTS_INFLACION }
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Clean-All {
    Clean-Intermediate
    Write-Host "`n🗑️  Limpiando todos los outputs..." -ForegroundColor Cyan
    if (Test-Path $OUTPUTS) { Remove-Item -Recurse -Force "$OUTPUTS/*" }
    Write-Host "✅ Limpieza total completada" -ForegroundColor Green
}

function Run-All {
    Write-Host "`n🚀 Ejecutando pipeline completo..." -ForegroundColor Cyan
    Run-ETL
    Run-Validate
    Run-Analyze
    Run-Report
    Write-Host "`n✅ Pipeline completo ejecutado" -ForegroundColor Green
}

# Ejecutar comando
switch ($Command.ToLower()) {
    "all" { Run-All }
    "etl" { Run-ETL }
    "validate" { Run-Validate }
    "analyze" { Run-Analyze }
    "report" { Run-Report }
    "test" { Run-Tests }
    "clean" { Clean-Intermediate }
    "clean-all" { Clean-All }
    "help" { Show-Help }
    default {
        Write-Host "❌ Comando desconocido: $Command" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
