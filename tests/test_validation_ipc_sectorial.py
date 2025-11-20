import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.validation_framework import check_conditional_nulls


def test_check_conditional_nulls_valid():
    # Build a minimal df: 4 rows, 3 Tipo_Metrica types
    df = pd.DataFrame({
        'Anio': [2020, 2020, 2020, 2020],
        'Categoria_ECOICOP': ['A', 'A', 'A', 'A'],
        'Tipo_Metrica': ['Variación anual', 'Variación mensual', 'Variación en lo que va de año', 'Índice'],
        'Inflacion_Sectorial_%': [1.2, 0.4, 0.8, None]
    })

    rules = {
        'Inflacion_Sectorial_%': {
            'cond_column': 'Tipo_Metrica',
            'cond_null_substrings': ['ndice']
        }
    }

    assert check_conditional_nulls(df, rules) is True


def test_check_conditional_nulls_invalid():
    # Invalid if a non-index metric has null in Inflacion_Sectorial_%
    df = pd.DataFrame({
        'Anio': [2020, 2020],
        'Categoria_ECOICOP': ['A', 'A'],
        'Tipo_Metrica': ['Variación anual', 'Índice'],
        'Inflacion_Sectorial_%': [None, None]
    })

    rules = {
        'Inflacion_Sectorial_%': {
            'cond_column': 'Tipo_Metrica',
            'cond_null_substrings': ['ndice']
        }
    }

    assert check_conditional_nulls(df, rules) is False


def test_real_ipc_sectorial_dataset():
    """Cargar pickle real y validar la regla condicional"""
    import pickle, os
    p = os.path.join('outputs','pickle_cache','df_ipc_sectorial.pkl')
    assert os.path.exists(p), f"Pickle no encontrado: {p}"
    df = pickle.load(open(p, 'rb'))
    rules = {
        'Inflacion_Sectorial_%': {
            'cond_column': 'Tipo_Metrica',
            'cond_null_substrings': ['ndice']
        }
    }
    assert check_conditional_nulls(df, rules) is True
