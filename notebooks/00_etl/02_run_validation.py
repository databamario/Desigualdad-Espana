"""
Orquestador de Validación de Datos
===================================
Script que ejecuta todos los notebooks de validación en secuencia.

Arquitectura Modular:
- 02a_validacion_INE.ipynb       → Valida tablas INE
- 02b_validacion_EUROSTAT.ipynb  → Valida tablas EUROSTAT
- 02c_validacion_integracion.ipynb → Valida coherencia entre fuentes

Uso:
    python 02_run_validation.py

Autor: Proyecto Desigualdad Social ETL
Fecha: 2025-11-13
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path


def analyze_validation_logs(logs_dir: str = '../data/validated/logs') -> dict:
    """
    Analiza los logs de validación y genera un resumen.
    
    Args:
        logs_dir: Directorio donde se encuentran los logs JSON
    
    Returns:
        Diccionario con tablas agrupadas por estado
    """
    # Resolver ruta absoluta desde el directorio del script
    if not Path(logs_dir).is_absolute():
        script_dir = Path(__file__).parent.resolve()
        # Desde notebooks/00_etl/ ir a raíz del proyecto
        project_root = script_dir.parent.parent
        logs_path = project_root / 'data' / 'validated' / 'logs'
    else:
        logs_path = Path(logs_dir)
    
    if not logs_path.exists():
        return {'passed': [], 'failed': [], 'no_logs': True}
    
    # Buscar todos los archivos JSON en el directorio
    json_files = list(logs_path.glob('*.json'))
    
    if not json_files:
        return {'passed': [], 'failed': [], 'no_logs': True}
    
    # Agrupar por timestamp para obtener solo los logs más recientes
    logs_by_table = {}
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
                
                table_name = log_data.get('table_name', 'UNKNOWN')
                timestamp = log_data.get('timestamp', '')
                status = log_data.get('status', 'UNKNOWN')
                errors = log_data.get('errors', [])
                warnings = log_data.get('warnings', [])
                
                # Guardar solo el log más reciente por tabla
                if table_name not in logs_by_table or timestamp > logs_by_table[table_name]['timestamp']:
                    logs_by_table[table_name] = {
                        'timestamp': timestamp,
                        'status': status,
                        'errors': errors,
                        'warnings': warnings,
                        'error_count': len(errors),
                        'warning_count': len(warnings)
                    }
        except Exception as e:
            continue
    
    # Agrupar por estado
    passed = []
    failed = []
    
    for table_name, log_info in sorted(logs_by_table.items()):
        if log_info['status'] == 'FAILED':
            failed.append({
                'table': table_name,
                'errors': log_info['errors'],
                'error_count': log_info['error_count']
            })
        elif log_info['status'] == 'PASSED':
            passed.append({
                'table': table_name,
                'warning_count': log_info['warning_count']
            })
    
    return {
        'passed': passed,
        'failed': failed,
        'no_logs': False
    }


def run_notebook(notebook_path: str) -> bool:
    """
    Ejecuta un notebook usando jupyter nbconvert.
    
    Args:
        notebook_path: Ruta al notebook a ejecutar
    
    Returns:
        True si se ejecutó exitosamente, False si hubo error
    """
    try:
        # Ejecutar notebook con jupyter nbconvert (sin output detallado)
        result = subprocess.run(
            [
                'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                '--inplace',
                notebook_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERR] Error ejecutando {notebook_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"\n[ERR] Error: jupyter nbconvert no encontrado. Instalar con: pip install nbconvert")
        return False


def main():
    """Función principal del orquestador"""
    
    print("="*80)
    print("VALIDACIÓN DE DATOS - DESIGUALDAD SOCIAL")
    print("="*80)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Definir notebooks a ejecutar (en orden)
    notebooks = [
        '02a_validacion_INE.ipynb',
        '02b_validacion_EUROSTAT.ipynb',
        '02c_validacion_integracion.ipynb'
    ]
    
    # Determinar directorio de notebooks (mismo donde está este script)
    script_dir = Path(__file__).parent.resolve()
    
    # Verificar que los notebooks existen
    missing_notebooks = []
    
    for notebook in notebooks:
        notebook_path = script_dir / notebook
        if not notebook_path.exists():
            missing_notebooks.append(str(notebook_path))
    
    if missing_notebooks:
        print("[ERR] Error: No se encontraron los siguientes notebooks:")
        for nb in missing_notebooks:
            print(f"   - {nb}")
        return False
    
    # Ejecutar notebooks en secuencia
    print("Ejecutando validación...")
    results = {}
    
    for notebook in notebooks:
        notebook_path = str(script_dir / notebook)
        print(f"  - {notebook}...", end=' ', flush=True)
        success = run_notebook(notebook_path)
        results[notebook] = success
        
        if success:
            print("[OK]")
        else:
            print("[ERR]")
            print(f"\n[WARN]  Error en {notebook}. ¿Continuar? (SI/NO): ", end='')
            response = input().strip().upper()
            if response != 'SI':
                print("\n[ERR] Validación interrumpida por el usuario")
                break
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE VALIDACIÓN")
    print("="*80)
    
    # Analizar logs de validación
    validation_summary = analyze_validation_logs()
    
    if validation_summary['no_logs']:
        print("\n[WARN]  No se encontraron logs de validación")
        print("   Los reportes deberían estar en: ../data/validated/logs/")
    else:
        failed_tables = validation_summary['failed']
        passed_tables = validation_summary['passed']
        
        print(f"\nTotal de tablas validadas: {len(failed_tables) + len(passed_tables)}")
        print(f"   Correctas (PASSED): {len(passed_tables)}")
        print(f"   Con errores (FAILED): {len(failed_tables)}")
        
        # Mostrar tablas con errores
        if failed_tables:
            print("\n" + "="*80)
            print("TABLAS CON ERRORES CRÍTICOS")
            print("="*80)
            for item in failed_tables:
                print(f"\n[TABLE] {item['table']} ({item['error_count']} errores)")
                for error in item['errors']:
                    print(f"   - {error}")
        
        # Mostrar tablas correctas (solo nombres)
        if passed_tables:
            print("\n" + "="*80)
            print("TABLAS VALIDADAS CORRECTAMENTE")
            print("="*80)
            for item in passed_tables:
                warnings_info = f" ({item['warning_count']} advertencias)" if item['warning_count'] > 0 else ""
                print(f"   {item['table']}{warnings_info}")
    
    print(f"\nFin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Determinar éxito basado en logs de validación
    has_failed_tables = len(validation_summary.get('failed', [])) > 0
    
    if not has_failed_tables and not validation_summary['no_logs']:
        print("\nVALIDACIÓN COMPLETA EXITOSA! Todas las tablas están correctas.")
        return True
    elif has_failed_tables:
        print(f"\n[WARN] VALIDACIÓN COMPLETADA CON ERRORES: {len(validation_summary['failed'])} tabla(s) requieren atención.")
        print("\n🎯 Acción requerida:")
        print("   1. Revisar errores listados arriba")
        print("   2. Corregir datos en origen o ajustar reglas de validación")
        print("   3. Volver a ejecutar validación")
        return False
    else:
        print("\n[WARN]  No se pudieron analizar los logs de validación")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
