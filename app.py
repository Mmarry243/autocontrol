from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco e criar a tabela se não existir
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

@app.route('/')
def home():
    # Esta parte busca os dados no banco para mostrar no site
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM veiculos')
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', veiculos=dados)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    modelo = request.form.get('modelo')
    placa = request.form.get('placa')

    # Salva no arquivo do banco de dados
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO veiculos (nome, modelo, placa) VALUES (?, ?, ?)', (nome, modelo, placa))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db() # Cria o banco assim que o código roda
    app.run(debug=True)