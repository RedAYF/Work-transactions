import sqlite3

def initialize_db():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        user_id TEXT,
                        order_id TEXT,
                        amount REAL,
                        status TEXT
                     )''')
    conn.commit()
    conn.close()
