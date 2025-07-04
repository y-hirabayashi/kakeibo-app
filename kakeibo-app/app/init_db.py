import sqlite3

conn = sqlite3.connect('kakeibo.db')
c = conn.cursor()
c.execute('''
CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount INTEGER,
    note TEXT
)
''')
conn.commit()
conn.close()
print("DB初期化しました。")
