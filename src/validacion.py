"""
Módulo de Validación y Control de Calidad de Datos
===================================================

Funciones reutilizables para validar datos de desigualdad social y detectar anomalías.

Autor: Proyecto Desigualdad España
Fecha: 2025-11-17
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union
import warnings


# =============================================================================
# FUNCIONES DE VALIDACIÓN BÁSICA
# =============================================================================

def validar_nulos(df: pd.DataFrame, 
                  columnas: Optional[List[str]] = None,
                  umbral_pct: float = 5.0,
                  verbose: bool = True) -> Dict[str, float]:
    """
    Valida el porcentaje de nulos en un DataFrame.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame a validar
    columnas : List[str], opcional
        Columnas específicas a validar. Si None, valida todas.
    umbral_pct : float, default 5.0
        Umbral de porcentaje de nulos para emitir advertencia
    verbose : bool, default True
        Si True, imprime resultados
        
    Retorna
    -------
    Dict[str, float]
        Diccionario con columnas y su porcentaje de nulos
        
    Advertencias
    ------------
    - Emite warning si alguna columna supera el umbral_pct
    - No distingue entre NULLs legítimos (ausencia de datos en fuente) 
      y errores de ETL
    """
    cols_validar = columnas if columnas else df.columns.tolist()
    
    resultados = {}
    problemas = []
    
    for col in cols_validar:
        if col not in df.columns:
            warnings.warn(f"Columna '{col}' no encontrada en DataFrame")
            continue
            
        pct_nulos = (df[col].isna().sum() / len(df)) * 100
        resultados[col] = round(pct_nulos, 2)
        
        if pct_nulos > umbral_pct:
            problemas.append(f"  [WARN]  {col}: {pct_nulos:.2f}% nulos (>{umbral_pct}%)")
    
    if verbose:
        print("=" * 80)
        print("VALIDACIÓN DE NULOS")
        print("=" * 80)
        print(f"Umbral de advertencia: {umbral_pct}%")
        print(f"Columnas validadas: {len(cols_validar)}")
        
        if problemas:
            print(f"\n[ERR] {len(problemas)} columna(s) superan el umbral:")
            for p in problemas:
                print(p)
        else:
            print(f"\n[OK] Todas las columnas cumplen el umbral (<{umbral_pct}% nulos)")
            
        # Mostrar detalle de todas las columnas
        print("\nDetalle por columna:")
        for col, pct in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
            estado = "[WARN]" if pct > umbral_pct else "[OK]"
            print(f"  {estado} {col}: {pct}%")
    
    return resultados


def _normalize_year_column(df: pd.DataFrame, columna_año: str = 'Anio', verbose: bool = False):
    """
    Normaliza la columna de año aceptando 'Anio' o 'Año' (fallback).
    Devuelve (df_modificado, columna_año_nombre)
    """
    if columna_año in df.columns:
        return df, columna_año
    if 'Anyo' in df.columns:
        # Some data may use 'Anyo' (no diacritics) - treat it as 'Anio'
        df2 = df.copy()
        df2['Anio'] = df2['Anyo']
        if verbose:
            print("[WARN] Se renombró 'Anyo' a 'Anio' temporalmente para validación")
        return df2, 'Anio'
    if 'Año' in df.columns:
        df2 = df.copy()
        df2['Anio'] = df2['Año']
        if verbose:
            print("[WARN] Se renombró 'Año' a 'Anio' temporalmente para validación")
        return df2, 'Anio'
    # No column found
    return df, None


def validar_rango(df: pd.DataFrame, 
                  columna: str, 
                  min_val: Optional[float] = None,
                  max_val: Optional[float] = None,
                  verbose: bool = True) -> pd.DataFrame:
    """
    Valida que los valores de una columna estén dentro del rango esperado.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame a validar
    columna : str
        Nombre de la columna a validar
    min_val : float, opcional
        Valor mínimo esperado
    max_val : float, opcional
        Valor máximo esperado
    verbose : bool, default True
        Si True, imprime resultados
        
    Retorna
    -------
    pd.DataFrame
        Registros fuera de rango (vacío si todo OK)
        
    Ejemplos
    --------
    >>> outliers = validar_rango(df, 'Gini', min_val=0, max_val=100)
    """
    if columna not in df.columns:
        raise ValueError(f"Columna '{columna}' no encontrada en DataFrame")
    
    # Filtrar valores no nulos
    datos_validos = df[df[columna].notna()]
    
    # Identificar valores fuera de rango
    fuera_rango = pd.DataFrame()
    
    if min_val is not None:
        fuera_rango = pd.concat([fuera_rango, datos_validos[datos_validos[columna] < min_val]])
    
    if max_val is not None:
        fuera_rango = pd.concat([fuera_rango, datos_validos[datos_validos[columna] > max_val]])
    
    fuera_rango = fuera_rango.drop_duplicates()
    
    if verbose:
        print("=" * 80)
        print(f"VALIDACIÓN DE RANGO: {columna}")
        print("=" * 80)
        rango = f"[{min_val if min_val is not None else '-∞'}, {max_val if max_val is not None else '+∞'}]"
        print(f"Rango esperado: {rango}")
        print(f"Registros validados: {len(datos_validos):,}")
        
        if len(fuera_rango) > 0:
            print(f"\n[ERR] {len(fuera_rango)} registro(s) fuera de rango:")
            print(fuera_rango.to_string(index=False))
        else:
            print(f"\n[OK] Todos los valores están dentro del rango esperado")
    
    return fuera_rango


def ensure_proportion_scale(df: pd.DataFrame, columna: str = 'Gini', upper_threshold: float = 1.1) -> pd.DataFrame:
    """
    Asegura que una métrica de tipo proporción (0-1) esté en escala 0-1.

    - Si la columna no existe se lanza ValueError.
    - Si el valor máximo es mayor que `upper_threshold`, asumimos escala 0-100 y dividimos por 100.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame que contiene la columna.
    columna : str
        Nombre de la columna a normalizar.
    upper_threshold : float
        Umbral para detectar escala en 0-100 (por defecto 1.1).

    Retorna
    -------
    pd.DataFrame
        DataFrame actualizado con la columna normalizada (cambiado en copia).
    """
    if columna not in df.columns:
        raise ValueError(f"Columna '{columna}' no encontrada en DataFrame")

    df = df.copy()
    max_val = df[columna].dropna().max()
    if pd.notna(max_val) and max_val > upper_threshold:
        # Convertir de % a proporción
        df[columna] = df[columna] / 100.0
        print(f"[INFO] Normalizando '{columna}' de escala 0-100 a 0-1 (max original: {max_val})")
    return df


def validar_continuidad_temporal(df: pd.DataFrame, 
                                  columna_año: str = 'Anio',
                                  agrupacion: Optional[List[str]] = None,
                                  verbose: bool = True) -> Dict[str, List[int]]:
    """
    Valida que existan datos continuos para cada año (detecta gaps temporales).
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame a validar
    columna_año : str, default 'Año'
        Nombre de la columna con el año
    agrupacion : List[str], opcional
        Columnas para agrupar (ej: ['Tipo_Hogar', 'CCAA'])
    verbose : bool, default True
        Si True, imprime resultados
        
    Retorna
    -------
    Dict[str, List[int]]
        Diccionario con grupos y años faltantes
        
    Notas
    -----
    Esta función detecta gaps en series temporales pero NO distingue entre:
    - Gaps por errores de ETL
    - Gaps legítimos (ej: cambios metodológicos, datos no publicados)
    """
    # Normalize year column: accept 'Anio' or fallback to 'Año'
    if columna_año not in df.columns:
        if 'Año' in df.columns:
            # Create a temporary 'Anio' column mapped from 'Año'
            df = df.copy()
            df['Anio'] = df['Año']
            columna_año = 'Anio'
            if verbose:
                print("[WARN] Se renombró 'Año' a 'Anio' temporalmente para validación")
        else:
            raise ValueError(f"Columna '{columna_año}' no encontrada en DataFrame")
    
    gaps_encontrados = {}
    
    if agrupacion:
        # Validar por grupo
        grupos = df.groupby(agrupacion)[columna_año].apply(lambda x: sorted(x.unique())).to_dict()
        
        for grupo, años in grupos.items():
            años_esperados = list(range(min(años), max(años) + 1))
            años_faltantes = sorted(set(años_esperados) - set(años))
            
            if años_faltantes:
                grupo_str = str(grupo) if not isinstance(grupo, tuple) else " | ".join(map(str, grupo))
                gaps_encontrados[grupo_str] = años_faltantes
    else:
        # Validar serie completa
        años_disponibles = sorted(df[columna_año].unique())
        años_esperados = list(range(min(años_disponibles), max(años_disponibles) + 1))
        años_faltantes = sorted(set(años_esperados) - set(años_disponibles))
        
        if años_faltantes:
            gaps_encontrados['Serie completa'] = años_faltantes
    
    if verbose:
        print("=" * 80)
        print("VALIDACIÓN DE CONTINUIDAD TEMPORAL")
        print("=" * 80)
        print(f"Columna año: {columna_año}")
        if agrupacion:
            print(f"Agrupación: {', '.join(agrupacion)}")
        
        if gaps_encontrados:
            print(f"\n[ERR] {len(gaps_encontrados)} grupo(s) con años faltantes:")
            for grupo, años in gaps_encontrados.items():
                print(f"\n  {grupo}:")
                print(f"    Años faltantes: {años}")
        else:
            print(f"\n[OK] Continuidad temporal completa (sin gaps)")
    
    return gaps_encontrados


def validar_consistencia_valores(df: pd.DataFrame,
                                  columnas_comparar: List[Tuple[str, str, str]],
                                  verbose: bool = True) -> pd.DataFrame:
    """
    Valida consistencia lógica entre columnas (ej: Gini_Antes > Gini_Despues).
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame a validar
    columnas_comparar : List[Tuple[str, str, str]]
        Lista de tuplas (col1, operador, col2)
        Operadores: '>', '<', '>=', '<=', '==', '!='
    verbose : bool, default True
        Si True, imprime resultados
        
    Retorna
    -------
    pd.DataFrame
        Registros con inconsistencias
        
    Ejemplos
    --------
    >>> inconsistencias = validar_consistencia_valores(
    ...     df, 
    ...     [('Gini_Antes', '>', 'Gini_Despues'),
    ...      ('S80S20_Antes', '>=', 'S80S20_Despues')]
    ... )
    """
    operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y
    }
    
    inconsistencias = pd.DataFrame()
    
    for col1, op, col2 in columnas_comparar:
        if col1 not in df.columns or col2 not in df.columns:
            warnings.warn(f"Columnas '{col1}' o '{col2}' no encontradas")
            continue
        
        if op not in operadores:
            raise ValueError(f"Operador '{op}' no válido. Use: {list(operadores.keys())}")
        
        # Filtrar registros con valores válidos en ambas columnas
        datos_validos = df[(df[col1].notna()) & (df[col2].notna())].copy()
        
        # Aplicar operador
        datos_validos['_cumple_condicion'] = operadores[op](datos_validos[col1], datos_validos[col2])
        
        # Identificar inconsistencias
        incons = datos_validos[~datos_validos['_cumple_condicion']].drop('_cumple_condicion', axis=1)
        
        if len(incons) > 0:
            incons['_condicion_violada'] = f"{col1} {op} {col2}"
            inconsistencias = pd.concat([inconsistencias, incons])
    
    inconsistencias = inconsistencias.drop_duplicates()
    
    if verbose:
        print("=" * 80)
        print("VALIDACIÓN DE CONSISTENCIA LÓGICA")
        print("=" * 80)
        print(f"Condiciones evaluadas: {len(columnas_comparar)}")
        
        if len(inconsistencias) > 0:
            print(f"\n[ERR] {len(inconsistencias)} registro(s) con inconsistencias:")
            print(inconsistencias.to_string(index=False))
        else:
            print(f"\n[OK] Todas las condiciones se cumplen")
    
    return inconsistencias


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN DE OUTLIERS
# =============================================================================

def plot_outliers_boxplot(df: pd.DataFrame,
                          columnas: List[str],
                          agrupacion: Optional[str] = None,
                          figsize: Tuple[int, int] = (14, 6),
                          title: Optional[str] = None) -> plt.Figure:
    """
    Visualiza outliers usando boxplots para una o varias columnas.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    columnas : List[str]
        Columnas numéricas a visualizar
    agrupacion : str, opcional
        Columna categórica para agrupar (ej: 'Año', 'CCAA')
    figsize : Tuple[int, int], default (14, 6)
        Tamaño de la figura
    title : str, opcional
        Título del gráfico
        
    Retorna
    -------
    plt.Figure
        Figura de matplotlib
    """
    n_cols = len(columnas)
    fig, axes = plt.subplots(1, n_cols, figsize=figsize)
    
    if n_cols == 1:
        axes = [axes]
    
    for idx, col in enumerate(columnas):
        if col not in df.columns:
            axes[idx].text(0.5, 0.5, f"Columna '{col}'\nno encontrada", 
                          ha='center', va='center')
            axes[idx].set_xticks([])
            axes[idx].set_yticks([])
            continue
        
        if agrupacion and agrupacion in df.columns:
            df.boxplot(column=col, by=agrupacion, ax=axes[idx])
            axes[idx].set_xlabel(agrupacion)
        else:
            df.boxplot(column=col, ax=axes[idx])
        
        axes[idx].set_title(col)
        axes[idx].set_ylabel('Valor')
    
    if title:
        fig.suptitle(title, fontsize=14, y=1.02)
    
    plt.tight_layout()
    return fig


def plot_outliers_temporal(df: pd.DataFrame,
                           columna_valor: str,
                           columna_año: str = 'Anio',
                           agrupacion: Optional[str] = None,
                           destacar_anomalias: bool = True,
                           umbral_z_score: float = 2.5,
                           figsize: Tuple[int, int] = (14, 6),
                           title: Optional[str] = None) -> plt.Figure:
    """
    Visualiza evolución temporal de una variable y destaca anomalías.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_valor : str
        Columna numérica a visualizar
    columna_año : str, default 'Año'
        Columna con el año
    agrupacion : str, opcional
        Columna para separar series (ej: 'CCAA', 'Tipo_Hogar')
    destacar_anomalias : bool, default True
        Si True, resalta puntos con z-score > umbral
    umbral_z_score : float, default 2.5
        Umbral de z-score para considerar anomalía
    figsize : Tuple[int, int], default (14, 6)
        Tamaño de la figura
    title : str, opcional
        Título del gráfico
        
    Retorna
    -------
    plt.Figure
        Figura de matplotlib
    """
    # Normalize year column
    df, columna_año = _normalize_year_column(df, columna_año, verbose=True)
    if columna_año is None:
        raise ValueError("No se encontró columna de año ('Anio'|'Año'|'Anyo') en el DataFrame")
    fig, ax = plt.subplots(figsize=figsize)
    
    if agrupacion and agrupacion in df.columns:
        for grupo in sorted(df[agrupacion].unique()):
            datos = df[df[agrupacion] == grupo].sort_values(columna_año)
            ax.plot(datos[columna_año], datos[columna_valor], 
                   marker='o', label=grupo, linewidth=2, markersize=6)
            
            if destacar_anomalias:
                # Calcular z-score para el grupo
                z_scores = np.abs((datos[columna_valor] - datos[columna_valor].mean()) / datos[columna_valor].std())
                anomalias = datos[z_scores > umbral_z_score]
                
                if len(anomalias) > 0:
                    ax.scatter(anomalias[columna_año], anomalias[columna_valor],
                             color='red', s=100, marker='X', zorder=5,
                             label=f'{grupo} - Anomalías' if grupo == sorted(df[agrupacion].unique())[0] else '')
    else:
        datos = df.sort_values(columna_año)
        ax.plot(datos[columna_año], datos[columna_valor], 
               marker='o', linewidth=2, markersize=6, color='steelblue')
        
        if destacar_anomalias:
            z_scores = np.abs((datos[columna_valor] - datos[columna_valor].mean()) / datos[columna_valor].std())
            anomalias = datos[z_scores > umbral_z_score]
            
            if len(anomalias) > 0:
                ax.scatter(anomalias[columna_año], anomalias[columna_valor],
                         color='red', s=100, marker='X', zorder=5, label='Anomalías')
    
    ax.set_xlabel(columna_año, fontsize=12)
    ax.set_ylabel(columna_valor, fontsize=12)
    ax.set_title(title if title else f'Evolución Temporal: {columna_valor}', fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def resumen_validacion_completo(df: pd.DataFrame,
                                 columnas_numericas: List[str],
                                 columna_año: str = 'Anio',
                                 agrupacion: Optional[List[str]] = None,
                                 umbral_nulos: float = 5.0) -> Dict[str, any]:
    """
    Ejecuta todas las validaciones y devuelve un resumen completo.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame a validar
    columnas_numericas : List[str]
        Columnas numéricas a validar
    columna_año : str, default 'Año'
        Columna con el año
    agrupacion : List[str], opcional
        Columnas para agrupar en validación temporal
    umbral_nulos : float, default 5.0
        Umbral de porcentaje de nulos
        
    Retorna
    -------
    Dict[str, any]
        Diccionario con resultados de todas las validaciones
    """
    print("\n" + "=" * 80)
    print("🔍 RESUMEN COMPLETO DE VALIDACIÓN")
    print("=" * 80)
    
    resultados = {}
    # Normalize year column for all the validations
    df, columna_año = _normalize_year_column(df, columna_año, verbose=True)
    if columna_año is None:
        raise ValueError("No se encontró columna de año ('Anio'|'Año'|'Anyo') en el DataFrame")
    
    # 1. Validar nulos
    print("\n1️⃣ Validación de nulos...")
    resultados['nulos'] = validar_nulos(df, columnas_numericas, umbral_nulos, verbose=True)
    
    # 2. Validar rangos (asumiendo rangos lógicos para indicadores comunes)
    print("\n2️⃣ Validación de rangos...")
    rangos_validar = {
        'Gini': (0, 100),
        'S80S20': (0, None),
        'Tasa_Riesgo_Pobreza': (0, 100),
        'AROPE': (0, 100)
    }
    
    resultados['rangos'] = {}
    for col in columnas_numericas:
        if col in rangos_validar:
            min_val, max_val = rangos_validar[col]
            fuera_rango = validar_rango(df, col, min_val, max_val, verbose=False)
            if len(fuera_rango) > 0:
                resultados['rangos'][col] = fuera_rango
                print(f"  [ERR] {col}: {len(fuera_rango)} valores fuera de rango")
            else:
                print(f"  [OK] {col}: Todos los valores en rango esperado")
    
    # 3. Validar continuidad temporal
    print("\n3️⃣ Validación de continuidad temporal...")
    resultados['gaps_temporales'] = validar_continuidad_temporal(
        df, columna_año, agrupacion, verbose=True
    )
    
    print("\n" + "=" * 80)
    print("[OK] Validación completa finalizada")
    print("=" * 80)
    
    return resultados


# =============================================================================
# FUNCIONES DE DOCUMENTACIÓN DE LIMITACIONES
# =============================================================================

def generar_reporte_limitaciones(df: pd.DataFrame,
                                  fuente: str,
                                  periodo: str,
                                  limitaciones_conocidas: Optional[List[str]] = None) -> str:
    """
    Genera un reporte en texto de las limitaciones del dataset.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame analizado
    fuente : str
        Fuente de los datos (ej: 'INE', 'Eurostat')
    periodo : str
        Periodo temporal de los datos
    limitaciones_conocidas : List[str], opcional
        Lista de limitaciones conocidas específicas del dataset
        
    Retorna
    -------
    str
        Reporte de limitaciones en formato texto
    """
    reporte = []
    reporte.append("=" * 80)
    reporte.append("[REPORT] LIMITACIONES Y ADVERTENCIAS METODOLÓGICAS")
    reporte.append("=" * 80)
    
    reporte.append(f"\n🔹 Fuente de datos: {fuente}")
    reporte.append(f"🔹 Periodo analizado: {periodo}")
    reporte.append(f"🔹 Registros totales: {len(df):,}")
    
    # Nulos
    pct_nulos_global = (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
    reporte.append(f"\n[WARN]  Porcentaje global de nulos: {pct_nulos_global:.2f}%")
    
    # Limitaciones conocidas
    if limitaciones_conocidas:
        reporte.append("\n[WARN]  Limitaciones conocidas:")
        for idx, lim in enumerate(limitaciones_conocidas, 1):
            reporte.append(f"   {idx}. {lim}")
    
    reporte.append("\n" + "=" * 80)
    
    return "\n".join(reporte)


if __name__ == "__main__":
    print("Módulo de validación cargado correctamente.")
    print("Funciones disponibles:")
    print("  - validar_nulos()")
    print("  - validar_rango()")
    print("  - validar_continuidad_temporal()")
    print("  - validar_consistencia_valores()")
    print("  - plot_outliers_boxplot()")
    print("  - plot_outliers_temporal()")
    print("  - resumen_validacion_completo()")
    print("  - generar_reporte_limitaciones()")
