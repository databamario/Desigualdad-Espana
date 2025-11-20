"""
Framework de Validación de Datos
=================================
Funciones reutilizables para validar la calidad de datos del proyecto Desigualdad Social.

Autor: Proyecto Desigualdad Social ETL
Fecha: 2025-11-13
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


class ValidationReport:
    """Clase para almacenar resultados de validación"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.errors = []
        self.warnings = []
        self.info = []
        self.timestamp = datetime.now().isoformat()
        self.records_original = 0
        self.records_excluded = 0

    def add_error(self, message: str):
        self.errors.append(f"[ERR] {message}")

    def add_warning(self, message: str):
        self.warnings.append(f"[WARN] {message}")

    def add_info(self, message: str):
        self.info.append(f"[INFO] {message}")

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_report(self):
        print("=" * 80)
        print(f"REPORTE DE VALIDACIÓN: {self.table_name}")
        print("=" * 80)

        if self.info:
            print("\n[INFO] INFORMACIÓN:")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print("\n[WARN] ADVERTENCIAS:")
            for msg in self.warnings:
                print(f"  {msg}")

        if self.errors:
            print("\n[ERR] ERRORES CRÍTICOS:")
            for msg in self.errors:
                print(f"  {msg}")
        else:
            print("\n[OK] Sin errores críticos")

        print("=" * 80)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el reporte a diccionario para JSON"""
        return {
            "table_name": self.table_name,
            "timestamp": self.timestamp,
            "records_original": self.records_original,
            "records_excluded": self.records_excluded,
            "records_clean": self.records_original - self.records_excluded,
            "errors": [msg.replace("[ERR] ", "") for msg in self.errors],
            "warnings": [
                msg.replace("[WARN] ", "").replace("[WARN]  ", "")
                for msg in self.warnings
            ],
            "info": [msg.replace("[INFO] ", "") for msg in self.info],
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "status": "FAILED" if self.has_errors() else "PASSED",
        }

    def save_json(self, output_dir: str = "../../data/validated/logs"):
        """Guarda el reporte en formato JSON"""
        # Resolver ruta absoluta desde este archivo (utils/)
        if not Path(output_dir).is_absolute():
            # Obtener directorio raíz del proyecto (2 niveles arriba desde utils/)
            project_root = Path(__file__).parent.parent
            output_path = project_root / "data" / "validated" / "logs"
        else:
            output_path = Path(output_dir)

        output_path.mkdir(parents=True, exist_ok=True)

        filename = (
            output_path
            / f"{self.table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        print(f"[REPORT] Report saved: {filename}")
        return str(filename)

    def save_csv(self, output_dir: str = "../../data/validated/logs"):
        """Guarda el reporte en formato CSV"""
        # Resolver ruta absoluta desde este archivo (utils/)
        if not Path(output_dir).is_absolute():
            # Obtener directorio raíz del proyecto (2 niveles arriba desde utils/)
            project_root = Path(__file__).parent.parent
            output_path = project_root / "data" / "validated" / "logs"
        else:
            output_path = Path(output_dir)

        output_path.mkdir(parents=True, exist_ok=True)

        filename = (
            output_path
            / f"{self.table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        # Crear DataFrame con los resultados
        records = []
        for msg in self.errors:
            records.append(
                {
                    "type": "ERROR",
                    "message": msg.replace("[ERR] ", "").replace("❌ ", ""),
                }
            )
        for msg in self.warnings:
            records.append(
                {
                    "type": "WARNING",
                    "message": msg.replace("[WARN] ", "")
                    .replace("⚠️ ", "")
                    .replace("⚠️  ", ""),
                }
            )
        for msg in self.info:
            records.append(
                {
                    "type": "INFO",
                    "message": msg.replace("[INFO] ", "")
                    .replace("✅ ", "")
                    .replace("ℹ️ ", ""),
                }
            )

        df = pd.DataFrame(records)
        df["table_name"] = self.table_name
        df["timestamp"] = self.timestamp

        df.to_csv(filename, index=False, encoding="utf-8")

        print(f"[REPORT] Report saved: {filename}")
        return str(filename)


def check_schema(
    df: pd.DataFrame,
    expected_columns: List[str],
    expected_types: Optional[Dict[str, type]] = None,
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida que el DataFrame tenga las columnas y tipos esperados.

    Args:
        df: DataFrame a validar
        expected_columns: Lista de columnas esperadas
        expected_types: Diccionario {columna: tipo_esperado}
        report: Objeto ValidationReport para logging

    Returns:
        True si pasa la validación, False si falla
    """
    valid = True

    # Normalize year column names: accept 'Anio' or fallback to 'Año'/'Anyo'
    if "Anio" not in df.columns and "Año" in df.columns:
        df = df.copy()
        df["Anio"] = df["Año"]
    if "Anio" not in df.columns and "Anyo" in df.columns:
        df = df.copy()
        df["Anio"] = df["Anyo"]
    # Verificar columnas
    missing_cols = set(expected_columns) - set(df.columns)
    extra_cols = set(df.columns) - set(expected_columns)

    if missing_cols:
        msg = f"Columnas faltantes: {missing_cols}"
        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        valid = False

    if extra_cols:
        msg = f"Columnas inesperadas: {extra_cols}"
        if report:
            report.add_warning(msg)
        else:
            print(f"[WARN] {msg}")

    # Verificar tipos
    if expected_types and valid:
        for col, expected_type in expected_types.items():
            if col in df.columns:
                actual_type = df[col].dtype
                # Simplificación: comparar familias de tipos
                if expected_type == int and not pd.api.types.is_integer_dtype(
                    actual_type
                ):
                    msg = f"Columna '{col}': tipo {actual_type}, esperado integer"
                    if report:
                        report.add_error(msg)
                    else:
                        print(f"[ERR] {msg}")
                    valid = False
                elif expected_type == float and not pd.api.types.is_float_dtype(
                    actual_type
                ):
                    msg = f"Columna '{col}': tipo {actual_type}, esperado float"
                    if report:
                        report.add_error(msg)
                    else:
                        print(f"[ERR] {msg}")
                    valid = False
                elif (
                    expected_type == str
                    and not pd.api.types.is_string_dtype(actual_type)
                    and not pd.api.types.is_object_dtype(actual_type)
                ):
                    msg = f"Columna '{col}': tipo {actual_type}, esperado string"
                    if report:
                        report.add_error(msg)
                    else:
                        print(f"[ERR] {msg}")
                    valid = False

    if valid and report:
        report.add_info(f"Esquema correcto: {len(df.columns)} columnas")

    return valid


def check_uniqueness(
    df: pd.DataFrame, primary_key: List[str], report: Optional[ValidationReport] = None
) -> bool:
    """
    Valida que no haya duplicados en la clave primaria.

    Args:
        df: DataFrame a validar
        primary_key: Lista de columnas que forman la clave primaria
        report: Objeto ValidationReport para logging

    Returns:
        True si no hay duplicados, False si hay duplicados
    """
    # Normalize year column names
    if "Anio" not in df.columns and "Año" in df.columns:
        df = df.copy()
        df["Anio"] = df["Año"]
    if "Anio" not in df.columns and "Anyo" in df.columns:
        df = df.copy()
        df["Anio"] = df["Anyo"]
    duplicates = df.duplicated(subset=primary_key, keep=False).sum()

    if duplicates > 0:
        msg = f"Duplicados encontrados en clave {tuple(primary_key)}: {duplicates} registros"
        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        return False

    if report:
        report.add_info(
            f"Unicidad verificada: clave {tuple(primary_key)} sin duplicados"
        )

    return True


def check_nulls(
    df: pd.DataFrame,
    critical_columns: Optional[List[str]] = None,
    max_null_percent: float = 0.05,
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida que no haya valores nulos excesivos.

    Args:
        df: DataFrame a validar
        critical_columns: Columnas críticas que NO deben tener nulos
        max_null_percent: Porcentaje máximo aceptable de nulos (default 5%)
        report: Objeto ValidationReport para logging

    Returns:
        True si pasa la validación, False si falla
    """
    valid = True

    # Verificar columnas críticas (0% nulos permitidos)
    if critical_columns:
        for col in critical_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    msg = f"Columna crítica '{col}' tiene {null_count} nulos ({null_count/len(df)*100:.2f}%)"
                    if report:
                        report.add_error(msg)
                    else:
                        print(f"[ERR] {msg}")
                    valid = False

    # Verificar todas las columnas contra umbral
    nulls = df.isnull().sum()
    for col, null_count in nulls.items():
        if null_count > 0:
            null_percent = null_count / len(df)
            if null_percent > max_null_percent:
                msg = f"Columna '{col}': {null_count} nulos ({null_percent*100:.2f}%) supera umbral {max_null_percent*100}%"
                if report:
                    report.add_warning(msg)
                else:
                    print(f"[WARN] {msg}")

    if valid and report:
        total_nulls = df.isnull().sum().sum()
        report.add_info(
            f"Valores faltantes: {total_nulls} nulos totales dentro de umbrales"
        )

    return valid


def check_conditional_nulls(
    df: pd.DataFrame,
    conditional_rules: Dict[str, dict],
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida reglas de nulos condicionados: por ejemplo, una columna puede ser NULL solo
    cuando otra columna tiene ciertos valores (ej. 'Inflacion_Sectorial_%' NULL solo
    cuando 'Tipo_Metrica' == 'Índice').

    Args:
        df: DataFrame a validar
        conditional_rules: Diccionario donde la clave es el nombre de la columna
                           a validar y el valor es un dict con parámetros:
                           {
                               'cond_column': str,
                               'cond_null_substrings': List[str]
                           }
        report: ValidationReport

    Returns:
        True si todas las reglas se cumplen, False en caso contrario
    """
    valid = True

    for col, rule in conditional_rules.items():
        cond_col = rule.get("cond_column")
        substrings = rule.get("cond_null_substrings", [])

        if col not in df.columns:
            msg = f"Columna condicional '{col}' no encontrada en DataFrame"
            if report:
                report.add_warning(msg)
            else:
                print(f"[WARN] {msg}")
            # skip this rule
            continue

        if cond_col not in df.columns:
            msg = f"Columna condicional de referencia '{cond_col}' no encontrada en DataFrame"
            if report:
                report.add_warning(msg)
            else:
                print(f"[WARN] {msg}")
            continue

        # Generar máscara donde se espera NULL en la columna objetivo (por coincidencia de substring)
        mask_expected_null = pd.Series(False, index=df.index)
        for subs in substrings:
            mask_expected_null = mask_expected_null | df[cond_col].astype(
                str
            ).str.contains(subs, case=False, na=False)

        # Fuera de la máscara: la columna objetivo NO debe ser NULL
        non_null_outside_expected = df[~mask_expected_null][col].isnull().sum()
        if non_null_outside_expected > 0:
            msg = f"Columna '{col}' tiene {non_null_outside_expected} nulos fuera de condición (referencia {cond_col} not in {substrings})"
            if report:
                report.add_error(msg)
            else:
                print(f"[ERR] {msg}")
            valid = False

        # Dentro de la máscara: la columna objetivo debería ser NULL (si hay no-NULL puede ser anomalía)
        non_null_inside_expected = df[mask_expected_null][col].notnull().sum()
        if non_null_inside_expected > 0:
            msg = f"Columna '{col}' tiene {non_null_inside_expected} valores NO-null donde se esperaba NULL (referencia {cond_col} in {substrings})"
            if report:
                report.add_warning(msg)
            else:
                print(f"[WARN] {msg}")
            # depending on strictness we may still consider this a failure; mark as warning only

    if valid and report:
        report.add_info("Reglas condicionales de nulos verificadas correctamente")

    return valid


def _fix_mojibake(s: str) -> str:
    """Attempt to fix common mojibake sequences from CP1252 -> UTF-8 mismatches.
    This is a best-effort approach using common sequences such as 'Ã¡' -> 'á'.
    """
    if s is None:
        return s
    if not isinstance(s, str):
        s = str(s)
    replacements = {
        "Ã¡": "á",
        "Ã©": "é",
        "Ã­": "í",
        "Ã³": "ó",
        "Ãº": "ú",
        "Ã±": "ñ",
        "Ã‘": "Ñ",
        "Ã€": "À",
        "Ã´": "ô",
        "Ã“": "Ó",
        "â": "'",
        "\ufffd": "",
        "�": "",
        "Â€": "€",
        "â‚¬": "€",
    }
    for k, v in replacements.items():
        if k in s:
            s = s.replace(k, v)
    return s


def normalize_text(s: str) -> str:
    """Normalize text for stable comparisons.

    - Attempts to fix common mojibake sequences
    - Strips diacritics (returns ascii/lowercased normalized string)
    - Collapses whitespace
    """
    import unicodedata

    if s is None:
        return s
    s = _fix_mojibake(s)
    # Remove Unicode replacement character if still present
    s = s.replace("\ufffd", "").replace("�", "")
    # Remove non-letter and non-digit characters (keep spaces)
    import unicodedata as _ud

    s = "".join(c for c in s if _ud.category(c)[0] in ("L", "N") or c.isspace())
    # Normalize NFC to composed, then remove accents
    s_nfkd = unicodedata.normalize("NFKD", s)
    s_ascii = "".join([c for c in s_nfkd if not unicodedata.combining(c)])
    s_clean = " ".join(s_ascii.strip().split())
    return s_clean


def normalize_tipo_metrica(series: pd.Series) -> pd.Series:
    """Convert a serie of Tipo_Metrica to canonical values.

    Recognizes and maps a variety of variants to canonical Spanish metric names:
        - 'Variación anual'
        - 'Variación mensual'
        - 'Variación en lo que va de año'
        - 'Índice'
    """
    if series is None:
        return series

    def _map_value(v):
        if pd.isna(v):
            return v
        s = normalize_text(v).lower()
        # Accept variants like 'variación anual', 'variacin anual', 'variacion anual', etc.
        s = (
            s.replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace("ñ", "n")
        )
        s = " ".join(s.split())

        # Basic substring checks
        if "variacion anual" in s or ("variacion" in s and "anual" in s):
            return "Variación anual"
        if "variacion mensual" in s or ("variacion" in s and "mensual" in s):
            return "Variación mensual"
        if (
            "variacion en lo que va de ano" in s
            or "variacion en lo que va de año" in s
            or "variacion en lo que va de" in s
            or ("variacion" in s and "ano" in s)
            or ("variacion" in s and "va de" in s)
        ):
            return "Variación en lo que va de año"
        if "indice" in s or "ndice" in s:
            return "Índice"
        return v

    return series.apply(_map_value)


def check_range(
    df: pd.DataFrame,
    column: str,
    min_val: float,
    max_val: float,
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida que los valores de una columna estén en el rango esperado.

    Args:
        df: DataFrame a validar
        column: Nombre de la columna
        min_val: Valor mínimo esperado
        max_val: Valor máximo esperado
        report: Objeto ValidationReport para logging

    Returns:
        True si todos los valores están en rango, False si hay outliers
    """
    if column not in df.columns:
        msg = f"Columna '{column}' no existe"
        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        return False

    out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]

    if len(out_of_range) > 0:
        msg = f"Columna '{column}': {len(out_of_range)} valores fuera de rango [{min_val}, {max_val}]"
        actual_min = df[column].min()
        actual_max = df[column].max()
        msg += f" (rango real: [{actual_min:.2f}, {actual_max:.2f}])"

        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        return False

    if report:
        report.add_info(f"Columna '{column}': valores en rango [{min_val}, {max_val}]")

    return True


def check_time_coherence(
    df: pd.DataFrame,
    year_column: str = "Año",
    value_column: str = "Valor",
    max_variation_percent: float = 200.0,
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida que no haya saltos temporales ilógicos.

    Args:
        df: DataFrame a validar
        year_column: Nombre de la columna de año
        value_column: Nombre de la columna de valor
        max_variation_percent: Variación máxima permitida entre años consecutivos (%)
        report: Objeto ValidationReport para logging

    Returns:
        True si la serie es coherente, False si hay saltos anormales
    """
    if year_column not in df.columns or value_column not in df.columns:
        msg = f"Columnas '{year_column}' o '{value_column}' no existen"
        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        return False

    # Ordenar por año
    df_sorted = df.sort_values(year_column)

    # Calcular variación año a año
    df_sorted["variacion"] = df_sorted[value_column].pct_change() * 100

    # Detectar saltos anormales
    anomalies = df_sorted[df_sorted["variacion"].abs() > max_variation_percent]

    if len(anomalies) > 0:
        msg = f"Saltos temporales anormales detectados: {len(anomalies)} casos con variación > {max_variation_percent}%"
        if report:
            report.add_warning(msg)
        else:
            print(f"[WARN] {msg}")
        return False

    if report:
        report.add_info(f"Coherencia temporal: sin saltos > {max_variation_percent}%")

    return True


def check_year_continuity(
    df: pd.DataFrame,
    year_column: str = "Año",
    expected_years: Optional[range] = None,
    report: Optional[ValidationReport] = None,
) -> bool:
    """
    Valida que no falten años en la serie temporal.

    Args:
        df: DataFrame a validar
        year_column: Nombre de la columna de año
        expected_years: Rango de años esperados
        report: Objeto ValidationReport para logging

    Returns:
        True si la serie es continua, False si faltan años
    """
    if year_column not in df.columns:
        msg = f"Columna '{year_column}' no existe"
        if report:
            report.add_error(msg)
        else:
            print(f"[ERR] {msg}")
        return False

    actual_years = set(df[year_column].unique())

    if expected_years:
        expected_set = set(expected_years)
        missing_years = expected_set - actual_years
        extra_years = actual_years - expected_set

        if missing_years:
            msg = f"Años faltantes: {sorted(missing_years)}"
            if report:
                report.add_warning(msg)
            else:
                print(f"[WARN] {msg}")
            return False

        if extra_years:
            msg = f"Años inesperados: {sorted(extra_years)}"
            if report:
                report.add_info(msg)
            else:
                print(f"[INFO] {msg}")
    else:
        # Si no se especifican años esperados, verificar continuidad
        min_year = min(actual_years)
        max_year = max(actual_years)
        expected_set = set(range(min_year, max_year + 1))
        missing_years = expected_set - actual_years

        if missing_years:
            msg = f"Años faltantes en el rango [{min_year}, {max_year}]: {sorted(missing_years)}"
            if report:
                report.add_warning(msg)
            else:
                print(f"[WARN] {msg}")
            return False

    if report:
        report.add_info(f"Continuidad temporal: {len(actual_years)} años completos")

    return True
