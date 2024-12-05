import sqlite3
from flask import g
from flask import current_app as app

DATABASE = 'Server/users.db'

def get_db():
    """Retorna a conexão com o banco de dados."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Para acessar os resultados como dicionários
    return db

def init_db():
    db = sqlite3.connect("Server/users.db")
    cursor = db.cursor()

    # Criando a tabela "users" caso ela não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            dispositivo TEXT NOT NULL,
            horas TEXT NOT NULL,
            pagina TEXT NOT NULL,
            ultimo_dispositivo TEXT
        )
    """)
    db.commit()
    db.close()


def close_db(error=None):
    """Fecha a conexão com o banco de dados."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
