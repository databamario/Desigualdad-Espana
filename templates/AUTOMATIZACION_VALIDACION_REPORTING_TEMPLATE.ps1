# Script PowerShell para automatizar validación y generación de reportes
# Ejecuta el script de validación automática y genera un reporte de warnings
# Adaptar rutas y nombres de archivos según el proyecto

$env:PYTHONPATH = "$PWD\templates"
python templates/VALIDACION_AUTOMATICA_TEMPLATE.py
# Suponiendo que el script exporta warnings a warnings.csv
if (Test-Path warnings.csv) {
    Write-Host "Warnings generados:"
    Get-Content warnings.csv
} else {
    Write-Host "No se generaron warnings."
}
