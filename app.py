from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo TEXT NOT NULL,
            placa TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM veiculos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')@app.route('/')
def home():
    search = request.args.get('search', '').strip() # Pega o termo e remove espaços extras
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    
    if search:
        # Busca inteligente: procura em nome OU placa
        query = "SELECT * FROM veiculos WHERE nome LIKE ? OR placa LIKE ?"
        cursor.execute(query, (f'%{search}%', f'%{search}%'))
    else:
        # Se não tiver busca, mostra tudo normalmente
        cursor.execute('SELECT * FROM veiculos')
        
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', veiculos=dados)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
