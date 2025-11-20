"""
Reglas de Validación por Tabla
================================
Configuración declarativa de las reglas de validación específicas para cada tabla.
"""

# Reglas de validación para tablas INE
INE_VALIDATION_RULES = {
    'INE_AROPE_Hogar': {
        'primary_key': ['Anio', 'Tipo_Hogar', 'Indicador'],
        'critical_columns': ['Anio', 'Tipo_Hogar', 'Indicador', 'Valor'],
        'expected_columns': ['Anio', 'Tipo_Hogar', 'Indicador', 'Valor'],
        'expected_types': {
            'Anio': int,
            'Tipo_Hogar': str,
            'Indicador': str,
            'Valor': float
        },
        'range_checks': {
            'Valor': (0, 100),
            'Anio': (2007, 2025)
        },
        'expected_years': range(2013, 2024),
        'exclude_categories': {
            'Tipo_Hogar': ['No consta']  # Alta volatilidad, artefacto metodológico
        },
        'expected_indicators': [
            'AROPE',
            'AROP',
            'Baja Intensidad Laboral',
            'Carencia Material Severa'
        ],
        'coherence_checks': {
            'internal': 'Verificar que componentes sumen AROPE',
            'temporal': 'Verificar variación < 200% año a año'
        }
    },
    
    'INE_AROPE_CCAA': {
        'primary_key': ['Anio', 'CCAA', 'Indicador'],
        'critical_columns': ['Anio', 'CCAA', 'Indicador', 'Valor'],
        'expected_columns': ['Anio', 'CCAA', 'Indicador', 'Valor'],
        'expected_types': {
            'Anio': int,
            'CCAA': str,
            'Indicador': str,
            'Valor': float
        },
        'range_checks': {
            'Valor': (0, 100),
            'Anio': (2007, 2025)
        },
        'expected_years': range(2008, 2024),
        'coherence_checks': {
            'internal': 'Verificar que Total Nacional sea coherente con CCAA',
            'temporal': 'Verificar variación < 200% año a año'
        }
    },
    
    'INE_AROPE_Edad_Sexo': {
        'primary_key': ['Anio', 'Edad', 'Sexo', 'Indicador'],
        'critical_columns': ['Anio', 'Edad', 'Sexo', 'Indicador', 'Valor'],
        'expected_columns': ['Anio', 'Edad', 'Sexo', 'Indicador', 'Valor'],
        'expected_types': {
            'Anio': int,
            'Edad': str,
            'Sexo': str,
            'Indicador': str,
            'Valor': float
        },
        'range_checks': {
            'Valor': (0, 100),
            'Anio': (2007, 2025)
        },
        'expected_years': range(2008, 2024)
    },
    
    'INE_AROPE_Laboral': {
        'primary_key': ['Anio', 'Sexo', 'Situacion_Laboral', 'Territorio'],
        'critical_columns': ['Anio', 'Sexo', 'Situacion_Laboral', 'Territorio', 'AROPE'],
        'expected_columns': ['Sexo', 'Situacion_Laboral', 'Territorio', 'Anio', 'AROPE'],
        'expected_types': {
            'Anio': int,
            'Sexo': str,
            'Situacion_Laboral': str,
            'Territorio': str,
            'AROPE': float
        },
        'range_checks': {
            'AROPE': (0, 100),  # Porcentaje
            'Anio': (2007, 2025)
        },
        'expected_years': range(2013, 2024)
    },
    
    'INE_IPC_Nacional': {  # Antes: INE_IPC_Anual
        'primary_key': ['Anio'],
        'critical_columns': ['Anio', 'IPC_Medio_Anual'],  # Inflacion_Anual_% puede ser NULL en 2002
        'expected_columns': ['Anio', 'IPC_Medio_Anual', 'Inflacion_Anual_%'],
        'expected_types': {
            'Anio': int,
            'IPC_Medio_Anual': float,
            'Inflacion_Anual_%': float
        },
        'range_checks': {
            'IPC_Medio_Anual': (50, 150),  # Índice base 100
            'Inflacion_Anual_%': (-5, 20),  # Inflación razonable
            'Anio': (2002, 2025)
        },
        'expected_years': range(2002, 2025),
        'coherence_checks': {
            'temporal': 'Verificar variación < 200% año a año (saltos IPC anormales)'
        },
        'notes': 'Inflacion_Anual_% es NULL en 2002 (primer año, no hay referencia anterior)'
    },
    
    'INE_Gini_S80S20_CCAA': {
        'primary_key': ['Año', 'Territorio'],
        'critical_columns': ['Año', 'Territorio', 'Gini', 'S80/S20'],
        'expected_columns': ['Territorio', 'Año', 'Gini', 'S80/S20'],
        'expected_types': {
            'Año': int,
            'Territorio': str,
            'Gini': float,
            'S80/S20': float
        },
        'range_checks': {
            'Gini': (0, 1),  # Gini normalizado (0=igualdad perfecta, 1=máxima desigualdad)
            'S80/S20': (1, 20),  # Ratio quintil 5/quintil 1
            'Año': (2007, 2025)
        },
        'expected_years': range(2008, 2023)
    },
    
    'INE_Poblacion_Edad_Sexo_CCAA': {
        'primary_key': ['Anio', 'CCAA', 'Sexo', 'Edad'],  # Sexo es parte de la clave
        'critical_columns': ['Anio', 'CCAA', 'Sexo', 'Edad', 'Poblacion'],
        'expected_columns': ['Anio', 'CCAA', 'Sexo', 'Edad', 'Poblacion'],
        'expected_types': {
            'Anio': int,
            'CCAA': str,
            'Sexo': str,
            'Edad': str,
            'Poblacion': float  # INE devuelve float (puede tener decimales)
        },
        'range_checks': {
            'Poblacion': (0, 50000000),  # Total nacional puede superar 10M
            'Anio': (2002, 2025)
        },
        'expected_years': range(2002, 2024)
    },
    
    'INE_Poblacion_Edad_Sexo_Nacionalidad': {
        'primary_key': ['Anio', 'Edad', 'Sexo'],
        'critical_columns': ['Anio', 'Edad', 'Sexo', 'Poblacion'],
        'range_checks': {
            'Poblacion': (0, 50000000),
            'Anio': (2002, 2025)
        },
        'expected_years': range(2002, 2024)
    },
    
    'INE_Umbral_Pobreza_Hogar': {
        'primary_key': ['Anio', 'Tipo_Hogar', 'Grupo_Edad', 'Sexo'],  # Incluir todas las dimensiones
        'critical_columns': ['Anio', 'Tipo_Hogar', 'Grupo_Edad', 'Sexo', 'Poblacion'],
        'expected_columns': ['Anio', 'Tipo_Hogar', 'Grupo_Edad', 'Sexo', 'Poblacion'],
        'range_checks': {
            'Poblacion': (0, 50000000),
            'Anio': (2002, 2025)
        },
        'expected_years': range(2013, 2024)
    },
    
    'INE_Renta_Media_Decil': {
        'primary_key': ['Anio', 'Decil'],
        'critical_columns': ['Anio', 'Decil', 'Renta_Media'],
        'range_checks': {
            'Renta_Media': (0, 200000),  # Euros anuales
            'Anio': (2007, 2025)
        },
        'expected_years': range(2008, 2023)
    },
    
    'INE_Umbral_Pobreza_Hogar': {
        'primary_key': ['Anio', 'Tipo_Hogar'],
        'critical_columns': ['Anio', 'Tipo_Hogar', 'Umbral'],
        'range_checks': {
            'Umbral': (0, 50000),  # Euros anuales
            'Anio': (2007, 2025)
        },
        'expected_years': range(2008, 2023)
    },
    
    'INE_Carencia_Material_Decil': {
        'primary_key': ['Anio', 'Decil', 'Item'],
        'critical_columns': ['Anio', 'Decil', 'Item', 'Porcentaje'],
        'range_checks': {
            'Porcentaje': (0, 100),
            'Anio': (2007, 2025)
        },
        'expected_years': range(2013, 2023)
    },
    
    'INE_Gasto_Medio_Hogar_Quintil': {
        'primary_key': ['Anio', 'Quintil', 'Grupo_Gasto', 'Tipo_Valor'],
        'critical_columns': ['Anio', 'Quintil', 'Grupo_Gasto', 'Tipo_Valor', 'Valor'],
        'range_checks': {
            'Valor': (0, 100000),  # Euros anuales
            'Anio': (2006, 2025)
        },
        'expected_years': range(2006, 2024)
    },
    
    'INE_IPC_Sectorial_ECOICOP': {
        'primary_key': ['Anio', 'Categoria_ECOICOP', 'Tipo_Metrica'],
        'critical_columns': ['Anio', 'Categoria_ECOICOP', 'Tipo_Metrica', 'IPC'],
        'range_checks': {
            'IPC': (50, 200),  # Base 100
            'Anio': (2002, 2025)
        },
        'expected_years': range(2002, 2024)
        ,
        # Regla: Inflacion_Sectorial_% debe ser NULL solo cuando Tipo_Metrica==Índice
        'conditional_nulls': {
            'Inflacion_Sectorial_%': {
                'cond_column': 'Tipo_Metrica',
                'cond_null_substrings': ['ndice']  # matches 'Índice', '�ndice', 'Indice'
            }
        }
    }
}

# Reglas de validación para tablas EUROSTAT
EUROSTAT_VALIDATION_RULES = {
    'EUROSTAT_Gini_UE27': {
        'primary_key': ['Anio', 'geo_name'],
        'critical_columns': ['Anio', 'geo_name', 'Gini'],
        'expected_columns': ['Anio', 'geo_name', 'Gini'],
        'expected_types': {
            'Anio': int,
            'geo_name': str,
            'Gini': float
        },
        'range_checks': {
              'Gini': (0, 1.0),  # Gini en escala 0-1
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Gini_Espana': {
        'primary_key': ['Anio'],
        'critical_columns': ['Anio', 'Gini'],
        'expected_columns': ['Anio', 'Gini'],
        'expected_types': {
            'Anio': int,
            'Gini': float
        },
        'range_checks': {
              'Gini': (0, 1.0),
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Gini_Ranking': {
        'primary_key': ['Anio', 'geo_name'],
        'critical_columns': ['Anio', 'geo_name', 'Gini'],
        'expected_columns': ['Anio', 'geo_name', 'Gini', 'geo_code'],
        'range_checks': {
              'Gini': (0, 1.0),
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_AROP_Ranking': {
        'primary_key': ['Anio', 'geo_name'],
        'critical_columns': ['Anio', 'geo_name', 'AROP_%'],
        'expected_columns': ['Anio', 'geo_name', 'AROP_%', 'geo_code'],
        'range_checks': {
            'AROP_%': (0, 100),
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_AROP_UE27': {
        'primary_key': ['Anio', 'geo_name'],
        'critical_columns': ['Anio', 'geo_name', 'AROP_%'],
        'expected_columns': ['Anio', 'geo_name', 'AROP_%'],
        'expected_types': {
            'Anio': int,
            'geo_name': str,
            'AROP_%': float
        },
        'range_checks': {
            'AROP_%': (0, 100),
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_AROP_Espana': {
        'primary_key': ['Anio'],
        'critical_columns': ['Anio', 'AROP'],
        'range_checks': {
            'AROP': (0, 100),
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_S80S20_UE27': {
        'primary_key': ['Anio', 'geo_name'],
        'critical_columns': ['Anio', 'geo_name', 'S80S20'],
        'range_checks': {
            'S80S20': (0, 20),  # Ratio razonable
            'Anio': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_S80S20_Espana': {
        'primary_key': ['Anio'],
        'critical_columns': ['Anio', 'S80S20'],
        'range_checks': {
            'S80S20': (0, 20),
            'Año': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_S80S20_Ranking': {
        'primary_key': ['Año', 'geo_name'],
        'critical_columns': ['Año', 'geo_name', 'S80S20', 'Ranking'],
        'range_checks': {
            'S80S20': (0, 20),
            'Ranking': (1, 30),
            'Año': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Brecha_Pobreza_UE27': {
        'primary_key': ['Año', 'geo_name'],
        'critical_columns': ['Año', 'geo_name', 'Brecha'],
        'range_checks': {
            'Brecha': (0, 100),
            'Año': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Brecha_Pobreza_Espana': {
        'primary_key': ['Año'],
        'critical_columns': ['Año', 'Brecha'],
        'range_checks': {
            'Brecha': (0, 100),
            'Año': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Brecha_Pobreza_Ranking': {
        'primary_key': ['Año', 'geo_name'],
        'critical_columns': ['Año', 'geo_name', 'Brecha', 'Ranking'],
        'range_checks': {
            'Brecha': (0, 100),
            'Ranking': (1, 30),
            'Año': (2015, 2025)
        },
        'expected_years': range(2015, 2024)
    },
    
    'EUROSTAT_Impacto_Redistributivo_UE27': {
        'primary_key': ['Año', 'geo_name'],
        'critical_columns': ['Año', 'geo_name', 'Impacto'],
        'range_checks': {
            'Impacto': (-50, 50),  # Puntos porcentuales
            'Año': (2004, 2025)  # Eurostat tiene datos desde 2004
        },
        'expected_years': range(2004, 2025)
    },
    
    'EUROSTAT_Impacto_Redistributivo_Espana': {
        'primary_key': ['Año'],
        'critical_columns': ['Año', 'Impacto'],
        'range_checks': {
            'Impacto': (-50, 50),
            'Año': (2004, 2025)  # Eurostat tiene datos desde 2004
        },
        'expected_years': range(2004, 2025)
    }
    # NOTA: EUROSTAT_Impacto_Redistributivo_Ranking eliminado - no existe en ETL 01b
}

# Combinar todas las reglas
ALL_VALIDATION_RULES = {
    **INE_VALIDATION_RULES,
    **EUROSTAT_VALIDATION_RULES
}


def get_rules(table_name: str) -> dict:
    """
    Obtiene las reglas de validación para una tabla específica.
    
    Args:
        table_name: Nombre de la tabla
    
    Returns:
        Diccionario con las reglas de validación, o diccionario vacío si no existe
    """
    return ALL_VALIDATION_RULES.get(table_name, {})
