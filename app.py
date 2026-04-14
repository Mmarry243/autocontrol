from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Função criada pelo aluno para conectar ao banco
def abrir_conexao():
    conexao = sqlite3.connect('oficina.db')
    conexao.row_factory = sqlite3.Row
    return conexao

# Função para criar as tabelas da oficina
def iniciar_oficina():
    conexao = abrir_conexao()
    conexao.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo TEXT NOT NULL,
            placa TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

@app.route('/')
def home():
    # Variável 'pesquisa' em português
    pesquisa = request.args.get('search', '').strip()
    conexao = abrir_conexao()
    
    if pesquisa:
        # Comando para filtrar nome, modelo ou placa
        comando_sql = "SELECT * FROM veiculos WHERE nome LIKE ? OR modelo LIKE ? OR placa LIKE ?"
        lista_carros = conexao.execute(comando_sql, (f'%{pesquisa}%', f'%{pesquisa}%', f'%{pesquisa}%')).fetchall()
    else:
        # Pega todos os carros se não tiver busca
        lista_carros = conexao.execute('SELECT * FROM veiculos').fetchall()
    
    conexao.close()
    # Enviando 'busca_cliente' para o HTML
    return render_template('index.html', veiculos=lista_carros, busca_cliente=pesquisa)

@app.route('/cadastrar', methods=['POST'])
def salvar_veiculo():
    nome = request.form.get('nome')
    modelo = request.form.get('modelo')
    placa = request.form.get('placa')
    
    if nome and modelo and placa:
        conexao = abrir_conexao()
        conexao.execute('INSERT INTO veiculos (nome, modelo, placa) VALUES (?, ?, ?)', (nome, modelo, placa))
        conexao.commit()
        conexao.close()
    
    return redirect(url_for('home'))

@app.route('/excluir/<int:id>')
def remover_carro(id):
    try:
        conexao = abrir_conexao()
        conexao.execute('DELETE FROM veiculos WHERE id = ?', (id,))
        conexao.commit()
        conexao.close()
    except Exception as erro:
        print(f"Erro ao remover no sistema: {erro}")
    
    return redirect(url_for('home'))

if __name__ == "__main__":
    iniciar_oficina()
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
