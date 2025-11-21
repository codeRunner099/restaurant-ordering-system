import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "restaurant.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

os.makedirs(DB_DIR, exist_ok=True)

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()
conn.executescript(sql_script)
conn.commit()
conn.close()