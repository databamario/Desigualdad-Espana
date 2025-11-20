#!/usr/bin/env python3
"""
Normalize 'Tipo_Metrica' values in pickles (remove diacritics and fix mojibake).

Usage:
    python scripts/normalize_tipo_metrica.py --in-place
    python scripts/normalize_tipo_metrica.py --output-dir outputs/pickle_cache/normalized
    python scripts/normalize_tipo_metrica.py --in-place --backup-dir outputs/pickle_cache/backups/2025

Run `python scripts/normalize_tipo_metrica.py --help` for more options.
"""
import argparse
import pickle
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from utils.validation_framework import normalize_tipo_metrica


def find_project_root():
    p = Path.cwd()
    while p != p.parent:
        if (p / '.git').exists() or (p / 'README.md').exists():
            return p
        p = p.parent
    return Path.cwd()


def main(cache_dir=None, in_place=False, output_dir=None, backup_dir=None, dry_run=False):
    project_root = find_project_root()
    if cache_dir is None:
        cache_dir = project_root / 'outputs' / 'pickle_cache'
    cache_dir = Path(cache_dir)
    if output_dir is None and not in_place:
        output_dir = cache_dir / 'normalized'
    if backup_dir is None:
        backup_dir = cache_dir / 'backups' / datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(output_dir) if output_dir is not None else None
    backup_dir = Path(backup_dir)

    pickles = list(Path(cache_dir).glob('*.pkl'))
    updated = []

    for p in pickles:
        try:
            df = pickle.load(open(p, 'rb'))
            if isinstance(df, pd.DataFrame) and 'Tipo_Metrica' in df.columns:
                df = df.copy()
                df['Tipo_Metrica'] = normalize_tipo_metrica(df['Tipo_Metrica'])
                # Prepare target path
                if in_place:
                    target_path = p
                    # Make backup before overwriting
                    if not dry_run:
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        backup_path = backup_dir / p.name
                        shutil.copy2(p, backup_path)
                        print(f"Backed up {p.name} -> {backup_path}")
                else:
                    target_path = (output_dir / p.name)
                    if not dry_run:
                        output_dir.mkdir(parents=True, exist_ok=True)
                if not dry_run:
                    with open(target_path, 'wb') as f:
                        pickle.dump(df, f)
                    print(f"Wrote normalized pickle: {target_path}")
                updated.append(p.name)
        except Exception as e:
            print(f"Error processing {p}: {e}")
            continue

    print(f"Normalized Tipo_Metrica in {len(updated)} pickles")
    for u in updated:
        print(' -', u)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Normalize Tipo_Metrica in pickles')
    parser.add_argument('--cache-dir', '-c', help='Directory where pickles to normalize live (defaults to outputs/pickle_cache)')
    parser.add_argument('--in-place', '-i', action='store_true', help='Modify pickles in place (will create backups)')
    parser.add_argument('--output-dir', '-o', help='Where to write normalized pickles when not in-place')
    parser.add_argument('--backup-dir', '-b', help='Where to store backups when using --in-place')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be modified but do not write files')
    args = parser.parse_args()
    main(cache_dir=args.cache_dir, in_place=args.in_place, output_dir=args.output_dir, backup_dir=args.backup_dir, dry_run=args.dry_run)
