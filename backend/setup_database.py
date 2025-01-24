#!/usr/bin/env python3.11

import sqlite3

conn = sqlite3.connect('herbs.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS herbs (
    id INTEGER PRIMARY KEY,
    common_name TEXT,
    scientific_name TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS uses (
    id INTEGER PRIMARY KEY,
    description TEXT UNIQUE
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS herb_use (
    herb_id INTEGER,
    use_id INTEGER,
    FOREIGN KEY (herb_id) REFERENCES herbs (id),
    FOREIGN KEY (use_id) REFERENCES uses (id),
    PRIMARY KEY (herb_id, use_id)
)
''')

conn.commit()
conn.close()
print("Database tables created successfully.")
