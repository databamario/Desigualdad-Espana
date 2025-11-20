import os
import subprocess
import sys
from pathlib import Path
import pickle
import pandas as pd


def run_encoding_check():
    repo_root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, str(repo_root / "scripts" / "check_pickles_encoding.py")]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(repo_root))
    return proc


def test_encoding_check_detects_mojibake(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    cache_dir = repo_root / "outputs" / "pickle_cache"
    test_pkl = cache_dir / "test_mojibake.pkl"
    df = pd.DataFrame({"Tipo_Metrica": ["Ã­ndice", "VariaciÃ³n anual"]})
    with open(test_pkl, "wb") as f:
        pickle.dump(df, f)
    try:
        proc = run_encoding_check()
        print(proc.stdout)
        print(proc.stderr)
        assert proc.returncode != 0
        assert (
            "mojibake" in proc.stdout.lower()
            or "mojibake" in proc.stderr.lower()
            or "m ojibake" in proc.stdout.lower()
        )
    finally:
        if test_pkl.exists():
            test_pkl.unlink()
