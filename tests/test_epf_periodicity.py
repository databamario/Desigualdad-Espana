import pickle, os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_epf_is_annual():
    p = os.path.join('outputs','pickle_cache','df_epf_gasto.pkl')
    assert os.path.exists(p), f"Pickle no encontrado: {p}"
    df = pickle.load(open(p, 'rb'))
    assert 'Anio' in df.columns or 'Año' in df.columns
    # Normalize year
    years = sorted(df['Anio'].tolist() if 'Anio' in df.columns else df['Año'].tolist())
    years_unique = sorted(list(set(years)))
    diffs = [y2 - y1 for y1, y2 in zip(years_unique[:-1], years_unique[1:])]
    # If at least one diff is 1, treat as annual series (some series may mix), otherwise it's strictly bienial or irregular
    assert any(d == 1 for d in diffs), "EPF serie no presenta paso anual en 'Anio' (posible bienalidad o datos irregulares)"
