"""
Ejemplo de test unitario para funciones de validación automática.
Utiliza pytest para asegurar que las funciones detectan correctamente outliers y discrepancias.
"""

import pandas as pd
import pytest
from VALIDACION_AUTOMATICA_TEMPLATE import (ValidationWarnings,
                                            comparar_fuentes, validar_rangos)


def test_validar_rangos_outliers():
    df = pd.DataFrame({"var": [10, 20, 150, -5, 30]})
    warnings = ValidationWarnings()
    outliers = validar_rangos(df, "var", 0, 100, warnings)
    assert len(outliers) == 2
    assert any(
        w["mensaje"].startswith("Valores fuera de rango") for w in warnings.warnings
    )


def test_comparar_fuentes_discrepancia():
    df1 = pd.DataFrame({"var": [1.0, 2.0, 3.0]})
    df2 = pd.DataFrame({"var": [1.0, 2.1, 2.7]})
    warnings = ValidationWarnings()
    dif = comparar_fuentes(df1, df2, "var", warnings, tolerancia=0.05)
    assert (dif > 0.05).any()
    assert any(
        "Discrepancias significativas" in w["mensaje"] for w in warnings.warnings
    )


if __name__ == "__main__":
    pytest.main()
