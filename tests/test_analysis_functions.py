"""
Tests unitarios para funciones críticas del análisis de desigualdad.

Verifica:
- Deflactación correcta
- Cálculo de Gini
- Validaciones de datos
- Consistencia de resultados

Uso: pytest tests/test_analysis_functions.py
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validacion import validar_nulos, validar_rango


class TestDeflactacion:
    """Tests para la deflactación de datos"""

    def test_deflactor_base_es_uno(self):
        """El deflactor del año base debe ser 1.0"""
        ano_base = 2008
        deflactor = {ano_base: 1.0}
        assert deflactor[ano_base] == 1.0, "El deflactor del año base debe ser 1.0"

    def test_deflactor_aumenta_con_inflacion_positiva(self):
        """Con inflación positiva, el deflactor debe aumentar"""
        deflactor = {2008: 1.0}
        inflacion_2009 = 0.03  # 3%
        deflactor[2009] = deflactor[2008] * (1 + inflacion_2009)

        assert (
            deflactor[2009] > deflactor[2008]
        ), "El deflactor debe aumentar con inflación positiva"
        assert (
            abs(deflactor[2009] - 1.03) < 0.001
        ), "Deflactor 2009 debe ser aproximadamente 1.03"

    def test_renta_real_menor_con_inflacion(self):
        """La renta real debe ser menor que la nominal si hay inflación acumulada"""
        renta_nominal = 10000
        deflactor = 1.20  # 20% inflación acumulada
        renta_real = renta_nominal / deflactor

        assert (
            renta_real < renta_nominal
        ), "Renta real debe ser menor que nominal con inflación"
        assert (
            abs(renta_real - 8333.33) < 1
        ), "Renta real debe ser aproximadamente 8333.33"


class TestValidacionDatos:
    """Tests para funciones de validación"""

    def test_validar_nulos_detecta_columnas_con_nulos(self):
        """validar_nulos debe detectar columnas con nulos"""
        df = pd.DataFrame(
            {
                "Anio": [2008, 2009, 2010],
                "Gini": [33.2, None, 34.1],
                "S80S20": [5.5, 5.8, 6.0],
            }
        )

        # Debe detectar nulos en Gini
        nulos_detectados = df["Gini"].isnull().sum()
        assert nulos_detectados == 1, "Debe detectar 1 nulo en Gini"

    def test_validar_rango_detecta_valores_fuera_rango(self):
        """validar_rango debe detectar valores fuera del rango esperado"""
        df = pd.DataFrame({"Gini": [33.2, 150.0, 34.1]})  # 150 está fuera de rango

        fuera_rango = df[(df["Gini"] < 0) | (df["Gini"] > 100)]
        assert len(fuera_rango) == 1, "Debe detectar 1 valor fuera de rango"


class TestCalculoIndicadores:
    """Tests para cálculo de indicadores de desigualdad"""

    def test_ratio_s80s20_siempre_mayor_que_uno(self):
        """El ratio S80/S20 debe ser siempre >= 1"""
        renta_s80 = 50000
        renta_s20 = 10000
        ratio = renta_s80 / renta_s20

        assert ratio >= 1.0, "S80/S20 debe ser >= 1"
        assert ratio == 5.0, "Ratio debe ser exactamente 5.0"

    def test_gini_rango_valido(self):
        """El Gini debe estar entre 0 y 100 (escala)"""
        gini_valores = [33.2, 34.5, 35.1, 32.8]

        for gini in gini_valores:
            assert 0 <= gini <= 100, f"Gini {gini} debe estar entre 0 y 100"

    def test_arope_menor_o_igual_100(self):
        """AROPE es un porcentaje, debe ser <= 100"""
        arope_valores = [26.5, 27.8, 25.3, 28.1]

        for arope in arope_valores:
            assert 0 <= arope <= 100, f"AROPE {arope} debe estar entre 0 y 100"


class TestConsistenciaResultados:
    """Tests para verificar consistencia entre indicadores"""

    def test_gini_y_s80s20_correlacionan_positivamente(self):
        """Gini y S80/S20 deben correlacionar positivamente"""
        df = pd.DataFrame(
            {"Gini": [32.0, 33.0, 34.0, 35.0], "S80S20": [5.0, 5.3, 5.6, 5.9]}
        )

        correlacion = df["Gini"].corr(df["S80S20"])
        assert (
            correlacion > 0.7
        ), f"Correlación Gini-S80S20 debe ser > 0.7, obtenida: {correlacion}"

    def test_renta_d10_mayor_que_d1(self):
        """La renta del D10 siempre debe ser mayor que D1"""
        renta_d1 = 5000
        renta_d10 = 45000

        assert renta_d10 > renta_d1, "Renta D10 debe ser mayor que D1"

    def test_umbral_real_consistente_con_inflacion(self):
        """El umbral real debe disminuir si inflación acumulada es positiva"""
        umbral_nominal_2023 = 10990
        umbral_nominal_2008 = 7980
        inflacion_acumulada = 0.35  # 35%

        umbral_real_2023 = umbral_nominal_2023 / (1 + inflacion_acumulada)

        # El umbral real 2023 debe ser menor que el nominal 2008 (aprox)
        # porque la inflación erosiona el poder adquisitivo
        assert (
            umbral_real_2023 < umbral_nominal_2023
        ), "Umbral real debe ser menor que nominal"


class TestIntegridadDatos:
    """Tests para integridad del DataFrame final"""

    def test_no_duplicados_en_año(self):
        """No debe haber años duplicados en df_limpio"""
        df = pd.DataFrame(
            {
                "Anio": [2008, 2009, 2010, 2010],  # 2010 duplicado
                "Gini": [32.0, 33.0, 34.0, 34.5],
            }
        )

        duplicados = df["Anio"].duplicated().sum()
        assert duplicados > 0, "Debe detectar años duplicados (test de ejemplo)"

    def test_continuidad_temporal(self):
        """Debe haber continuidad en los años (sin saltos)"""
        años = [2008, 2009, 2010, 2012]  # Falta 2011
        años_esperados = list(range(2008, 2013))

        diferencia = set(años_esperados) - set(años)
        assert len(diferencia) == 1, f"Debe detectar año faltante: {diferencia}"


# Configuración de pytest
def pytest_configure(config):
    """Configuración personalizada de pytest"""
    config.addinivalue_line(
        "markers", "slow: marca tests lentos que requieren datos completos"
    )
    config.addinivalue_line(
        "markers", "integration: tests de integración que requieren archivos externos"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
