from pathlib import Path
import pandas as pd
import sqlite3
from typing import Dict
import unicodedata


def normalize_text_for_merge(val):
    if pd.isna(val):
        return val
    s = str(val)
    s = s.strip()
    s = s.replace('_', ' ')
    s = s.replace('.', '')
    s = ' '.join(s.split())
    # Remove diacritics
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    s = s.lower()
    return s


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply common column name normalizations used across notebooks/tests.

    - Estandarizar a 'Anio' (ASCII-safe, sin tildes)
    - Ensure Gini, inflation columns are present
    - Normalize IPC/Inflacion columns names
    """
    # Convertir 'Año' → 'Anio' (ASCII-safe)
    if 'Año' in df.columns:
        if 'Anio' in df.columns:
            df = df.drop(columns=['Año'])
        else:
            df = df.rename(columns={'Año': 'Anio'})
    if 'IPC_Medio_Anual' in df.columns and 'Inflacion_Anual_%' not in df.columns:
        df['Inflacion_Anual_%'] = df['IPC_Medio_Anual']
    if 'Inflacion_Anual_%' in df.columns and 'IPC_Medio_Anual' not in df.columns:
        df['IPC_Medio_Anual'] = df['Inflacion_Anual_%']
    if 'IPC_Indice' in df.columns and 'Inflacion_Sectorial_%' not in df.columns:
        df['Inflacion_Sectorial_%'] = df['IPC_Indice']
    if 'Inflacion_Sectorial_%' in df.columns and 'IPC_Indice' not in df.columns:
        df['IPC_Indice'] = df['Inflacion_Sectorial_%']
    return df


def normalize_umbral_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure df_umbral has consistent columns, create aliases where necessary.

    This handles variants observed in pickles & DB tables where the threshold
    column may be named `Umbral_Euros`, `Umbral_Pobreza_Euros` or `Umbral_Real_€_Base`.
    Also ensure 'Tipo_Hogar' and 'Año/Anio' are present.
    """
    # canonical column names we want:
    # 'Año', 'Anio', 'Tipo_Hogar', 'Umbral_Euros', 'Umbral_Real_€_Base'
    if 'Año' in df.columns and 'Anio' not in df.columns:
        df['Anio'] = df['Año']
    if 'Anio' in df.columns and 'Año' not in df.columns:
        df['Año'] = df['Anio']
    # Map older names to canonical ones
    if 'Umbral_Pobreza_Euros' in df.columns and 'Umbral_Euros' not in df.columns:
        df['Umbral_Euros'] = df['Umbral_Pobreza_Euros']
    if 'Umbral_Real_€_Base' in df.columns and 'Umbral_Euros' not in df.columns:
        # keep Umbral_Real_€_Base but provide Umbral_Euros alias
        df['Umbral_Euros'] = df['Umbral_Real_€_Base']
    if 'Umbral_Euros' in df.columns and 'Umbral_Real_€_Base' not in df.columns:
        df['Umbral_Real_€_Base'] = df['Umbral_Euros']
    if 'Tipo_Hogar' not in df.columns:
        df['Tipo_Hogar'] = 'Hogares de una persona'
    # Relax: ensure Umbral columns exist as floats
    if 'Umbral_Euros' in df.columns:
        try:
            df['Umbral_Euros'] = df['Umbral_Euros'].astype(float)
        except Exception:
            pass
    if 'Umbral_Real_€_Base' in df.columns:
        try:
            df['Umbral_Real_€_Base'] = df['Umbral_Real_€_Base'].astype(float)
        except Exception:
            pass
    return df


def normalize_categoria_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize categoria groups for IPC and Gasto tables to canonical `Categoria_ECOICOP` values.

    This moves the repeated mapping logic from tests into a single helper.
    """
    mapeo_categorias = {
        'Alimentos_y_bebidas_no_alcohólicas.': 'Alimentos y bebidas no alcohólicas',
        'Bebidas_alcohólicas_y_tabaco.': 'Bebidas alcohólicas y tabaco',
        'Vestido_y_calzado.': 'Vestido y calzado',
        'Vivienda,_agua,_electricidad,_gas_y_otros_combustibles.': 'Vivienda, agua, electricidad, gas y otros combustibles',
        'Muebles,_artículos_del_hogar_y_artículos_para_el_mantenimiento_corriente_del_hogar.': 'Muebles, artículos del hogar y artículos para el mantenimiento corriente del hogar',
        'Sanidad.': 'Sanidad',
        'Transporte.': 'Transporte',
        'Comunicaciones.': 'Comunicaciones',
        'Ocio_y_cultura.': 'Ocio y cultura',
        'Enseñanza.': 'Enseñanza',
        'Restaurantes_y_hoteles.': 'Restaurantes y hoteles',
        'Otros_bienes_y_servicios.': 'Otros bienes y servicios'
    }
    norm_output_to_output = {normalize_text_for_merge(v): v for v in mapeo_categorias.values()}
    norm_key_to_output = {normalize_text_for_merge(k): v for k, v in mapeo_categorias.items()}
    if 'Categoria_ECOICOP' in df.columns:
        df['Categoria_ECOICOP'] = df['Categoria_ECOICOP'].apply(lambda x: norm_output_to_output.get(normalize_text_for_merge(x), x))
    if 'Grupo_Gasto' in df.columns:
        df['Categoria_ECOICOP'] = df['Grupo_Gasto'].map(mapeo_categorias)
        mask = df['Categoria_ECOICOP'].isna()
        if mask.any():
            df.loc[mask, 'Categoria_ECOICOP'] = df.loc[mask, 'Grupo_Gasto'].apply(lambda x: norm_key_to_output.get(normalize_text_for_merge(x), x))
    return df


def load_pickles_to_namespace(pickle_dir: Path, mapping: Dict[str, str] = None):
    """Load pickles into global namespace variables based on mapping.

    Args:
        pickle_dir: Path to outputs/pickle_cache
        mapping: dict varname -> pickle filename
    Returns:
        dict of varname -> DataFrame
    """
    if mapping is None:
        mapping = {
            'df_ipc_sectorial': 'df_ipc_sectorial.pkl',
            'df_gasto': 'df_epf_gasto.pkl',
            'df_ipc_nacional': 'df_ipc_anual.pkl',
            'df_arope_edad': 'df_arope_edad_sexo.pkl',
            'df_gini_ccaa': 'df_gini_ccaa.pkl',
            'df_renta': 'df_renta_decil.pkl',
            'df_carencia': 'df_carencia_material.pkl',
        }
    results = {}
    pickle_dir = Path(pickle_dir)
    for var, pkl in mapping.items():
        p = pickle_dir / pkl
        if p.exists():
            df = pd.read_pickle(p)
            # normalize column names: Año -> Anio (ASCII-safe)
            if 'Año' in df.columns:
                if 'Anio' in df.columns:
                    df = df.drop(columns=['Año'])
                else:
                    df = df.rename(columns={'Año': 'Anio'})
            # Standardize inflation column names
            if 'IPC_Medio_Anual' in df.columns and 'Inflacion_Anual_%' not in df.columns:
                # Some pickles may use IPC_Medio_Anual which is index-like; use it as Inflacion_Anual_% if present
                df['Inflacion_Anual_%'] = df['IPC_Medio_Anual']
            if 'Inflacion_Anual_%' in df.columns and 'IPC_Medio_Anual' not in df.columns:
                df['IPC_Medio_Anual'] = df['Inflacion_Anual_%']
            # Sectorial: ensure IPC_Indice exists when Inflation column exists and vice versa
            if 'IPC_Indice' in df.columns and 'Inflacion_Sectorial_%' not in df.columns:
                df['Inflacion_Sectorial_%'] = df['IPC_Indice']
            if 'Inflacion_Sectorial_%' in df.columns and 'IPC_Indice' not in df.columns:
                df['IPC_Indice'] = df['Inflacion_Sectorial_%']
            # ensure Gini column name present
            if 'Gini' in df.columns:
                df['Gini'] = df['Gini']
            # Apply general normalizations
            df = normalize_columns(df)
            # Normalize categories (if applicable)
            df = normalize_categoria_columns(df)
            # If this is the Umbral table, apply Umbral normalization
            if var == 'df_umbral' or 'umbral' in p.name.lower():
                df = normalize_umbral_dataframe(df)
            # If the var is df_pivot_deciles, ensure decile labels are normalized
            if var == 'df_pivot_deciles':
                try:
                    df = normalize_decile_columns(df)
                except Exception:
                    pass
            # If the var is df_renta, also derive df_pivot_deciles for convenience
            if var == 'df_renta':
                try:
                    dr = df.copy()
                    if 'Año' in dr.columns and 'Anio' not in dr.columns:
                        dr['Anio'] = dr['Año']
                    # Choose the column to use for pivot values:
                    # Prefer explicit 'Valor', then any column that contains 'Renta', 'Media', 'Mean', or a numeric column.
                    val_col = None
                    if 'Valor' in dr.columns:
                        val_col = 'Valor'
                    else:
                        # case-insensitive search for likely columns
                        col_lc = [c.lower() for c in dr.columns]
                        for candidate in ('renta', 'media', 'mean', 'valor', 'median', 'mediana'):
                            for i, c in enumerate(col_lc):
                                if candidate in c:
                                    val_col = dr.columns[i]
                                    break
                            if val_col is not None:
                                break
                    # If still not found, fallback to the first numeric column excluding the Decil/Anio columns
                    if val_col is None:
                        numeric_cols = [c for c in dr.select_dtypes(include=['number']).columns if str(c).lower() not in ('anio', 'año')]
                        # Exclude Decil column if present
                        numeric_cols = [c for c in numeric_cols if 'decil' not in str(c).lower()]
                        val_col = numeric_cols[0] if numeric_cols else None
                    if val_col is not None and 'Decil' in dr.columns:
                        pivot = dr.pivot_table(index='Anio', columns='Decil', values=val_col)
                        try:
                            pivot = normalize_decile_columns(pivot)
                        except Exception:
                            pass
                        results['df_pivot_deciles'] = pivot
                except Exception:
                    pass
            # If the var is df_arope_edad, derive a yearly series for AROPE (df_arope_anual)
            if var == 'df_arope_edad':
                try:
                    da = df.copy()
                    # Ensure a year alias exists
                    if 'Año' in da.columns and 'Anio' not in da.columns:
                        da['Anio'] = da['Año']
                    if 'Anio' in da.columns and 'Año' not in da.columns:
                        da['Año'] = da['Anio']
                    # Choose value column
                    val_col = 'Valor' if 'Valor' in da.columns else None
                    if val_col is None:
                        col_lc = [c.lower() for c in da.columns]
                        for candidate in ('valor','arope','indice'):
                            for i, c in enumerate(col_lc):
                                if candidate in c:
                                    val_col = da.columns[i]
                                    break
                            if val_col is not None:
                                break
                    # derive annual AROPE only when present
                    if val_col is not None and 'Indicador' in da.columns and 'Sexo' in da.columns and 'Edad' in da.columns:
                        da_n = da[(da.get('Sexo') == 'Total') & (da.get('Edad') == 'Total') & (da.get('Indicador') == 'AROPE')]
                        idx_col = 'Año' if 'Año' in da_n.columns else 'Anio' if 'Anio' in da_n.columns else None
                        if idx_col is not None:
                            da_n = da_n.groupby(idx_col)[val_col].mean().reset_index()
                            da_n.rename(columns={val_col: 'AROPE_%'}, inplace=True)
                            da_n = add_year_aliases(da_n)
                            results['df_arope_anual'] = da_n
                except Exception:
                    pass
            results[var] = df
    return results


def create_sqlite_from_pickles(pickle_dir: Path, sqlite_path: Path, table_mapping: Dict[str, str] = None):
    """Create a sqlite DB with tables from pickles.

    Args:
        pickle_dir: Path to pickle cache
        sqlite_path: path to sqlite db to create
        table_mapping: mapping pickle filename -> table name
    """
    pickle_dir = Path(pickle_dir)
    sqlite_path = Path(sqlite_path)
    conn = sqlite3.connect(str(sqlite_path))
    if table_mapping is None:
        table_mapping = {
            'df_ipc_sectorial.pkl': 'INE_IPC_Sectorial_ECOICOP',
            'df_epf_gasto.pkl': 'INE_Gasto_Medio_Hogar_Quintil',
            'df_ipc_anual.pkl': 'INE_IPC_Nacional',
            'df_arope_edad_sexo.pkl': 'INE_AROPE_Edad_Sexo',
            'df_gini_ccaa.pkl': 'INE_Gini_S80S20_CCAA',
            'df_renta_decil.pkl': 'INE_Renta_Media_Decil',
            'df_carencia_material.pkl': 'INE_Carencia_Material_Decil',
        }
    for pkl_name, table in table_mapping.items():
        pkl = pickle_dir / pkl_name
        if pkl.exists():
            df = pd.read_pickle(pkl)
            # Normalize df columns
            df = normalize_columns(df)
            # If this relates to Umbral table, normalize Umbral columns
            if 'umbral' in pkl_name.lower() or table.lower().startswith('ine_umbral'):
                df = normalize_umbral_dataframe(df)
            # If this is an IPC or Gasto table, normalize category column
            if 'ipc' in pkl_name.lower() or 'gasto' in pkl_name.lower() or table.lower().startswith('ine_ipc') or table.lower().startswith('ine_gasto'):
                df = normalize_categoria_columns(df)
            df.to_sql(table, conn, if_exists='replace', index=False)
    conn.close()


def add_year_aliases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza columnas de año a 'Anio' (ASCII-safe).
    
    Usa después de operaciones groupby/pivot que pueden crear columnas 'Año'.
    
    Estrategia: Convertir 'Año' → 'Anio' para evitar problemas encoding.
    
    Args:
        df: DataFrame to standardize year column in
        
    Returns:
        DataFrame with only 'Anio' column (no 'Año')
    """
    if 'Año' in df.columns:
        if 'Anio' in df.columns:
            df = df.drop(columns=['Año'])
        else:
            df = df.rename(columns={'Año': 'Anio'})
    return df


def normalize_decile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize pivot table column labels for deciles to canonical 'D{n}' format.

    Handles column names like integers (1..10), strings ('1', 'Decil 1'), or already
    formatted 'D1' strings.
    """
    if not hasattr(df, 'columns'):
        return df
    import re
    def _to_d(c):
        s = str(c)
        # Don't treat indicator-like names such as 'S80/S20' or 's80s20' as deciles.
        # These contain the substring 's80' (case-insensitive) and are not decile labels.
        if re.search(r"s80", s, re.I):
            return s
        m = re.search(r"(\d+)", s)
        if m:
            return f"D{m.group(1)}"
        if s.upper().startswith('D') and s[1:].isdigit():
            return s
        return s
    try:
        df = df.copy()
        # If MultiIndex columns, try to extract the decile part from tuple elements
        if hasattr(df.columns, 'nlevels') and df.columns.nlevels > 1:
            new_cols = []
            for c in df.columns:
                # c is a tuple
                found = None
                for part in c:
                    d = _to_d(part)
                    if isinstance(d, str) and d.upper().startswith('D') and d[1:].isdigit():
                        found = d
                        break
                if found is None:
                    # fallback: join tuple and try to convert
                    new_cols.append(_to_d('_'.join([str(x) for x in c])))
                else:
                    new_cols.append(found)
            df.columns = new_cols
        else:
            df.rename(columns={c: _to_d(c) for c in df.columns}, inplace=True)
    except Exception:
        pass
    
    # Apply year aliasing after column operations
    return add_year_aliases(df)
