#!/usr/bin/env python3
"""
Check critical ETL pickles for existence and emptiness.
Usage: python scripts/check_pickles.py [--no-abort]
Returns exit code 0 if all ok, 1 otherwise.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

# Ensure `src` package can be imported when running the script from scripts/ directory
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Imports del proyecto (después de configurar sys.path)
from src.config import CACHE_DIR  # noqa: E402

CRITICAL_PICKLES = ["df_ipc_sectorial.pkl", "df_gini_ccaa.pkl", "df_epf_gasto.pkl"]

# Columns expectations (optional) - if a list is present, check that columns exist
# UPDATED 2025-11-19: Changed 'Año' → 'Anio' (ASCII-safe encoding fix)
CRITICAL_PICKLES_COLS = {
    "df_ipc_sectorial.pkl": ["Anio", "Categoria_ECOICOP", "Inflacion_Sectorial_%"],
    "df_gini_ccaa.pkl": ["Territorio", "Anio", "Gini"],
    "df_epf_gasto.pkl": ["Anio", "Quintil", "Grupo_Gasto", "Valor"],
}

parser = argparse.ArgumentParser(
    description="Check critical ETL pickles for presence/emptiness"
)
parser.add_argument(
    "--no-abort",
    action="store_true",
    help="Do not abort on missing/empty pickles; only print warnings",
)
parser.add_argument(
    "--no-emoji",
    action="store_true",
    help="Do not print emoji characters (safe for non-utf8 consoles)",
)
args = parser.parse_args()

missing_or_empty = []
emoji = not args.no_emoji
for p in CRITICAL_PICKLES:
    ppath = Path(CACHE_DIR) / p
    if not ppath.exists():
        print(f"[WARN] Missing pickle: {ppath}")
        missing_or_empty.append(str(ppath))
    else:
        try:
            df = pd.read_pickle(ppath)
            if df is None or df.empty:
                print(
                    f"[WARN] Empty pickle: {ppath} (shape: {None if df is None else df.shape})"
                )
                missing_or_empty.append(str(ppath))
            else:
                if emoji:
                    print(f"[OK] {ppath} ({df.shape[0]} rows x {df.shape[1]} cols)")
                else:
                    print(f"OK: {ppath} ({df.shape[0]} rows x {df.shape[1]} cols)")
                # Optional column checks
                expected_cols = CRITICAL_PICKLES_COLS.get(p, [])
                if expected_cols:
                    missing_cols = [c for c in expected_cols if c not in df.columns]
                    if missing_cols:
                        print(
                            f"[WARN] Pickle {ppath} lacks expected columns: {missing_cols}"
                        )
                        missing_or_empty.append(str(ppath))
        except Exception as e:
            print(f"[ERROR] Error reading pickle {ppath}: {e}")
            missing_or_empty.append(str(ppath))

if missing_or_empty:
    print("\nERROR: Critical pickles missing/empty:")
    for m in missing_or_empty:
        print(" - " + m)
    if not args.no_abort:
        sys.exit(1)
    else:
        print("\nContinuing (no-abort specified).")
else:
    print("\nAll critical pickles OK.")
    sys.exit(0)
