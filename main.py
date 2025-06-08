from src.scraper import extrair_posts
from src.database import criar_tabela, inserir_post
from src.gerador_relatorio import gerar_relatorio_excel
from src.publicador_x import publicar_no_x

def main():
    criar_tabela()
    posts = extrair_posts()

    novos_posts = 0

    for post in posts:
        if inserir_post(
            post['titulo'],
            post['autor'],
            post['tags'],
            post['reacoes'],
            post['comentarios'],
            post['url_post'],
            post['data_coleta'],
            post['data_publicacao'],
        ):
            novos_posts = novos_posts + 1

    print(f'{novos_posts} posts novos inseridos no banco de dados com sucesso!')

    gerar_relatorio_excel()

    #Bônus: Publicar no Twitter
    publicar_no_x()

if __name__ == '__main__':
    main()