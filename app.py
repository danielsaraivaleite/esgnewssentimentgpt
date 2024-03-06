'''
Aplicativo WEB em FLASK para apresentar a analise de sentimento das noticias
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
'''


from flask import Flask, render_template, request, make_response, session

import os
import pandas as pd
from analise_sentimento_modelo_gpt import gera_curva_polaridade_media
from noticias_graficos import *
from noticias_wordcloud import plotar_word_cloud
import xlsxwriter
import io
from cotacoes import busca_cotacao
from noticias_io import le_base_noticias_compacta_para_df

df = le_base_noticias_compacta_para_df()
# carrega lista de empresas
nomes_empresas = list(df.sort_values(by='Nome')['Nome'].drop_duplicates())

app = Flask(__name__)

app.secret_key = "ESGNEWSSENT"


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Página principal do app que mostra o sentimento das noticias
    O resultado mostrado da analise ja foi previamente gerado nas Jupyter notebooks do projeto
    '''

    # processa a busca
    if request.method == 'POST':
        nome = request.form.get('nomes')

        if len( df[df['Nome'].str.lower() == nome.lower()]  ) > 0:
            session['nome'] = nome
            return render_template("loading.html")

    if 'nome' in session:  # acionado depois do loading
        if session['nome'] is not None and session['nome'] != '':
            return renderiza_dashboard(session['nome'])
    else:
        session.pop('nome', None)

    # pagina principal de busca
    return render_template('index.html', nomes=nomes_empresas)


def renderiza_dashboard(nome):
    dfEmpresa = df[df['Nome'].str.lower() == nome.lower()]

    empresa = dfEmpresa['empresa'].iloc[0]

    cnpj = dfEmpresa['CNPJ'].iloc[0]

    razao = dfEmpresa['Razão social'].iloc[0]

    setor = dfEmpresa['Setor'].iloc[0]

    detalhes = ''

    if (not pd.isnull(cnpj))  and cnpj != '':
        detalhes = 'CNPJ: ' + str(cnpj)
        if (not pd.isnull(razao)) and razao != '':
            detalhes = detalhes + ' - Razão social: ' + str(razao).title()
        if (not pd.isnull(setor)) and setor != '':
            detalhes = detalhes + ' - Atividade: ' + str(setor).title()

    # adiciona o formato de exibicao
    dfEmpresa['formato'] = dfEmpresa['polaridade'].apply(formato_tabela)

    # converte a tabela pra dicionario permitindo a exibicao
    tabela_dados_pos = dfEmpresa[dfEmpresa.polaridade>0.05].to_dict(orient='records')
    tabela_dados_neg = dfEmpresa[dfEmpresa.polaridade<-0.05].to_dict(orient='records')

    # ultima noticia
    ultima_data = dfEmpresa['data_publicacao'].max().strftime('%d/%m/%Y')

    # plota grafico polaridade media
    lista_dfs_polaridade = gera_lista_curvas_polaridade(df, empresa)
    graph_path = (os.path.join('static', 'images', 'grafico_polaridade.png'))
    plota_polaridade_media_sintetico(df, empresa, arquivo=graph_path, lista_dfs_polaridade=lista_dfs_polaridade)

    # plota cotacoes
    arquivo_cotacoes = ''
    if (not (lista_dfs_polaridade is  None)) and len(lista_dfs_polaridade) > 0 and (not (lista_dfs_polaridade is None)) and  (not (lista_dfs_polaridade[0] is None))   and  len(lista_dfs_polaridade[0])>0 and (not pd.isnull(dfEmpresa['Código'].iloc[0])):
        simbolo = dfEmpresa['Código'].iloc[0]
        if simbolo != '' and simbolo != empresa and simbolo != nome:
            df_cotacoes = busca_cotacao(simbolo)
            if df_cotacoes is not None and len(df_cotacoes) >0:
                arquivo_cotacoes = (os.path.join('static', 'images', 'grafico_cotacoes.png'))
                plota_polaridade_cotacoes(empresa, lista_dfs_polaridade[0], df_cotacoes, simbolo, arquivo=arquivo_cotacoes)


    # plota os gauges
    plotar_gauge_polaridade(df, empresa=empresa, dimensao='ESG', df_pol=lista_dfs_polaridade[0], arquivo=os.path.join('static', 'images', 'gauge_esg.png'))
    plotar_gauge_polaridade(df, empresa=empresa, dimensao='E', df_pol=lista_dfs_polaridade[1], arquivo=os.path.join('static', 'images', 'gauge_e.png'))
    plotar_gauge_polaridade(df, empresa=empresa, dimensao='S', df_pol=lista_dfs_polaridade[2], arquivo=os.path.join('static', 'images', 'gauge_s.png'))
    plotar_gauge_polaridade(df, empresa=empresa, dimensao='G', df_pol=lista_dfs_polaridade[3], arquivo=os.path.join('static', 'images', 'gauge_g.png'))

    # base de dados
    plotar_descricao_base(dfEmpresa, plotar_histograma=True, arquivo=r'static/images/grafico_base_dados.png')

    # timeline
    plota_timeline_polaridade(dfEmpresa, +1, numero_noticias=2, empresa=empresa, imprime=False, arquivo=os.path.join('static', 'images', 'grafico_timeline_pos.png') )
    plota_timeline_polaridade(dfEmpresa, -1, numero_noticias=2, empresa=empresa, imprime=False, arquivo=os.path.join('static', 'images', 'grafico_timeline_neg.png') )

    # wordclouds
    plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao='E', arquivo=os.path.join('static', 'images', 'wordcloud_E.png'), coluna_texto='gpt_resumo')
    plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao='S', arquivo=os.path.join('static', 'images', 'wordcloud_S.png'), coluna_texto='gpt_resumo')
    plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao='G', arquivo=os.path.join('static', 'images', 'wordcloud_G.png'), coluna_texto='gpt_resumo')

    session.pop('nome', None)

    return render_template('index.html', nomes=nomes_empresas, tabela_pos=tabela_dados_pos,
                            tabela_neg=tabela_dados_neg, empresa_selecionada=nome, ultima_data=ultima_data,
                            arquivo_cotacoes=arquivo_cotacoes, detalhes=detalhes)



@app.route('/exportar_excel_noticias', methods=['GET', 'POST'])
def exportar_excel_noticias():

    dfEmpresa = df
    empresa=''

    # processa a busca
    if request.method == 'POST':
        nome = request.form.get('nome_empresa_exportar_noticias')
        dfEmpresa = df[df['Nome'] == nome]
        empresa = dfEmpresa['empresa'].iloc[0]

    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    dfEmpresa.to_excel(excel_writer=writer, index=False, sheet_name='Dados_Sentimento_ESG')
    writer.close()

    r = make_response(out.getvalue())
    r.headers["Content-Disposition"] = "attachment; filename=" + 'Dados_Sentimento_ESG_'+empresa+'.xlsx'
    r.headers["Content-type"] = "application/x-xls"

    return r

@app.route('/exportar_excel_grafico_polaridade', methods=['GET', 'POST'])
def exportar_excel_grafico_polaridade():

    dfEmpresa = df
    empresa=''

    # processa a busca
    if request.method == 'POST':
        nome = request.form.get('nome_empresa_exportar_grafico_polaridade')
        dfEmpresa = df[df['Nome'] == nome]
        empresa = dfEmpresa['empresa'].iloc[0]

        dfEmpresa = pd.concat( gera_lista_curvas_polaridade(df, empresa)  )

    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    dfEmpresa.to_excel(excel_writer=writer, index=False, sheet_name='Dados_Curva_Sentimento_ESG')
    writer.close()

    r = make_response(out.getvalue())
    r.headers["Content-Disposition"] = "attachment; filename=" + 'Dados_Curva_Sentimento_ESG_'+empresa+'.xlsx'
    r.headers["Content-type"] = "application/x-xls"

    return r

def gera_lista_curvas_polaridade(df, empresa):
    '''
    Gera as curvas de polaridade pelo modelo ewma
    '''

    calibragem_alfa = [0.07, 0.075, 0.1, 0.15]
    # plota grafico polaridade media
    lista_dfs_polaridade = [gera_curva_polaridade_media(df, empresa, 'ESG', alfa=calibragem_alfa[0]),
                            gera_curva_polaridade_media(df, empresa, 'E', alfa=calibragem_alfa[1]),
                            gera_curva_polaridade_media(df, empresa, 'S', alfa=calibragem_alfa[2]),
                            gera_curva_polaridade_media(df, empresa, 'G', alfa=calibragem_alfa[3])]

    return lista_dfs_polaridade


def formato_tabela(n):
    '''
    Define o Formato da tabela (heatmap) de acordo com polaridade
    '''
    cor_fundo = 'bg-success p-2'
    text = 'text-dark'
    opacidade = 'bg-opacity-10'
    if (n < 0):
        cor_fundo = 'bg-danger p-2'
        n = -1 * n

    if n >= 0.75:
        opacidade = ''
        text = 'text-white'
    elif n >= 0.5 and n<0.75:
        text = 'text-white'
        opacidade = 'bg-opacity-75'
    elif n >= 0.25 and n<0.5:
        opacidade = 'bg-opacity-50'
    elif n >= 0.10 and n<0.25:
        opacidade = 'bg-opacity-25'
    return cor_fundo + ' ' + text + ' ' + opacidade



if __name__ == '__main__':
    app.run(debug=True)
