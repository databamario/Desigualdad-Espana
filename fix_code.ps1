# ============================================================================
# Script de CorrecciÃ³n AutomÃ¡tica de CÃ³digo - Desigualdad EspaÃ±a ETL
# ============================================================================
# Este script ejecuta automÃ¡ticamente todas las herramientas de calidad de cÃ³digo
# para corregir errores de estilo, formateo, imports y otros problemas detectables.
#
# Uso: .\fix_code.ps1
# ============================================================================

Write-Host "Iniciando correccion automatica de codigo..." -ForegroundColor Cyan
# Force UTF-8 output to avoid garbled characters on Windows PowerShell
chcp 65001 > $null
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
Write-Host ""

# Activar el entorno virtual si existe
$venvPath = ".\desigualdad\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & $venvPath
} else {
    # Evitar que la cadena termine con una barra invertida que rompa las comillas
    Write-Host "No se encontrÃ³ entorno virtual en .\desigualdad" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '1) INSTALANDO HERRAMIENTAS DE CALIDAD DE CODIGO' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""

# Asegurar que todas las herramientas estÃ©n instaladas
Write-Host "Instalando/actualizando herramientas necesarias..." -ForegroundColor Yellow
# Remove problematic optional package `types-pyodbc` and add `ruff` as fallback for style fixes
pip install --upgrade black isort autopep8 flake8 mypy ruff --quiet

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '2) EJECUTANDO AUTOPEP8 (Correccion de PEP8)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Corrigiendo errores de estilo con autopep8..." -ForegroundColor Yellow
Write-Host "   (E501: lÃ­neas largas, E402: imports fuera de lugar, etc.)" -ForegroundColor Gray
try {
    autopep8 --in-place --aggressive --aggressive --recursive --exclude="desigualdad/Lib/*,desigualdad/Scripts/*" . 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "autopep8 returned non-zero" }
} catch {
    Write-Host 'autopep8 fallo o no esta disponible; intentando ruff format --fix como alternativa...' -ForegroundColor Yellow
    # Ruff puede arreglar muchos problemas de estilo y es un buen fallback
    ruff format --fix . 2>&1 | Out-Null
}

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '3) EJECUTANDO BLACK (Formateo de codigo)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Formateando cÃ³digo con Black..." -ForegroundColor Yellow
black --exclude="desigualdad/|\.git/" .

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '4) EJECUTANDO ISORT (Ordenamiento de imports)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ordenando imports con isort..." -ForegroundColor Yellow
isort --skip=desigualdad --skip-glob="*/Lib/*" --skip-glob="*/Scripts/*" .

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '5) VERIFICANDO CON FLAKE8 (Analisis de codigo)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutando Flake8 para verificar el cÃ³digo..." -ForegroundColor Yellow
Write-Host "   (Solo se mostrarÃ¡n errores en archivos de tu proyecto)" -ForegroundColor Gray

# Ejecutar flake8 solo en tus archivos (excluyendo dependencias)
$flake8Output = flake8 --exclude=desigualdad/Lib,desigualdad/Scripts,.git,__pycache__ --extend-ignore=E203,W503 . 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "No se encontraron errores de Flake8" -ForegroundColor Green
} else {
    Write-Host "Flake8 encontrÃ³ algunos problemas:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host $flake8Output
    Write-Host ""
    Write-Host "Nota: Algunos errores pueden requerir correcciÃ³n manual." -ForegroundColor Gray
}

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '6) VERIFICANDO CON MYPY (Analisis de tipos)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutando MyPy para verificar tipado..." -ForegroundColor Yellow

# Ejecutar mypy solo en tus archivos
$mypyOutput = mypy --exclude="desigualdad/" --ignore-missing-imports . 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "No se encontraron errores de MyPy" -ForegroundColor Green
} else {
    Write-Host "MyPy encontrÃ³ algunos problemas:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host $mypyOutput
    Write-Host ""
    Write-Host "Nota: Errores de tipado pueden requerir anotaciones adicionales." -ForegroundColor Gray
}

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host '7) EJECUTANDO TESTS (Pytest)' -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutando tests con pytest..." -ForegroundColor Yellow

$pytestOutput = pytest --tb=short --ignore=desigualdad/Lib --ignore=desigualdad/Scripts 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Todos los tests pasaron" -ForegroundColor Green
} else {
    Write-Host "Algunos tests fallaron:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host $pytestOutput
    Write-Host ""
    Write-Host "Nota: Revisa los tests que fallaron y corrÃ­gelos manualmente." -ForegroundColor Gray
}

Write-Host ""
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host "RESUMEN DE EJECUCIÃ“N" -ForegroundColor Cyan
Write-Host "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""
Write-Host "Autopep8: Correcciones de estilo aplicadas" -ForegroundColor Green
Write-Host "Black: CÃ³digo formateado" -ForegroundColor Green
Write-Host "Isort: Imports ordenados" -ForegroundColor Green
Write-Host ""
Write-Host "Verificaciones completadas:" -ForegroundColor Cyan
Write-Host "   - Flake8 (errores de estilo)" -ForegroundColor Gray
Write-Host "   - MyPy (errores de tipado)" -ForegroundColor Gray
Write-Host "   - Pytest (tests unitarios)" -ForegroundColor Gray
Write-Host ""
Write-Host "Para guardar los cambios en Git:" -ForegroundColor Yellow
Write-Host "   git add ." -ForegroundColor White
Write-Host "   git commit -m style:apply_code_quality_fixes_autopep8_black_isort" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "Proceso de correccion automatica" -ForegroundColor Green -NoNewline
Write-Host " completado!" -ForegroundColor Green
Write-Host ""

