import sqlite3
import os

db_path = '/app/db_data/database.db'

if os.path.exists(db_path):
    print("✅ DB already exists, skipping init.")
    exit(0)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        amount INTEGER,
        date TEXT
    )
""")
conn.commit()
conn.close()
print("✅ DB initialized.")

