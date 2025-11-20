import os
import subprocess
import sys
from pathlib import Path


def run_check(args=None, env_overrides=None):
    repo_root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, str(repo_root / 'scripts' / 'check_pickles.py')]
    if args:
        cmd.extend(args)
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(repo_root), env=env)
    return proc


def test_default_encoding_ok():
    proc = run_check()
    print(proc.stdout)
    print(proc.stderr)
    assert proc.returncode == 0


def test_cp1252_encoding_ok():
    proc = run_check(env_overrides={'PYTHONIOENCODING': 'cp1252'})
    print(proc.stdout)
    print(proc.stderr)
    assert proc.returncode == 0


def test_cp1252_noemoji_ok():
    proc = run_check(args=['--no-emoji'], env_overrides={'PYTHONIOENCODING': 'cp1252'})
    print(proc.stdout)
    print(proc.stderr)
    assert proc.returncode == 0
