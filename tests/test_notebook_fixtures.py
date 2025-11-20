import pandas as pd
from pathlib import Path
from src.notebook_fixtures import normalize_columns, normalize_umbral_dataframe
from src.notebook_fixtures import normalize_decile_columns


def test_normalize_columns_anio_alias():
    df = pd.DataFrame({"Anio": [2019, 2020], "Inflacion_Anual_%": [1.0, 2.0]})
    df2 = normalize_columns(df)
    assert "Año" in df2.columns and "Anio" in df2.columns


def test_normalize_umbral_pobreza_euros_alias():
    df = pd.DataFrame(
        {
            "Anio": [2020],
            "Tipo_Hogar": ["Hogares de una persona"],
            "Umbral_Pobreza_Euros": [1000],
        }
    )
    df2 = normalize_umbral_dataframe(df)
    assert "Umbral_Euros" in df2.columns
    assert df2["Umbral_Euros"].iloc[0] == 1000


def test_normalize_umbral_real_base_alias():
    df = pd.DataFrame(
        {
            "Anio": [2020],
            "Tipo_Hogar": ["Hogares de una persona"],
            "Umbral_Real_€_Base": [1200],
        }
    )
    df2 = normalize_umbral_dataframe(df)
    assert "Umbral_Euros" in df2.columns
    assert df2["Umbral_Euros"].iloc[0] == 1200


def test_normalize_decile_columns_int_and_str():
    df = pd.DataFrame(
        {1: [100, 200], "2": [150, 250], "Decil 3": [120, 220]}, index=[2019, 2020]
    )
    df2 = normalize_decile_columns(df)
    assert "D1" in df2.columns and "D2" in df2.columns and "D3" in df2.columns
    assert df2["D1"].iloc[0] == 100
    assert df2["D2"].iloc[1] == 250


def test_normalize_decile_columns_tuple_multiindex():
    # Simulate pivot with MultiIndex columns: ('Renta', 'D1') etc.
    import pandas as pd

    data = {("Renta", "1"): [100, 200], ("Renta", "10"): [900, 1000]}
    df = pd.DataFrame(data, index=[2019, 2020])
    df2 = normalize_decile_columns(df)
    assert "D1" in df2.columns and "D10" in df2.columns
    assert df2["D10"].iloc[0] == 900
