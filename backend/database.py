import sqlite3

conn = sqlite3.connect("interview.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    score INTEGER,
    skills TEXT
)
""")

conn.commit()