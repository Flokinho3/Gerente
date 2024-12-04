import tkinter as tk
import json
import os
import subprocess
from tkinter import messagebox

# Caminho do arquivo de configurações e sessão
FILE_CONFIG = "Sistema/Configuraçoes/Config_janela.json"
FILE_TEMP = "Sistema/temp_session.json"

class Sistema:
    def __init__(self):
        self.root = tk.Tk()
        config = self.carregar_config()

        # Configurando a janela com base no arquivo JSON
        if config:
            if config.get("modo") == "fullscreen":
                self.root.attributes("-fullscreen", True)
            else:
                largura = config.get("largura", 800)
                altura = config.get("altura", 600)
                self.root.geometry(f"{largura}x{altura}")
        else:
            self.root.geometry("800x600")

        self.root.title("Sistema de Vendas")

        # Sidebar
        self.sidebar_frame = tk.Frame(self.root, width=100, bg="lightgray")
        self.sidebar_frame.pack(side="left", fill="y")

        # Páginas
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Botões da Sidebar
        self.paginas = {
            "Inicio": self.inicio,
            "Cadastro": self.cadastro,
            "Sair": self.sair
        }

        for nome_pagina, funcao_pagina in self.paginas.items():
            if nome_pagina == "Sair":
                btn = tk.Button(self.sidebar_frame, text=nome_pagina.capitalize(), command=funcao_pagina, bg="red", fg="white")
                btn.pack(fill="x", pady=5, side="bottom")
            else:
                btn = tk.Button(self.sidebar_frame, text=nome_pagina.capitalize(), command=funcao_pagina, bg="lightblue")
                btn.pack(fill="x", pady=5)

        # Página inicial
        self.inicio()

        self.root.mainloop()

    def limpar_frame(self):
        """Remove todos os widgets do frame principal."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def inicio(self):
        """Página inicial."""
        self.limpar_frame()
        tk.Label(self.main_frame, text="Bem-vindo à página inicial!", font=("Arial", 16), bg="white").pack(pady=20)

    def cadastro(self):
        """Página de cadastro."""
        self.limpar_frame()
        tk.Label(self.main_frame, text="Página de cadastro", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Entry(self.main_frame).pack(pady=10)  # Campo de exemplo
        tk.Button(self.main_frame, text="Salvar", bg="green", fg="white").pack(pady=10)

    def carregar_config(self):
        """Carrega as configurações do arquivo JSON ou cria um padrão."""
        if os.path.exists(FILE_CONFIG):
            try:
                with open(FILE_CONFIG, "r") as f:
                    config = json.load(f)
                    return config.get("janela", {})
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Erro ao ler o arquivo de configuração.\nAplicando configurações padrão.")
        else:
            # Cria um arquivo de configuração padrão
            self.salvar_config({"largura": 800, "altura": 600, "modo": "janela"})
            messagebox.showinfo("Configuração", "Arquivo de configuração criado com valores padrão.")
            return {"largura": 800, "altura": 600, "modo": "janela"}

    def salvar_config(self, config):
        """Salva as configurações no arquivo JSON."""
        os.makedirs(os.path.dirname(FILE_CONFIG), exist_ok=True)
        with open(FILE_CONFIG, "w") as f:
            json.dump({"janela": config}, f, indent=4)

    def sair(self):
        """Página de saída."""
        self.limpar_frame()
        tk.Label(self.main_frame, text="Deseja realmente sair?", font=("Arial", 16), bg="white").pack(pady=20)

        btn_sim = tk.Button(self.main_frame, text="Sim", bg="red", fg="white", command=self.sair_sistema)
        btn_sim.pack(pady=10)

        btn_nao = tk.Button(self.main_frame, text="Não", bg="green", fg="white", command=self.inicio)
        btn_nao.pack(pady=10)

    def sair_sistema(self):
        """Fecha a aplicação e apaga a sessão."""
        if os.path.exists(FILE_TEMP):
            os.remove(FILE_TEMP)
        self.root.destroy()


def verificar_sessao():
    """Verifica a existência e integridade do arquivo de sessão."""
    if os.path.exists(FILE_TEMP):
        with open(FILE_TEMP, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Erro ao ler o arquivo de sessão.")
    return None


if __name__ == "__main__":
    sessao = verificar_sessao()
    if sessao:
        Sistema()
    else:
        messagebox.showerror("Erro", "Você não tem permissão para estar aqui!")
        # Certifique-se de que o caminho para app.py está correto
        subprocess.run(["python", "app.py"])
