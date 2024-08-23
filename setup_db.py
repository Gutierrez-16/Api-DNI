import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            email TEXT NOT NULL,
            direccion TEXT NOT NULL,
            celular TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
