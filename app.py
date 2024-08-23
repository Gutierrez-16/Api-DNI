from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
import logging
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
DATABASE = 'database.db'

class ApisNetPe:
    BASE_URL = "https://api.apis.net.pe"

    def __init__(self, token: str) -> None:
        self.token = token

    def _get(self, path: str, params: dict) -> dict:
        url = f"{self.BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Referer": "https://apis.net.pe/api-tipo-cambio.html"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"API error: {response.status_code} - {response.text}")
            return {}

    def get_person(self, dni: str) -> dict:
        return self._get("/v2/reniec/dni", {"numero": dni})

# Leer el token desde el archivo .env
APIS_TOKEN = os.getenv('APIS_TOKEN')
api_consultas = ApisNetPe(APIS_TOKEN)

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            email TEXT,
            direccion TEXT,
            celular TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    error = None

    if request.method == 'POST':
        dni = request.form.get('dni')
        if dni:
            person_data = api_consultas.get_person(dni)
            if person_data:
                apellido_paterno = person_data.get('apellidoPaterno', '')
                apellido_materno = person_data.get('apellidoMaterno', '')
                nombre = person_data.get('nombres', '')

                if apellido_paterno and apellido_materno and nombre:
                    return render_template('index.html', dni=dni, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, nombre=nombre, error=error)
                error = 'Datos incompletos en la respuesta de la API.'

    cursor.execute('SELECT * FROM persons')
    persons = cursor.fetchall()
    conn.close()

    return render_template('index.html', persons=persons, error=error)

@app.route('/add', methods=['POST'])
def add_person():
    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    apellido_paterno = request.form.get('apellido_paterno')
    apellido_materno = request.form.get('apellido_materno')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    celular = request.form.get('celular')

    if dni and nombre and apellido_paterno and apellido_materno:
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO persons (dni, nombre, apellido_paterno, apellido_materno, email, direccion, celular)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (dni, nombre, apellido_paterno, apellido_materno, email, direccion, celular))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            logging.error(f"Error inserting data: Duplicate DNI {dni}")
            return redirect(url_for('index', error='El DNI ya está registrado.'))

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_person(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM persons WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error deleting data: {e}")
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if request.method == 'POST':
        dni = request.form.get('dni')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        celular = request.form.get('celular')

        cursor.execute('''
            UPDATE persons
            SET dni = ?, nombre = ?, apellido_paterno = ?, apellido_materno = ?, email = ?, direccion = ?, celular = ?
            WHERE id = ?
        ''', (dni, nombre, apellido_paterno, apellido_materno, email, direccion, celular, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute('SELECT * FROM persons WHERE id = ?', (id,))
        person = cursor.fetchone()
        conn.close()
        return render_template('edit.html', person=person)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")
