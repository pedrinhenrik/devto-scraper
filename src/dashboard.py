import matplotlib
matplotlib.use('Agg')

import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import mysql.connector
from src.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import webbrowser
import threading

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Lê os dados da tabela
query = "SELECT * FROM posts"
df = pd.read_sql(query, conn)

# Inicializa o app
app = dash.Dash(__name__)
app.title = 'Dashboard Dev.to'

# Layout
app.layout = html.Div([
    html.H1('📊 Dashboard de Posts do Dev.to', style={'textAlign': 'center', 'marginBottom': 40}),

    html.Div([
        html.Div([
            html.Label('Filtrar por Autor:'),
            dcc.Dropdown(
                options=[{'label': autor, 'value': autor} for autor in sorted(df['autor'].dropna().unique())],
                id='autor-dropdown',
                multi=True,
                placeholder="Selecione um ou mais autores"
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0px 20px'}),

        html.Div([
            html.Label('Filtrar por Tag:'),
            dcc.Dropdown(
                options=[{'label': tag, 'value': tag} for tag in sorted(set(sum((str(tags).split(', ') for tags in df['tags'].dropna()), [])))],
                id='tag-dropdown',
                multi=True,
                placeholder="Selecione uma ou mais tags"
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0px 20px'})
    ], style={'marginBottom': 50}),

    dash_table.DataTable(
        id='posts-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': "#159cfc",
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '5px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        filter_action='native',
        sort_action='native'
    ),

    html.Br(),

    dcc.Graph(id='grafico-reacoes'),

    html.Footer('Powered by: Seu Nome 🚀', style={'textAlign': 'center', 'marginTop': 50, 'padding': 20, 'fontSize': 14, 'color': 'gray'})
], style={'fontFamily': 'Arial', 'padding': '20px'})

# Callback para atualizar
@app.callback(
    [Output('posts-table', 'data'),
     Output('grafico-reacoes', 'figure')],
    [Input('autor-dropdown', 'value'),
     Input('tag-dropdown', 'value')]
)
def update_dashboard(autores_selecionados, tags_selecionadas):
    df_filtrado = df.copy()

    if autores_selecionados:
        df_filtrado = df_filtrado[df_filtrado['autor'].isin(autores_selecionados)]

    if tags_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['tags'].apply(
            lambda x: any(tag.strip() in str(x) for tag in tags_selecionadas)
        )]

    fig = px.histogram(df_filtrado, x='reacoes', nbins=30, title='Distribuição de Reações por Post',
                       color_discrete_sequence=['#1f77b4'])
    fig.update_layout(bargap=0.2, plot_bgcolor='white')

    return df_filtrado.to_dict('records'), fig

# Função para rodar o dashboard
def iniciar_dashboard():
    app.run(debug=True, use_reloader=False) 