'''
Módulo que trata a busca das noticias dos temas ESG no Google, e suas transformações e processamentos
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
'''

import warnings
import numpy as np
import pandas as pd
import re
import unidecode
import datetime as dt
from noticias_google_buscador import busca_noticias_google_news
from noticias_processamento_texto import *
from noticias_io import le_termos_esg_para_df

warnings.filterwarnings('ignore')


def busca_noticias_google_periodo(termo, atualiza=False, ultima_data=None):
    '''
    Busca as noticias do google , por periodo, realizando divisao por tempo para poder carregar mais de 100 noticias
    Isso é necessario pela limitacao da API que retorna no maximo 100 noticias
    '''
    
    if not atualiza:
        df = busca_noticias_google_news(termo, '')  # busca sem data

        hoje = dt.datetime.now()
        for i in range(1, 15):   # busca 14 periodos de 6 meses
            dt_defasada = hoje - dt.timedelta(i * 180)

            dfNovaPesquisa = busca_noticias_google_news(termo, dt_defasada.strftime("%Y-%m-%d"))

            if len(dfNovaPesquisa) > 0:
                df = pd.concat([df, dfNovaPesquisa ])
    else:
        if ultima_data is not None:
            df = busca_noticias_google_news(palavras=termo, data_limite=ultima_data.strftime("%Y-%m-%d"), after=True)
        else:
            df = busca_noticias_google_news(palavras=termo)
            
            
    if len(df) > 0:

        df  = filtra_noticias_sites_especificos(df)

        df['fonte'] = df['fonte'].apply(lambda x : x['title'])

        df = df.drop_duplicates().reset_index(drop=True)
    
    return df




def busca_noticias_google_esg(empresa_pesquisada, atualiza=False, ultima_data=None, inclui_apenas_nome_empresa=False):
    '''
    Busca as noticias do google 
    '''
    dfTermos = le_termos_esg_para_df()
    
    empresa_pesquisada_aju = empresa_pesquisada.replace(' ', '+')
    empresa_pesquisada_aju = empresa_pesquisada_aju.replace('&', '%26')
    
    print('...... buscando no google ' + empresa_pesquisada_aju)


    dfESG = busca_noticias_google_periodo(empresa_pesquisada_aju + '+ESG', atualiza, ultima_data)

    for letra in 'ESG':
        q = remove_acentos(empresa_pesquisada_aju + '+('+ '|'.join(''+ dfTermos[letra][dfTermos[letra].notnull()] +'').replace(' ', '+') + ')')
        dfLetra = busca_noticias_google_periodo(q, atualiza, ultima_data)
        
        if len(dfLetra) > 0:
            dfESG = pd.concat([dfESG,dfLetra]).drop_duplicates().reset_index(drop=True)
            
        
    if inclui_apenas_nome_empresa:    
        dfEmp = busca_noticias_google_periodo(empresa_pesquisada_aju , atualiza, ultima_data)    
        if len(dfEmp) > 0:
            dfESG = pd.concat([dfESG,dfEmp]).drop_duplicates().reset_index(drop=True)
            
    if len(dfESG) > 0:
        dfESG = dfESG.sort_values(by='data_publicacao')  #ordena

        dfESG['empresa'] = remove_acentos(empresa_pesquisada.lower())
    
    return dfESG


def filtra_noticias_sites_especificos(noticias):
    '''
    Filtra determinados sites na busca
    '''
    df = noticias
    df = df[df['fonte'].str['href'].str.contains('xpi.')==False]
    df = df[df['fonte'].str['href'].str.contains('estrategiaconcursos')==False]
    df = df[df['fonte'].str['href'].str.contains('conjur')==False]
    df = df[df['fonte'].str['href'].str.contains('gov.br')==False]
    df = df[df['fonte'].str['href'].str.contains('portogente')==False]
    df = df[df['fonte'].str['href'].str.contains('stj.')==False]
    df = df[df['fonte'].str['href'].str.contains('pcb.')==False]
    df = df[df['fonte'].str['href'].str.contains('tre.')==False]
    df = df[df['fonte'].str['href'].str.contains('boatos.org')==False]
    
    # tira portugal e europa
    df = df[df['fonte'].str['href'].str.endswith('.pt')==False]
    df = df[df['fonte'].str['href'].str.endswith('.eu')==False]
    

    return df


def recupera_noticias_completas(noticias, apenas_titulos=False):
    '''
    Faz o scrapping de cada noticias utilizando biblioteca 
    https://newspaper.readthedocs.io/en/latest/
    '''
    
    import pandas as pd
    from newspaper import Article 
    
    if apenas_titulos: # nao extrai conteudo
        df = noticias
        df['texto_completo'] = df['titulo']
        
        return df
    
    df = noticias
    textos = []

    for i in range(0, len(df)):
        url = df.iloc[i]['url']
        article = Article(url, language='pt')
        try:
            article.download()
            article.parse()
            textos.append(article.text)       
        except:
            textos.append('')     
    
    df['texto_completo'] = textos
    
    df = df[ (df['texto_completo'] != '')]
    
    return df




