import pickle, os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_ipc_sectorial_group_sizes_are_four():
    p = os.path.join("outputs", "pickle_cache", "df_ipc_sectorial.pkl")
    assert os.path.exists(p), f"Pickle no encontrado: {p}"
    df = pickle.load(open(p, "rb"))
    # Ensure that for any Anio + Categoria_ECOICOP there are exactly 4 records (4 Tipo_Metrica)
    group_counts = df.groupby(["Anio", "Categoria_ECOICOP"]).size().unique()
    assert (
        len(group_counts) == 1 and group_counts[0] == 4
    ), f"Group sizes not consistent: {group_counts}"
