import json
from pathlib import Path
import re

nb_path = Path(
    "notebooks/01_analisis_nacional/02_analisis_indicadores_principales.ipynb"
)
text = nb_path.read_text(encoding="utf-8")
for m in re.finditer(re.escape("df_gini_ccaa[Gini]"), text):
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    print("FOUND at", m.start(), "preview:", text[start:end])
else:
    print("No df_gini_ccaa[Gini] in file")

for m in re.finditer(re.escape("df_gini_ccaa['Gini']"), text):
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    print("FOUND QUOTED at", m.start(), "preview:", text[start:end])
