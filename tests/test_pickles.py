import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "outputs" / "pickle_cache"
CRITICAL_PICKLES = ["df_ipc_sectorial.pkl", "df_gini_ccaa.pkl", "df_epf_gasto.pkl"]


def test_critical_pickles_exist_and_non_empty():
    missing_or_empty = []
    for p in CRITICAL_PICKLES:
        ppath = CACHE_DIR / p
        assert ppath.exists(), f"Missing critical pickle: {ppath}"
        df = pd.read_pickle(ppath)
        assert df is not None and not df.empty, f"Empty critical pickle: {ppath}"
