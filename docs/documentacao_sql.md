# Documentação SQL - Dev.to Scraper

## Banco de Dados: banco_devto
Banco de dados para armazenar posts extraídos do site Dev.to.

## Tabela: posts

| Coluna      | Tipo                     | Descrição                                   |
|-------------|--------------------------|--------------------------------------------|
| id          | INT AUTO_INCREMENT PRIMARY KEY | Identificador único do post.            |
| titulo      | VARCHAR(255)              | Título do post.                            |
| autor       | VARCHAR(255)              | Nome do autor do post.                     |
| categoria   | VARCHAR(255)              | Categoria ou tag principal do post.        |
| url_post    | VARCHAR(255) UNIQUE       | **Link do post** no Dev.to (deve ser único). |
| data_coleta | DATETIME                  | Data e hora em que o post foi coletado.     |
| tags        | TEXT                      | Lista de tags associadas, separadas por vírgula. |
| reacoes     | INT                       | Número de reações do post.                 |
| comentarios | INT                       | Número de comentários no post.             |

---

## Script SQL

```sql
CREATE DATABASE IF NOT EXISTS banco_devto
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE banco_devto;

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    url_post VARCHAR(255) UNIQUE,
    data_coleta DATETIME,
    tags TEXT,
    reacoes INT DEFAULT 0,
    comentarios INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
