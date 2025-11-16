"""
🚀 Script de Ejecución del Pipeline ETL
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
    print(f"▶️  Ejecutando: {nombre}")
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
            print(f"✅ {nombre} completado exitosamente")
            return True
        else:
            print(f"❌ Error en {nombre}:")
            print(resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout en {nombre} (>10 minutos)")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando {nombre}: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("🚀 PIPELINE ETL - DESIGUALDAD SOCIAL")
    print("="*80)
    print(f"🕒 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Directorio de notebooks
    notebooks_dir = Path(__file__).parent
    
    # Notebooks a ejecutar en orden (usando los existentes y probados)
    notebooks = [
        notebooks_dir / '01a_extract_transform_INE.ipynb',
        notebooks_dir / '01b_extract_transform_EUROSTAT.ipynb',
        notebooks_dir / '01c_load_to_sql.ipynb'
    ]
    
    # Verificar que existen
    for nb in notebooks:
        if not nb.exists():
            print(f"❌ Error: No se encuentra {nb.name}")
            sys.exit(1)
    
    # Ejecutar notebooks en orden
    inicio = datetime.now()
    exitosos = 0
    
    for notebook in notebooks:
        if ejecutar_notebook(notebook):
            exitosos += 1
        else:
            print(f"\n❌ Pipeline detenido por error en {notebook.name}")
            break
    
    # Resumen final
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    
    print("\n" + "="*80)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("="*80)
    print(f"✅ Notebooks ejecutados: {exitosos}/{len(notebooks)}")
    print(f"⏱️  Duración total: {duracion:.1f} segundos ({duracion/60:.1f} minutos)")
    print(f"🕒 Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exitosos == len(notebooks):
        print("\n🎉 ¡Pipeline ETL completado exitosamente!")
        print("\n📋 Siguiente paso:")
        print("   • Ejecutar validación: python 02_run_validation.py")
        sys.exit(0)
    else:
        print("\n❌ Pipeline incompleto - revisar errores arriba")
        sys.exit(1)

if __name__ == '__main__':
    main()
