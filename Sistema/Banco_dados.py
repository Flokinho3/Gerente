import sqlite3
import os

# Caminho da pasta onde os bancos de dados serão armazenados
FILE_BG = "Sistema/Banco_de_dados/"

class Banco_de_dados:
    def criar_tabela(self, nome_banco, nome_tabela, colunas, nome_colunas, tipo_colunas):
        # Verifica se o banco de dados já existe
        banco_path = os.path.join(FILE_BG, f"{nome_banco}.db")
        
        if not os.path.exists(banco_path):  # Se o banco não existe
            # Cria a pasta se não existir
            if not os.path.exists(FILE_BG):
                os.mkdir(FILE_BG)

            # Cria o banco de dados e a tabela
            conn = sqlite3.connect(banco_path)
            cursor = conn.cursor()

            # Montando a string de criação da tabela de forma correta
            colunas_str = ", ".join([f"{nome_colunas[i]} {tipo_colunas[i]}" for i in range(len(nome_colunas))])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({colunas_str})")
            
            conn.commit()
            conn.close()
            print(f"Banco de dados {nome_banco} e tabela {nome_tabela} criados com sucesso.")
            return True  # Indica que o banco foi criado
        else:
            print(f"O banco de dados {nome_banco} já existe.")
            return False  # Indica que o banco já existe
