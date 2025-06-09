from src.scraper import extrair_posts
from src.database import criar_tabela, inserir_post
from src.gerador_relatorio import gerar_relatorio_excel
from src.publicador_x import publicar_no_x
from src.dashboard import iniciar_dashboard


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
    #publicar_no_x()

    # Pergunta ao usuário se deseja abrir o dashboard de relatórios
    resposta = input("\nDeseja abrir o dashboard de relatórios? (1 = Sim, 2 = Não): ")

    if resposta == "1":
        print("✅ Dashboard iniciado com sucesso!")
        from src.dashboard import iniciar_dashboard
        iniciar_dashboard()
        print("Aperte CTRL+C para fechar o dashboard.")
        print("✅ Execução finalizada com sucesso!")

if __name__ == '__main__':
    main()