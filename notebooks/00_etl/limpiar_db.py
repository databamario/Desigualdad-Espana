import pyodbc
import sys
from pathlib import Path

# Añadir la ruta base del proyecto al sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config import DB_CONNECTION_STRING

conn = pyodbc.connect(DB_CONNECTION_STRING)
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
      AND TABLE_NAME NOT LIKE 'sys%'
    ORDER BY TABLE_NAME
""")
tablas = [r[0] for r in cursor.fetchall()]

print(f"[LIST] Tablas a eliminar: {len(tablas)}")
for t in tablas:
    print(f"  - {t}")

confirmacion = input("\n[WARN]  ¿Confirmar eliminación de TODAS las tablas? (escribir SI): ")

if confirmacion.strip().upper() == "SI":
    print("\n[INFO]  Eliminando tablas...")
    for tabla in tablas:
        try:
            cursor.execute(f"DROP TABLE {tabla}")
            print(f"  [OK] {tabla}")
        except Exception as e:
            print(f"  [ERR] {tabla}: {e}")
    
    conn.commit()
    print("\n[OK] Base de datos limpiada")
else:
    print("\n[ERR] Operación cancelada")

conn.close()
