def gerar_relatorio_excel():
    import pandas as pd
    import mysql.connector
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image
    from openpyxl.styles import Alignment, Font, PatternFill
    import matplotlib.pyplot as plt
    import os
    from src.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
    from collections import Counter

    # Cria o caminho da pasta
    pasta_relatorios = os.path.join(os.path.dirname(__file__), '..', 'relatorios')
    os.makedirs(pasta_relatorios, exist_ok=True)
    arquivo_excel = os.path.join(pasta_relatorios, 'relatorio_posts_devto.xlsx')

    # Conexão ao banco
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # Query para pegar todos os posts
    query = "SELECT * FROM posts"
    df = pd.read_sql(query, conn)

    # Exporta para Excel
    df.to_excel(arquivo_excel, index=False)

    # Abre o arquivo para formatação
    wb = load_workbook(arquivo_excel)
    ws = wb.active
    ws.title = "Posts"
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions

    # Centralizar todas as células da aba Posts
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # Formatar o cabeçalho
    header_fill = PatternFill(start_color='006400', end_color="224e22", fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    # Cabeçalho
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font

    # Ajustar largura das colunas
    for column_cells in ws.columns:
        max_length = 0
        column = column_cells[0].column_letter  # Letra da coluna

        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Função para encurtar o texto
    def encurtar_texto(texto, limite=25):
        if len(texto) > limite:
            return texto[:limite] + '...'
        return texto


    # Gráfico Top 10 autores
    top_autores = df['autor'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#00bfff' if val < top_autores.max() else '#ff4500' for val in top_autores]
    bars = ax.barh(top_autores.index, top_autores.values, color=colors, edgecolor='black')

    fig.suptitle('Top 10 Autores por Número de Posts', fontsize=16, weight='bold', y=0.98)
    ax.set_xlabel('Quantidade de Posts', fontsize=12)
    ax.set_ylabel('Autores', fontsize=12)

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords='offset points',
                    ha='left', va='center', fontsize=10, fontweight='bold', color='black')

    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    caminho_img_autores = os.path.join(pasta_relatorios, 'top_autores.png')
    plt.savefig(caminho_img_autores)
    plt.close()

    # Junta todas as tags
    todas_tags = []
    for tags in df['tags']:
        if pd.notnull(tags):
            tags_list = [tag.strip() for tag in tags.split(',')]
            todas_tags.extend(tags_list)

    # Conta a frequência
    contador_tags = Counter(todas_tags)
    top_tags = contador_tags.most_common(10)
    tags_labels, tags_counts = zip(*top_tags)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#00bfff' if val < max(tags_counts) else '#ff4500' for val in tags_counts]
    bars = ax.barh(tags_labels, tags_counts, color=colors, edgecolor='black')
    fig.suptitle('Top 10 Tags Mais Usadas', fontsize=16, weight='bold', y=0.98)
    ax.set_xlabel('Quantidade de Vezes', fontsize=12)
    ax.set_ylabel('Tag', fontsize=12)

    # Adicionando os valores no final da barra
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords='offset points',
                    ha='left', va='center', fontsize=10, fontweight='bold', color='black')

    # Remover bordas
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    # Salva a imagem na pasta relatorios
    plt.savefig(os.path.join(pasta_relatorios, 'top_tags.png'))
    plt.close()

    # Gráfico Top 10 posts por reações
    top_reacoes = df.sort_values(by='reacoes', ascending=False).head(10)
    top_reacoes['titulo_curto'] = top_reacoes['titulo'].apply(lambda x: encurtar_texto(str(x), limite=10))

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#00bfff' if val < top_reacoes['reacoes'].max() else '#ff4500' for val in top_reacoes['reacoes']]
    bars = ax.barh(top_reacoes['titulo_curto'], top_reacoes['reacoes'], color=colors, edgecolor='black')

    fig.suptitle('Top 10 Posts por Número de Reações', fontsize=16, weight='bold', y=0.98)
    ax.set_xlabel('Reações', fontsize=12)
    ax.set_ylabel('Título', fontsize=12)

    # Adicionando os valores no final da barra
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords='offset points',
                    ha='left', va='center', fontsize=10, fontweight='bold', color='black')

    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    caminho_img_reacoes = os.path.join(pasta_relatorios, 'top_posts_reacoes.png')
    plt.savefig(caminho_img_reacoes)
    plt.close()


    # Cria novas abas e adiciona as imagens
    aba_autores = wb.create_sheet(title="Gráfico Autores")
    img_autores = Image(caminho_img_autores)
    img_autores.anchor = 'A1'
    aba_autores.add_image(img_autores)

    # Cria novas abas e adiciona as imagens
    aba_reacoes = wb.create_sheet(title="Gráfico Reações")
    img_reacoes = Image(caminho_img_reacoes)
    img_reacoes.anchor = 'A1'
    aba_reacoes.add_image(img_reacoes)

    # Cria novas abas e adiciona as imagens
    aba_tags = wb.create_sheet(title="Gráfico Tags")
    img_tags = Image(os.path.join(pasta_relatorios, 'top_tags.png'))
    img_tags.anchor = 'A1'
    aba_tags.add_image(img_tags)


    # Salva o arquivo Excel final
    wb.save(arquivo_excel)

    print(f"✅ Relatório gerado: {arquivo_excel}")