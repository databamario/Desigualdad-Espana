"""
Configuración Global de Validación
===================================
Umbrales y parámetros globales para la validación de datos.
"""

import os

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Umbrales de calidad
MAX_NULL_PERCENT = 0.05  # 5% máximo de valores nulos permitidos
MAX_TEMPORAL_VARIATION = 200.0  # 200% variación máxima año a año
MIN_VOLATILITY_RATIO = 3.0  # Ratio mínimo para considerar exclusión por volatilidad

# Rangos esperados para indicadores
EXPECTED_RANGES = {
    "AROPE": (0, 100),  # Porcentajes
    "AROP": (0, 100),
    "Gini": (0, 1),  # Coeficiente entre 0 y 1
    "S80S20": (0, 20),  # Ratio típicamente < 10
    "IPC": (-5, 20),  # Inflación razonable
    "Tasa_Desempleo": (0, 50),
    "Poblacion": (0, float("inf")),  # Sin límite superior
}

# Protocolo de corrección
CORRECTION_PROTOCOL = {
    "missing_data": "Si falta > 5% de datos en columna crítica, volver al ETL",
    "outliers": "Documentar outliers, no corregir en validación",
    "duplicates": "Eliminar duplicados si son exactos, investigar si difieren",
    "unstable_categories": "Excluir si volatilidad > 3x baseline y es artefacto metodológico",
}

# Conexión a base de datos
# Carga desde variable de entorno, con fallback a valor por defecto
DB_CONNECTION_STRING = os.environ.get(
    "DB_CONNECTION_STRING",
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=desigualdad;Trusted_Connection=yes;TrustServerCertificate=yes;",
)
