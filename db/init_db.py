import sqlite3
import os

def execute_sql_file(conn, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn.executescript(sql)

def init_db(db_path='library.db', sql_dir='db'):
    conn = sqlite3.connect(db_path)
    sql_files = [
        'system.sql',
        'region.sql',
        'genre.sql',
        'game_title.sql',
        'game_version.sql'
    ]
    for filename in sql_files:
        filepath = os.path.join(sql_dir, filename)
        print(f"Executing {filepath}")
        execute_sql_file(conn, filepath)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
