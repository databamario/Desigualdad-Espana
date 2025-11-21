import json

nb = json.load(
    open(
        "notebooks/01_analisis_nacional/03_analisis_inflacion_diferencial.ipynb",
        "r",
        encoding="utf-8",
    )
)

for i, cell in enumerate(nb["cells"]):
    source = cell.get("source", [])
    source_str = "".join(source) if isinstance(source, list) else source
    if "df_arope_anual.columns" in source_str:
        print(f"Cell {i}:")
        print("".join(source[:10]))
        print("...")
        break
