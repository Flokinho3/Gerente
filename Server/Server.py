from flask import Flask, render_template, request, jsonify
import sqlite3
import time
import os
from database import get_db, init_db, close_db

# Criando a instância do Flask
app = Flask(__name__)

# Inicializa o banco de dados na primeira vez
@app.before_request
def initialize_db():
    init_db()


@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Função para verificar se o dispositivo é móvel
def eh_dispositivo_movel(user_agent):
    mobile_keywords = ['iphone', 'android', 'blackberry', 'windows phone', 'mobile', 'kindle', 'ipad']
    return any(keyword in user_agent.lower() for keyword in mobile_keywords)

# Função para salvar ou atualizar as informações dos usuários
def atualizar_usuarios(ip_cliente, dispositivo, horas, pagina):
    db = get_db()
    cursor = db.cursor()

    # Verificar se o IP já existe no banco de dados
    cursor.execute("SELECT id FROM users WHERE ip = ?", (ip_cliente,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        # Atualizar o usuário existente
        cursor.execute("""
            UPDATE users 
            SET dispositivo = ?, horas = ?, pagina = ?, ultimo_dispositivo = ? 
            WHERE ip = ?
        """, (dispositivo, horas, pagina, dispositivo if dispositivo != "Desconhecido" else None, ip_cliente))
        print(f"Usuário {ip_cliente} atualizado.")
    else:
        # Adicionar um novo usuário
        cursor.execute("""
            INSERT INTO users (ip, dispositivo, horas, pagina, ultimo_dispositivo) 
            VALUES (?, ?, ?, ?, ?)
        """, (ip_cliente, dispositivo, horas, pagina, dispositivo if dispositivo != "Desconhecido" else None))
        print(f"Novo usuário {ip_cliente} inserido.")
    
    # Salvar as alterações no banco de dados
    db.commit()

# Rota principal
@app.route('/')
def index():
    # Obter o IP do cliente e o User-Agent
    ip_cliente = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    horas = time.strftime("%H:%M:%S", time.localtime())

    # Verificar se o dispositivo é móvel ou PC
    if eh_dispositivo_movel(user_agent):
        dispositivo = 'Celular'
    else:
        dispositivo = 'PC'

    # Atualizar o banco de dados com as informações do usuário
    atualizar_usuarios(ip_cliente, dispositivo, horas, "Home")

    # Consultar todos os usuários no banco de dados
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT ip, dispositivo, horas, pagina, ultimo_dispositivo FROM users")
    users = cursor.fetchall()

    # Renderizar o template com os dados
    return render_template('index.html', users=users)

# Rota para atualizar a aba ativa
@app.route('/atualizar_aba', methods=['POST'])
def atualizar_aba():
    dados = request.get_json()
    if not dados or 'aba' not in dados:
        return jsonify({"status": "error", "message": "Aba não fornecida"}), 400

    ip_cliente = request.remote_addr
    aba = dados['aba']

    # Atualizar a aba ativa no banco de dados
    horas = time.strftime("%H:%M:%S", time.localtime())
    atualizar_usuarios(ip_cliente, "Desconhecido", horas, aba)

    return jsonify({"status": "success", "ip": ip_cliente, "aba": aba})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
