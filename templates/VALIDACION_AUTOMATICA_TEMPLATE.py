"""
Script de validación automática para proyectos profesionales de análisis de datos.
Incluye funciones para validar rangos, detectar outliers, comparar fuentes y registrar warnings.
Adapta los criterios y umbrales según el contexto del proyecto.
"""
import pandas as pd
import numpy as np

class ValidationWarnings:
    def __init__(self):
        self.warnings = []
    def add(self, mensaje, nivel="warning", contexto=None):
        self.warnings.append({"mensaje": mensaje, "nivel": nivel, "contexto": contexto})
    def export_csv(self, ruta):
        pd.DataFrame(self.warnings).to_csv(ruta, index=False)

# Ejemplo de validación de rangos

def validar_rangos(df, columna, min_val, max_val, warnings):
    outliers = df[(df[columna] < min_val) | (df[columna] > max_val)]
    if not outliers.empty:
        warnings.add(f"Valores fuera de rango en {columna}", contexto=outliers.index.tolist())
    return outliers

# Ejemplo de comparación entre fuentes

def comparar_fuentes(df1, df2, columna, warnings, tolerancia=0.05):
    dif = np.abs(df1[columna] - df2[columna])
    if (dif > tolerancia).any():
        warnings.add(f"Discrepancias significativas en {columna} entre fuentes", contexto=dif[dif > tolerancia].index.tolist())
    return dif

# Ejemplo de validación temporal

def validar_coherencia_temporal(df, columna, warnings, max_delta=0.2):
    delta = df[columna].diff().abs()
    if (delta > max_delta).any():
        warnings.add(f"Cambios interanuales atípicos en {columna}", contexto=delta[delta > max_delta].index.tolist())
    return delta

# Uso recomendado:
# warnings = ValidationWarnings()
# outliers = validar_rangos(df, 'variable', 0, 100, warnings)
# dif = comparar_fuentes(df1, df2, 'variable', warnings)
# delta = validar_coherencia_temporal(df, 'variable', warnings)
# warnings.export_csv('warnings.csv')
