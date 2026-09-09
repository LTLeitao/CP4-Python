import sqlite3

DATABASE = 'academia.db'

def get_connection():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            plan_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            status_reason TEXT,
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        );
    ''')

    plans = [
        ("básico",),
        ("premium",),
        ("empresarial",),
        ("diária",)
    ]

    cursor.execute("SELECT COUNT(*) FROM plans")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO plans (type) 
            VALUES (?)
        """, plans)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")