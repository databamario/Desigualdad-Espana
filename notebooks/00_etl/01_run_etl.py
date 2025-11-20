"""
Script de Ejecución del Pipeline ETL
========================================

Ejecuta los 3 notebooks de ETL en orden:
1. 01a_extract_transform_INE.ipynb      - Extracción de 14 tablas INE
2. 01b_extract_transform_EUROSTAT.ipynb - Extracción de 14 tablas Eurostat
3. 01c_load_to_sql.ipynb                - Carga de 28 tablas a SQL Server

Uso:
    python run_etl.py
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def ejecutar_notebook(notebook_path):
    """
    Ejecuta un notebook usando nbconvert
    
    Args:
        notebook_path: Path al notebook
        
    Returns:
        True si exitoso, False si error
    """
    nombre = notebook_path.stem
    print(f"\n{'='*80}")
    print(f">>> Ejecutando: {nombre}")
    print(f"{'='*80}")
    
    try:
        # Ejecutar notebook con jupyter nbconvert
        cmd = [
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--inplace',
            str(notebook_path)
        ]
        
        resultado = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutos timeout
        )
        
        if resultado.returncode == 0:
            print(f"[OK] {nombre} completado exitosamente")
            return True
        else:
            print(f"[ERR] Error en {nombre}:")
            print(resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[WARN] Timeout en {nombre} (>10 minutos)")
        return False
    except Exception as e:
        print(f"[ERR] Error ejecutando {nombre}: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("PIPELINE ETL - DESIGUALDAD SOCIAL")
    print("="*80)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Directorio de notebooks (current file parent)
    notebooks_dir = Path(__file__).resolve().parent
    # Repo root is two levels above (notebooks/00_etl -> notebooks -> repo root)
    repo_root = Path(__file__).resolve().parents[2]
    
    # Notebooks a ejecutar en orden (usando los existentes y probados)
    notebooks = [
        notebooks_dir / '01a_extract_transform_INE.ipynb',
        notebooks_dir / '01b_extract_transform_EUROSTAT.ipynb',
        notebooks_dir / '01c_load_to_sql.ipynb'
    ]
    
    # Verificar que existen
    for nb in notebooks:
        if not nb.exists():
            print(f"[ERR] Error: No se encuentra {nb.name}")
            sys.exit(1)
    
    # Ejecutar notebooks en orden
    inicio = datetime.now()
    exitosos = 0
    
    for notebook in notebooks:
        if ejecutar_notebook(notebook):
            exitosos += 1
        else:
            print(f"\n[ERR] Pipeline detenido por error en {notebook.name}")
            break
        # After running the Eurostat + INE extraction notebooks but before loader, run the pre-check for critical pickles
        if notebook.name == '01b_extract_transform_EUROSTAT.ipynb' and exitosos >= 2:
            # After extraction, ensure 'Anio' columns in pickles to avoid encoding problems
            print('\nAsegurando columnas "Anio" en pickles (scripts/ensure_anio_columns.py)')
            ensure_cmd = [sys.executable, str(repo_root / 'scripts' / 'ensure_anio_columns.py')]
            try:
                ensure_res = subprocess.run(ensure_cmd, capture_output=True, text=True, cwd=str(repo_root))
                print(ensure_res.stdout)
                if ensure_res.stderr:
                    print('--- ensure stderr ---')
                    print(ensure_res.stderr)
            except Exception as e_ens:
                print(f'[WARN] No se pudo ejecutar ensure_anio_columns: {e_ens}')

            print('\nVerificando pickles críticos antes de cargar (scripts/check_pickles.py)')
            check_cmd = [sys.executable, str(repo_root / 'scripts' / 'check_pickles.py')]
            try:
                check_result = subprocess.run(check_cmd, capture_output=True, text=True, cwd=str(repo_root))
                print(check_result.stdout)
                if check_result.stderr:
                    print('--- check stderr ---')
                    print(check_result.stderr)
                if check_result.returncode != 0:
                    print('[ERR] Error: Pickles críticos faltantes o vacíos. Interrumpiendo pipeline ETL.')
                    sys.exit(1)
            except Exception as e_check:
                print(f'[WARN] No se pudo ejecutar el chequeo de pickles: {e_check}')
                sys.exit(1)
    
    # Resumen final
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    
    print("\n" + "="*80)
    print("RESUMEN DE EJECUCIÓN")
    print("="*80)
    print(f"Notebooks ejecutados: {exitosos}/{len(notebooks)}")
    print(f"Duración total: {duracion:.1f} segundos ({duracion/60:.1f} minutos)")
    print(f"Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exitosos == len(notebooks):
        print("\nPipeline ETL completado exitosamente!")
        print("\nSiguiente paso:")
        print("   • Ejecutar validación: python 02_run_validation.py")
        sys.exit(0)
    else:
        print("\nPipeline incompleto - revisar errores arriba")
        sys.exit(1)

if __name__ == '__main__':
    main()
