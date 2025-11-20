import json
from pathlib import Path

nb_path = Path(
    "notebooks/01_analisis_nacional/02_analisis_indicadores_principales.ipynb"
)
nb = json.loads(nb_path.read_text(encoding="utf-8"))
for i, cell in enumerate(nb["cells"]):
    src = "".join(cell.get("source", []))
    if (
        "def __apply_compatibility_normalization" in src
        or "__apply_compatibility_normalization()" in src
    ):
        print("INDEX", i)
        print("type", cell.get("cell_type"))
        print("id", cell.get("id"))
        print("first 2 lines:\n", "\n".join(src.splitlines()[:2]))
        print("---")
