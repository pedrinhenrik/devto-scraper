import mysql.connector
from mysql.connector import Error
from src.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

#Conexão no banco de dados no MySQL
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None
    
# Função para criar a tabela de posts no banco de dados se não existir
def criar_tabela():
    # Não usar conexão na mesma variável para evitar conflitos
    conn = conectar_db()
    if conn is None:
        return
    cursor = conn.cursor()
    
    # Criação da tabela posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(100) NOT NULL,
            url_post VARCHAR(255) UNIQUE,
            data_coleta DATETIME NOT NULL,
            tags TEXT,
            reacoes INT DEFAULT 0,
            comentarios INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    conn.commit()
    conn.close()

def inserir_post(titulo, autor, tags, reacoes, comentarios, url_post, data_coleta):
    conn = conectar_db()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO posts (titulo, autor, tags, reacoes, comentarios, url_post, data_coleta)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (titulo, autor, tags, reacoes, comentarios, url_post, data_coleta))
        conn.commit()
        return True

    except Error as e:
        if e.errno == 1062:  # Código de erro para entrada duplicada
             print(f"🔁 Post já existente no banco (duplicado): {url_post}")
             return False
        else:
            print(f"❌ Erro inesperado ao inserir post: {e}")
            return False
    finally:
        conn.close()