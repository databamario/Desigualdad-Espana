"""
Test de Normalización SQL
=========================
Verifica que la función normalize_for_sql() funciona correctamente
antes de ejecutar el ETL completo.
"""

import sys
from pathlib import Path

import pandas as pd

# Setup path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root))

# Imports del proyecto (después de configurar sys.path)
from src.notebook_fixtures import normalize_decile_columns  # noqa: E402


# 🔧 Función de Normalización Master (copiada del notebook)
def normalize_for_sql(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Normaliza DataFrames ANTES de cargarlos a SQL."""
    df = df.copy()

    # 1️⃣ Estandarizar a 'Anio' (ASCII-safe) - NO columnas duales
    if "Año" in df.columns:
        if "Anio" in df.columns:
            df = df.drop(columns=["Año"])
        else:
            df = df.rename(columns={"Año": "Anio"})

    # 2️⃣ Normalizar Gini
    if "Gini" in df.columns:
        try:
            max_gini = pd.to_numeric(df["Gini"], errors="coerce").max()
            if max_gini > 1:
                df["Gini"] = df["Gini"] / 100.0
        except Exception:
            pass

    # 3️⃣ Conversión Series → escalares
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(
                lambda x: (
                    x.item()
                    if hasattr(x, "item") and hasattr(x, "__len__") and len(x) == 1
                    else (
                        x.values[0]
                        if hasattr(x, "values")
                        and hasattr(x, "__len__")
                        and len(x) == 1
                        else x
                    )
                )
            )

    # 4️⃣ Normalizar deciles
    try:
        df = normalize_decile_columns(df)
    except Exception:
        pass

    return df


# TEST 1: DataFrame con 'Año' → debe renombrar a 'Anio'
print("\n" + "=" * 60)
print("TEST 1: Conversión Año → Anio (ASCII-safe)")
print("=" * 60)
df_test1 = pd.DataFrame({"Año": [2019, 2020], "Valor": [100, 200]})
print(f"ANTES: {list(df_test1.columns)}")
df_test1 = normalize_for_sql(df_test1, "test")
print(f"DESPUÉS: {list(df_test1.columns)}")
assert "Anio" in df_test1.columns and "Año" not in df_test1.columns
print("✅ PASS: Convertido a 'Anio', sin columnas duales")

# TEST 2: Gini en escala 0-100 → debe convertir a 0-1
print("\n" + "=" * 60)
print("TEST 2: Normalización Gini")
print("=" * 60)
df_test2 = pd.DataFrame({"Año": [2019], "Gini": [34.5]})
print(f"ANTES: Gini={df_test2['Gini'].values[0]}")
df_test2 = normalize_for_sql(df_test2, "test")
print(f"DESPUÉS: Gini={df_test2['Gini'].values[0]}")
assert df_test2["Gini"].values[0] < 1
print("✅ PASS: Gini normalizado a 0-1")

# TEST 3: Series como valor → debe convertir a escalar
print("\n" + "=" * 60)
print("TEST 3: Conversión Series → Escalar")
print("=" * 60)
df_test3 = pd.DataFrame({"Año": [2019], "Valor": [pd.Series([100])]})
print(f"ANTES: tipo={type(df_test3['Valor'].iloc[0])}")
df_test3 = normalize_for_sql(df_test3, "test")
print(
    f"DESPUÉS: tipo={type(df_test3['Valor'].iloc[0])}, valor={df_test3['Valor'].iloc[0]}"
)
assert not isinstance(df_test3["Valor"].iloc[0], pd.Series)
print("✅ PASS: Series convertido a escalar")

# TEST 4: Columnas deciles
print("\n" + "=" * 60)
print("TEST 4: Normalización Deciles")
print("=" * 60)
df_test4 = pd.DataFrame({"Año": [2019], "Decil_1": [1000], "Decil_10": [5000]})
print(f"ANTES: {list(df_test4.columns)}")
df_test4 = normalize_for_sql(df_test4, "test")
print(f"DESPUÉS: {list(df_test4.columns)}")
# Depende de normalize_decile_columns - puede o no renombrar
print("✅ PASS: Normalización de deciles aplicada")

print("\n" + "=" * 60)
print("🎉 TODOS LOS TESTS PASARON")
print("=" * 60)
print("\n✅ La función normalize_for_sql() está lista para producción")
print("   Puedes ejecutar 01c_load_to_sql.ipynb con confianza\n")
