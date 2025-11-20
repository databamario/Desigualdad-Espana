#!/usr/bin/env python3
"""
Check pickles for corrupted strings (mojibake or replacement chars).
Exits with code 1 if corruption is detected.
"""
from pathlib import Path
import pickle
import sys
import re
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def find_project_root():
    p = Path.cwd()
    while p != p.parent:
        if (p / ".git").exists() or (p / "README.md").exists():
            return p
        p = p.parent
    return Path.cwd()


def scan_pickle_for_mojibake(pickle_path: Path) -> List[str]:
    issues = []
    try:
        df = pickle.load(open(pickle_path, "rb"))
        if df is None or getattr(df, "empty", False):
            return issues
        # Convert to strings and search for common mojibake patterns
        # Wider detection: any 'Ã' followed by a char, 'Â', 'â', Unicode replacement char or common 'Â€' sequences
        mojibake_patterns = [r"Ã.", r"Â", r"â", r"�", r"\ufffd", r"Â€", r"â\u20ac"]
        regex = re.compile("|".join(mojibake_patterns))

        # Check object dtype columns
        for col in df.select_dtypes(include=["object"]).columns:
            # Sample values to limit memory, but scan all if small
            values = df[col].astype(str)
            if any(values.str.contains(regex, na=False)):
                issues.append(f"Column {col} contains mojibake sequences")
    except Exception as e:
        issues.append(f"Error reading pickle {pickle_path.name}: {e}")
    return issues


def main():
    project_root = find_project_root()
    cache_dir = project_root / "outputs" / "pickle_cache"
    pickles = list(Path(cache_dir).glob("*.pkl"))
    all_issues = {}
    for p in pickles:
        issues = scan_pickle_for_mojibake(p)
        if issues:
            all_issues[p.name] = issues

    if all_issues:
        print("Mojibake / encoding issues detected in pickles:")
        for k, v in all_issues.items():
            print(f" - {k}:")
            for item in v:
                print(f"    - {item}")
        sys.exit(1)
    else:
        print("No encoding issues detected in pickles.")
        sys.exit(0)


if __name__ == "__main__":
    main()
