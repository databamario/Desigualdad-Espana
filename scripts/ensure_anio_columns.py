"""
Script to ensure pickles in outputs/pickle_cache use 'Anio' as canonical year column.
Renames columns 'Año', 'Anyo', 'A�o' to 'Anio' when present.

This is meant to be run after extraction notebooks and before the load stage.
"""

import pickle
import sys
from pathlib import Path
from pathlib import Path as _Path

import pandas as pd

BASE_DIR = _Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Imports del proyecto (después de configurar sys.path)
from utils.validation_framework import normalize_tipo_metrica  # noqa: E402


def find_project_root():
    p = Path.cwd()
    while p != p.parent:
        if (p / ".git").exists() or (p / "README.md").exists():
            return p
        p = p.parent
    return Path.cwd()


project_root = find_project_root()
CACHE_DIR = project_root / "outputs" / "pickle_cache"

PICKLES = [p for p in CACHE_DIR.glob("*.pkl")]

print(f"Cache dir: {CACHE_DIR}")
print(f"Total pickles: {len(PICKLES)}")

# We'll check for these variants and rename to 'Anio'
VARIANTS = ["Año", "Anyo", "A�o"]

fixed = []
for p in PICKLES:
    try:
        with open(p, "rb") as f:
            df = pickle.load(f)
        if not isinstance(df, pd.DataFrame):
            continue
        cols = df.columns.tolist()
        rename = {}
        for bad in ["Año", "Anyo", "A�o"]:
            if bad in cols and "Anio" not in cols:
                rename[bad] = "Anio"
        modified = False
        if rename:
            df = df.rename(columns=rename)
            modified = True
        # Normalize Tipo_Metrica if present
        if "Tipo_Metrica" in df.columns:
            df = df.copy()
            df["Tipo_Metrica"] = normalize_tipo_metrica(df["Tipo_Metrica"])
            modified = True

        # If we made modifications (rename or normalization), write back pickle
        if modified:
            try:
                with open(p, "wb") as f:
                    pickle.dump(df, f)
                fixed.append((p.name, rename))
            except Exception as e:
                print(f"Failed to write back modified pickle {p}: {e}")
    except Exception as e:
        print(f"Error processing {p}: {e}")

print(f"Fixed {len(fixed)} pickles:")
for name, rename in fixed:
    print(f" - {name}: {rename}")

if len(fixed) == 0:
    print("No renames required.")

print("Done.")
