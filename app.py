import tkinter as tk
import os
import sqlite3
import subprocess

from tkinter import messagebox
from Sistema.Banco_dados import Banco_de_dados

# Instanciando o objeto do banco de dados
banco = Banco_de_dados()

# Caminho do arquivo SQLite
FILE_BG_FUNCIONARIO = "Sistema/Banco_de_dados/Funcionario.db"

# Função para verificar e criar a tabela no banco de dados
def verificar_BG():
    if not os.path.exists(FILE_BG_FUNCIONARIO):
        # Chamando a função de criar a tabela
        nome_banco = "Funcionario"
        nome_tabela = "funcionarios"
        colunas = 3
        nome_colunas = ["id", "nome", "email", "senha","cargo"]
        tipo_colunas = ["INTEGER PRIMARY KEY AUTOINCREMENT", "TEXT", "TEXT", "TEXT", "TEXT"]
        banco.criar_tabela(nome_banco, nome_tabela, colunas, nome_colunas, tipo_colunas)
    else:
        print("Tabela já existe")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Entrada aplicaçao")
        self.geometry("500x300")

        self.titulo = tk.Label(self, text="Login", font=("Arial", 20))
        self.email_login = tk.Label(self, text="Email")
        self.senha_login = tk.Label(self, text="Senha")
        self.logar_btn = tk.Button(self, text="Logar", command=self.logar)
        
        self.email_entry = tk.Entry(self)
        self.senha_entry = tk.Entry(self, show="*")

        self.titulo.place(x=200, y=10, anchor="center")
        self.email_login.place(x=50, y=100)
        self.senha_login.place(x=50, y=150)
        self.email_entry.place(x=150, y=100)
        self.senha_entry.place(x=150, y=150)
        self.logar_btn.place(x=200, y=200, anchor="center")

    def logar(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        conn = sqlite3.connect(FILE_BG_FUNCIONARIO)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM funcionarios WHERE email = '{email}' AND senha = '{senha}'")
        dados = cursor.fetchall()

        if dados:
            FILE = "Sistema/main.py"
            FILE_temp_session = "Sistema/temp_session.json"
            with open(FILE_temp_session, "w") as f:
                f.write(f'{{"email": "{email}", "senha": "{senha}"}}')
            subprocess.Popen(f"python {FILE}")
            #encerra a aplicação
            self.destroy()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos")

        conn.close()

if __name__ == "__main__":
    verificar_BG()  
    app = App()
    app.mainloop()
