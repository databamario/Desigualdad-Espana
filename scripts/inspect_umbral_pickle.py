from pathlib import Path
import pandas as pd

pickle = Path("outputs") / "pickle_cache" / "df_umbral_limpio.pkl"
df = pd.read_pickle(pickle)
print(df.columns.tolist())
print(df.head().to_dict())
