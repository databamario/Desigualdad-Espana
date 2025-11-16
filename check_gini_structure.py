import pyodbc
import pandas as pd
from utils.config import DB_CONNECTION_STRING

# Connect to database
conn = pyodbc.connect(DB_CONNECTION_STRING)

# Get first 20 records to understand structure
query = "SELECT TOP 20 * FROM EUROSTAT_Gini_Ranking ORDER BY geo_name, Año, Gini"

df = pd.read_sql(query, conn)

print("=" * 80)
print("EUROSTAT_Gini_Ranking - Sample Records")
print("=" * 80)
print(df.to_string(index=False))

print("\n" + "=" * 80)
print("Column Names:")
print("=" * 80)
for col in df.columns:
    print(f"  - {col}")

# Check for duplicates
query_dup = """
SELECT geo_name, Año, COUNT(*) as count, 
       STRING_AGG(CAST(Gini AS VARCHAR), ', ') as gini_values
FROM EUROSTAT_Gini_Ranking
GROUP BY geo_name, Año
HAVING COUNT(*) > 1
ORDER BY geo_name, Año
"""

df_dup = pd.read_sql(query_dup, conn)

print("\n" + "=" * 80)
print(f"Duplicate (geo_name, Año) combinations: {len(df_dup)}")
print("=" * 80)
if not df_dup.empty:
    print(df_dup.head(10).to_string(index=False))

conn.close()
