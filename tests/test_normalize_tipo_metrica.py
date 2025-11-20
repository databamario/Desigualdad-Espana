import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.validation_framework import normalize_tipo_metrica
import scripts.normalize_tipo_metrica as script_mod
import pickle


def test_normalize_handles_mojibake_and_accents():
    s = pd.Series(["Variación anual", "VariaciÃ³n anual", "Variacion anual", "Índice", "�ndice"])
    normalized = normalize_tipo_metrica(s)
    assert normalized.iloc[0] == 'Variación anual'
    assert normalized.iloc[1] == 'Variación anual'
    assert normalized.iloc[2] == 'Variación anual'
    assert normalized.iloc[3] == 'Índice'
    assert normalized.iloc[4] == 'Índice'


def test_normalize_cli_inplace_and_backup(tmp_path):
    # Create a temporary cache dir
    cache_dir = tmp_path / 'cache'
    cache_dir.mkdir()
    # Create a sample dataframe and pickle
    df = pd.DataFrame({'Tipo_Metrica': ['VariaciÃ³n anual', 'Índice']})
    pfile = cache_dir / 'test.pkl'
    with open(pfile, 'wb') as f:
        pickle.dump(df, f)

    # Run in-place with backup
    backup_dir = tmp_path / 'backups'
    script_mod.main(cache_dir=cache_dir, in_place=True, backup_dir=backup_dir)

    # Backup should exist
    backup_files = list(backup_dir.glob('*.pkl'))
    assert len(backup_files) == 1

    # Original file should be updated (normalized)
    df_after = pickle.load(open(pfile, 'rb'))
    assert df_after['Tipo_Metrica'].iloc[0] == 'Variación anual'


def test_normalize_cli_output_dir(tmp_path):
    cache_dir = tmp_path / 'cache'
    cache_dir.mkdir()
    df = pd.DataFrame({'Tipo_Metrica': ['VariaciÃ³n anual', 'Índice']})
    pfile = cache_dir / 'test2.pkl'
    with open(pfile, 'wb') as f:
        pickle.dump(df, f)

    output_dir = tmp_path / 'normalized'
    script_mod.main(cache_dir=cache_dir, in_place=False, output_dir=output_dir)

    # Output file should exist and normalized
    out_files = list(output_dir.glob('*.pkl'))
    assert len(out_files) == 1
    df_out = pickle.load(open(out_files[0], 'rb'))
    assert df_out['Tipo_Metrica'].iloc[0] == 'Variación anual'

    # Original file should be unchanged
    df_orig = pickle.load(open(pfile, 'rb'))
    assert df_orig['Tipo_Metrica'].iloc[0] == 'VariaciÃ³n anual'


def test_normalize_cli_dry_run(tmp_path):
    cache_dir = tmp_path / 'cache'
    cache_dir.mkdir()
    df = pd.DataFrame({'Tipo_Metrica': ['VariaciÃ³n anual', 'Índice']})
    pfile = cache_dir / 'test3.pkl'
    with open(pfile, 'wb') as f:
        pickle.dump(df, f)

    backup_dir = tmp_path / 'backups'
    output_dir = tmp_path / 'normalized'
    # Dry-run should not create backups or output files
    script_mod.main(cache_dir=cache_dir, in_place=True, backup_dir=backup_dir, dry_run=True)
    assert not any(backup_dir.glob('*.pkl'))
    assert not any((output_dir).glob('*.pkl'))
    # Original unchanged
    df_orig = pickle.load(open(pfile, 'rb'))
    assert df_orig['Tipo_Metrica'].iloc[0] == 'VariaciÃ³n anual'
