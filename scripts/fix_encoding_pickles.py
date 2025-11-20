"""
Script para corregir el encoding de columnas en pickles existentes.
Convierte 'Año' → 'Anio' para evitar problemas de encoding Windows cp1252/UTF-8.

Fase 1 - Critical Fix para coherencia analítica
"""

import pickle
from pathlib import Path
import pandas as pd


def find_project_root():
    p = Path.cwd()
    while p != p.parent:
        if (p / ".git").exists() or (p / "README.md").exists():
            return p
        p = p.parent
    return Path.cwd()


project_root = find_project_root()
CACHE_DIR = project_root / "outputs" / "pickle_cache"

# Lista de pickles a corregir
PICKLES_TO_FIX = [
    "df_ipc_anual.pkl",
    "df_umbral_limpio.pkl",
    "df_carencia_material.pkl",
    "df_arope_edad_sexo.pkl",
    "df_arope_hogar.pkl",
    "df_arope_ccaa.pkl",
    "df_gini_ccaa.pkl",
    "df_renta_decil.pkl",
    "df_poblacion.pkl",
    "df_poblacion_ccaa_edad.pkl",
    "df_arope_ccaa_filtrado.pkl",
    "df_epf_gasto.pkl",
    "df_ipc_sectorial.pkl",
]


def fix_pickle_encoding(pickle_path):
    """Corrige encoding de columnas en un pickle."""
    try:
        with open(pickle_path, "rb") as f:
            df = pickle.load(f)

        if not isinstance(df, pd.DataFrame):
            print(f"  ⚠️  {pickle_path.name}: No es DataFrame, skip")
            return False

        # Detectar columnas con problemas de encoding
        problematic_cols = [
            col for col in df.columns if "ñ" in str(col).lower() or "�" in str(col)
        ]

        if not problematic_cols:
            print(f"  ✓  {pickle_path.name}: Sin problemas de encoding")
            return False

        # Renombrar columnas
        rename_map = {}
        for col in problematic_cols:
            if "Año" in col or "año" in col or "A�o" in col:
                new_col = (
                    col.replace("Año", "Anio")
                    .replace("año", "anio")
                    .replace("A�o", "Anio")
                )
                rename_map[col] = new_col

        if rename_map:
            df = df.rename(columns=rename_map)

            # Guardar pickle corregido
            with open(pickle_path, "wb") as f:
                pickle.dump(df, f)

            print(f"  ✅ {pickle_path.name}: Corregido {rename_map}")
            return True

        return False

    except Exception as e:
        print(f"  ❌ {pickle_path.name}: Error - {e}")
        return False


def main():
    print("=" * 60)
    print("FIX ENCODING PICKLES - Fase 1 Critical")
    print("=" * 60)
    print(f"Cache directory: {CACHE_DIR.absolute()}\n")

    if not CACHE_DIR.exists():
        print(f"❌ Directory no existe: {CACHE_DIR}")
        return

    fixed_count = 0
    for pickle_name in PICKLES_TO_FIX:
        pickle_path = CACHE_DIR / pickle_name

        if not pickle_path.exists():
            print(f"  ⊘  {pickle_name}: No encontrado, skip")
            continue

        if fix_pickle_encoding(pickle_path):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"RESUMEN: {fixed_count} pickles corregidos")
    print(f"{'='*60}")
    print(
        "\n✅ Siguiente paso: Re-ejecutar ETL para regenerar pickles con encoding correcto"
    )
    print("   Comando: python notebooks/00_etl/01_run_etl.py")


if __name__ == "__main__":
    main()
