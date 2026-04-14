from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Função para conectar ao banco de forma segura
def get_db_connection():
    conn = sqlite3.connect('oficina.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo TEXT NOT NULL,
            placa TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    search = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    if search:
        # Busca inteligente: funciona para Nome, Modelo ou Placa
        query = "SELECT * FROM veiculos WHERE nome LIKE ? OR modelo LIKE ? OR placa LIKE ?"
        veiculos = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        veiculos = conn.execute('SELECT * FROM veiculos').fetchall()
    
    conn.close()
    return render_template('index.html', veiculos=veiculos)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    modelo = request.form.get('modelo')
    placa = request.form.get('placa')
    
    if nome and modelo and placa:
        conn = get_db_connection()
        conn.execute('INSERT INTO veiculos (nome, modelo, placa) VALUES (?, ?, ?)', (nome, modelo, placa))
        conn.commit()
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/excluir/<int:id>')
def excluir(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM veiculos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao excluir: {e}")
    
    return redirect(url_for('home'))

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
