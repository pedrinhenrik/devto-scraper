# 📊 DEV.to Scraper + Bot de Postagem no X (Twitter)

Este projeto realiza a extração automatizada de posts do site DEV.to, salva os dados em um banco MySQL, gera relatórios e gráficos em Excel, e ainda prepara postagens automáticas no X (antigo Twitter).

✅ Raspagem de dados  
✅ Armazenamento em banco de dados  
✅ Relatórios automatizados  
✅ Gráficos de visualização  
✅ Bot para pré-postagem no X com print automático  

---

## 🚀 Funcionalidades

- Scraper automatizado de posts do DEV.to
- Armazenamento dos dados em MySQL
- Relatório em Excel com dados tabulados
- Geração de gráficos:
  - Top 10 autores por número de posts
  - Top 10 posts por número de reações
  - Captura das tags (hashtags) mais populares
- Bot de postagem no X (Twitter):
  - Login manual para segurança
  - Preenchimento automático do post
  - Screenshot da prévia do tweet
  - Opção de postar ou não via escolha do usuário

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- Selenium
- WebDriver Manager
- MySQL
- Pandas
- OpenPyXL
- Matplotlib
- ChromeDriver

---

## 📁 Estrutura de Diretórios

```
Poder360/
│
├── relatorios/              # Relatórios gerados (Excel, imagens PNG)
├── src/
│   ├── scraper.py            # Lógica de scraping
│   ├── database.py           # Banco de dados
│   ├── gerador_relatorio.py  # Geração de relatórios e gráficos
│   ├── publicador_x.py       # Bot de postagem no X (Twitter)
│   └── config.py             # Configurações de acesso ao banco
│
├── venv/                     # Ambiente virtual (não subir para o GitHub)
├── requirements.txt          # Dependências
├── README.md                  # Documentação
└── main.py                    # Script principal
```

---

## 📦 Instalação

### 1 Clone o repositório

```bash
git clone https://github.com/seuusuario/poder360.git
cd poder360
```

### 2 Crie e ative o ambiente virtual

```bash
python -m venv venv
# Ativar:
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3 Instale as dependências

```bash
pip install -r requirements.txt
```

### 4 Configure seu `config.py`

```python
# src/config.py
DB_HOST = "localhost"
DB_USER = "seu_usuario"
DB_PASSWORD = "sua_senha"
DB_NAME = "nome_do_banco"
```


---

## 📝 Como Usar

Execute o script principal:

```bash
python main.py
```

O que acontece automaticamente:

✅ Criação de Tabela no MySQL se ainda não existir  
✅ Scraping de Posts do DEV.to  
✅ Armazenamento no banco (sem duplicados)  
✅ Geração de Relatório em Excel com dados organizados  
✅ Gráficos salvos em PNG:
- Top 10 autores por número de posts
- Top 10 posts por reações

Em seguida:

✅ O navegador será aberto para o X (Twitter) em [https://x.com/compose/post](https://x.com/compose/post)  
✅ Você faz o login manualmente (por segurança, não guardamos senha!)  
✅ O link é preenchido automaticamente.  
✅ Você verá uma opção:

```bash
Digite:
1 - Para Postar automaticamente
2 - Apenas gerar o print sem postar
```

✅ Um screenshot da prévia da postagem é gerado e salvo em `relatorios/preview_tweet.png`.

---

## 📈 Exemplos de Relatórios Gerados

### 📊 Relatório em Excel

Contém:

- Título
- Autor
- Tags
- Número de Reações
- Comentários
- Link do Post
- Data de Coleta
- Data da Publicação no DEV.to

### 📊 Gráficos Gerados

- Top 10 Autores com Mais Posts
- Top 10 Posts com Mais Reações

### 📸 Screenshot da Prévia no X

---

## 🔒 Observações

- Login manual evita exposição de credenciais e problemas com autenticação de dois fatores (2FA).
- Sem duplicação: Posts repetidos são ignorados.
- Compatível com últimas versões do Chrome e ChromeDriver.

---

## 🚀 Melhorias Futuras

- Automatizar login via cookies/session.
- Postagem com imagens customizadas.
- Melhor tratamento de erros durante scraping/postagem.
- Geração de Wordcloud com tags mais usadas.

---

## 👨‍💻 Autor

Desenvolvido por [Pedro Liberal]([https://github.com/pedroliberal](https://github.com/pedrinhenrik)) 🚀
