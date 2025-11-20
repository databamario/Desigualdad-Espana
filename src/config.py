from pathlib import Path

# Repository root (assumes this module is under repo/src)
BASE_DIR = Path(__file__).resolve().parent.parent
# Common cache dir used by notebooks and scripts
CACHE_DIR = BASE_DIR / "outputs" / "pickle_cache"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


# Ensure CACHE_DIR exists at import time
ensure_dir(CACHE_DIR)
