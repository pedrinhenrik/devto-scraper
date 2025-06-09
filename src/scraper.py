import requests
from bs4 import BeautifulSoup
from datetime import datetime

#Função para extrair posts do dev.to
def extrair_posts():
    url = 'https://dev.to/'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Erro ao acessar {url}')
    
    soup = BeautifulSoup(response.text, 'lxml')

    posts = []

    # Loop para encontrar todos os blocos de posts
    articles = soup.find_all('div', class_='crayons-story')

    # Loop por todas as tags de post da página
    for article in articles:
        #Pular se for anuncio
        if 'crayons-story__billboard' in article.get('class', []):
            continue

        # Título e URL
        title_tag = article.find('h2')
        link_tag = title_tag.find('a') if title_tag else None

        if link_tag:
            titulo = link_tag.get_text(strip=True)
            href = link_tag['href']
            if href.startswith('http'):
                url_post = href
            else:
                url_post = f"https://dev.to{href}"
        else:
            titulo = 'Sem título'
            url_post = None

        # Autor
        autor_tag = article.select_one('a.crayons-story__secondary.fw-medium')
        autor = autor_tag.get_text(strip=True) if autor_tag else 'Desconhecido'

        # Tags
        tags_list = [tag.get_text(strip=True) for tag in article.find_all('a', class_='crayons-tag')]
        tags = ', '.join(tags_list) if tags_list else 'Sem tags'

        # Número de reações
        reacoes_tag = article.select_one('span.aggregate_reactions_counter')
        if reacoes_tag:
            reacoes_text = reacoes_tag.get_text(strip=True)
            reacoes_num = ''.join(filter(str.isdigit, reacoes_text))
            reacoes = int(reacoes_num) if reacoes_num else 0
        else:
            reacoes = 0

        # Número de comentários
        comentarios_tag = article.find('a', href=lambda href: href and '#comments' in href)
        comentarios = None

        if comentarios_tag:
            for child in comentarios_tag.children:
                if isinstance(child, str):
                    texto = child.strip()
                    if texto.isdigit():
                        comentarios = int(texto)
                        break

        # Pega a data de postagem
        data_postagem_tag = article.find('time')
        if data_postagem_tag:
            iso_data = data_postagem_tag['datetime']
            try:
                # Remove o 'Z' e converte para datetime para evitar problemas no Sql de formatação
                dt = datetime.strptime(iso_data.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
                data_postagem = dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                data_postagem = None
        else:
            data_postagem = None

        # Define hora atual e data no formato
        data_coleta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adiciona o post à lista
        posts.append({
            'titulo': titulo,
            'autor': autor,
            'tags': tags,
            'reacoes': reacoes,
            'comentarios': comentarios,
            'url_post': url_post,
            'data_coleta': data_coleta,
            'data_publicacao': data_postagem,
            })

    return posts