"""
Minimal integration tests for the analysis notebooks.

This module contains a minimal, focused test to verify the decile normalization helper
and to assert that the pivot with columns D1..D10 is present for 2019 and 2023.
"""

from pathlib import Path
import pandas as pd
import pytest
from src.notebook_fixtures import load_pickles_to_namespace, normalize_decile_columns


@pytest.mark.integration
def test_execute_03_analisis_inflacion_diferencial_basic(tmp_path: Path):
    project_root = Path(__file__).parent.parent
    outputs_dir = project_root / 'outputs'
    pickle_cache = outputs_dir / 'pickle_cache'

    mapping = {
        'df_renta': 'df_renta_decil.pkl',
        'df_gini_ccaa': 'df_gini_ccaa.pkl',
        'df_gini_s80s20': 'df_s80s20_es.pkl',
    }
    ns = load_pickles_to_namespace(pickle_cache, mapping)
    assert 'df_renta' in ns or 'df_pivot_deciles' in ns, (
        'Neither df_renta nor df_pivot_deciles present in pickles'
    )

    # Derive pivot if only df_renta present
    if 'df_pivot_deciles' not in ns and 'df_renta' in ns:
        dr = ns['df_renta']
        if 'Año' in dr.columns and 'Anio' not in dr.columns:
            dr['Anio'] = dr['Año']
        val_col = 'Valor' if 'Valor' in dr.columns else next((c for c in dr.columns if 'Renta' in str(c)), None)
        assert val_col is not None, 'No renta column found to construct pivot'
        pivot = dr.pivot_table(index='Anio', columns='Decil', values=val_col)
        pivot = normalize_decile_columns(pivot)
        ns['df_pivot_deciles'] = pivot
    else:
        ns['df_pivot_deciles'] = normalize_decile_columns(ns.get('df_pivot_deciles', pd.DataFrame()))

    pivot = ns['df_pivot_deciles']
    assert isinstance(pivot, pd.DataFrame), 'df_pivot_deciles must be a DataFrame'
    assert 'D1' in pivot.columns and 'D10' in pivot.columns, f"Missing decile columns: {list(pivot.columns)}"
    # Ensure index includes 2019 and 2023
    try:
        years = list(pivot.index.astype(int))
    except Exception:
        years = list(pivot.index)
    assert 2019 in years and 2023 in years, f"Years missing in df_pivot_deciles index: {years}"

    d1_2019 = pivot.loc[2019, 'D1']
    d1_2023 = pivot.loc[2023, 'D1']
    d10_2019 = pivot.loc[2019, 'D10']
    d10_2023 = pivot.loc[2023, 'D10']

    assert pd.notna(d1_2019) and pd.notna(d10_2019), 'D1/D10 missing values for 2019'
    assert pd.notna(d1_2023) and pd.notna(d10_2023), 'D1/D10 missing values for 2023'
    assert d10_2019 > d1_2019 and d10_2023 > d1_2023, 'D10 must be greater than D1'

    print('✅ Minimal decile check passed')
