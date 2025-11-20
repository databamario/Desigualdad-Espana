import sqlite3

conn = sqlite3.connect("tmp_test_db.sqlite")
cur = conn.cursor()
cur.execute("PRAGMA table_info('INE_Umbral_Pobreza_Hogar')")
print(cur.fetchall())
conn.close()
