import sqlite3
import os

db_path = '/app/db_data/database.db'

# ディレクトリがなければ作成
os.makedirs(db_dir, exist_ok=True)

if os.path.exists(db_path):
    print("✅ DB already exists, skipping init.")
    exit(0)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount INTEGER,
        note TEXT
    )
""")
conn.commit()
conn.close()
print("✅ DB initialized.")
