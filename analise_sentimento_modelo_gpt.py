'''
Módulo do modelo de analise de sentimento usando chat gpt
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
'''

import openai
import os
import pandas as pd
import time
import re
import os
from noticias_processamento_texto import *
import traceback
import logging
import warnings
import numpy as np
import datetime  as dt
from scipy import interpolate
import scipy.stats
from scipy.interpolate import make_interp_spline
from noticias_timeline import plota_timeline

openai.api_key = os.getenv('GPT_API_KEY')


def classifica_sentimento_noticia_gpt(data, titulo, texto, empresa, model='gpt-4-turbo-preview', caminho_cache='datasets/gpt_cache.xlsx', usar_cache=True, dicionario_cache=None):
    '''Utiliza a API do Chat GPT para analisar uma noticia'''
    
    pergunta = '''Você receberá um texto de uma notícia sobre uma empresa, e deverá responder:'
                  a) se a notícia do tema ESG (considere que casos relacionados à inadimplência, falência ou recuperação judicial devem ser classificados na dimensão G); 
                  b) Em caso positivo, qual a dimensão dominante: E, S ou G; 
                  c) Avaliar o sentimento da notícia, considerando a atitude da empresa sob a ótica ESG, no intervalo real entre -1.0 até +1.0; 
                  d) Qual o nome da principal empresa envolvida; e) Esse texto tem como tema principal a empresa "<empresa>"? 
                  f) Se a notícia for do tema ESG, faça um breve resumo de apenas 1 sentença. Dê respostas curtas'''.replace('<empresa>', empresa)
    
    
    
    hash_texto = criar_hash_noticia(texto, empresa, titulo=titulo, data=data)
    
    caminho_cache='datasets/gpt_cache.xlsx'
    
    if usar_cache:
        if dicionario_cache is not None:
            dic= dicionario_cache
        else:
            df = pd.read_excel(caminho_cache)
            dic = df.set_index('hash')['resposta'].to_dict()


    if usar_cache and hash_texto in dic:
        return dic[hash_texto]
    else:
        response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {
                          "role": "system",
                          "content": pergunta
                        },
                        {
                          "role": "user",
                          "content": titulo + '\n' + texto
                        }
                      ],
                    temperature=0,
                    max_tokens=255,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )


        resposta = response.choices[0].message["content"]
        dic[hash_texto] = resposta
        if dicionario_cache is  None: # salva cache caso nao seja controlado pelo chamador
            df = pd.DataFrame({'hash': dic.keys(),  'resposta': dic.values()})
            df.to_excel(caminho_cache, index=False)

    return resposta


def trata_resposta_gpt(r):
    '''Rotina interna para tratar a resposta do chat gpt'''
    
    itens = ['a) ', 'b) ', 'c) ', 'd) ', 'e) ', 'f) ', 'g) ']
    
    r = r.replace('\n\n', '\n')
    
    respostas = r.split('\n')
    
    
    respostas = [resp.replace(item, '') for resp, item in zip(respostas, itens)]
    
    if len(respostas) <= 2:
        return 'Outros', 'Outros', '', '', '', ''
    
    try:
    
        tema = respostas[0][:3]

        if tema == 'Sim':
            tema = 'ESG'
        else:
            tema = 'Outros'

        dimensao = 'Outros'
        if 'S' in respostas[1] or 'G' in respostas[1] or 'E' in respostas[1]:
            dimensao = respostas[1].replace('A dimensão dominante é ', '').replace('"', '').strip()[:1]

        sentimento = 0
        nota = re.findall('[+-]?[0-9][.]?[0-9]{1,3}', respostas[2])
        if len(nota) > 0:
            sentimento = float(nota[0].strip())

        empresa_detectada = respostas[3].replace('A principal empresa envolvida é o ', '').replace('A principal empresa envolvida é a ', '').replace('.', '')

        foco_empresa = respostas[4][:3]
        
        if len(respostas) < 6:
            resumo = ''
        else:
            resumo = respostas[5]
            
    except Exception as e:
        logging.error(traceback.format_exc())
        print(respostas)
    
    return [tema, dimensao, sentimento, empresa_detectada, foco_empresa, resumo]


def gera_colunas_gpt(df, coluna_resposta_gpt='resposta'):
    '''rotina interna para fazer a separacao das respostas do chat gpt em colunas'''
    df['gpt_lista_respostas'] = df.apply(lambda row: trata_resposta_gpt(row[coluna_resposta_gpt]), axis=1)
    df['gpt_tema_esg'] = df['gpt_lista_respostas'].apply(lambda x : x[0])
    df['gpt_classificacao'] = df['gpt_lista_respostas'].apply(lambda x : x[1])
    df['gpt_polaridade'] = df['gpt_lista_respostas'].apply(lambda x : x[2])
    df['gpt_empresa_principal'] = df['gpt_lista_respostas'].apply(lambda x : x[3])
    df['gpt_focado_empresa'] = df['gpt_lista_respostas'].apply(lambda x : x[4])
    df['gpt_resumo'] = df['gpt_lista_respostas'].apply(lambda x : x[5])
    return df


def filtros_pos_gpt(df):
    '''filtra as noticias apos aplicacao do chat gpt, descartando o que nao for ESG'''
    
    df = df[df['gpt_tema_esg'] != 'Outros']

    
    df = df[df['gpt_focado_empresa'] == 'Sim']
    
    df['classificacao'] = df.apply(lambda row: row['gpt_classificacao'] if (row['gpt_classificacao'] in ['E', 'S', 'G']) else row['classificacao_ml'], axis=1)
    
    return df



def gera_curva_polaridade_media(dfNoticiasComPolaridade, empresa, dimensao, maxima_data=None, alfa=0.07, tam_minimo=5):
    '''
    Gera a curva de polaridade média - modelo EWMA 
    '''
    dfPolaridade = dfNoticiasComPolaridade
    
    dfPolaridade = dfPolaridade.rename(columns={'data_publicacao' : 'data'})
    
    if maxima_data is not None:
        dfPolaridade = dfPolaridade[dfPolaridade['data'].dt.date <= maxima_data]
    
    if empresa != '':
        dfPolaridade = dfPolaridade[dfPolaridade['empresa'] == empresa]
    if dimensao != '' and dimensao != 'ESG':
        dfPolaridade = dfPolaridade[dfPolaridade['classificacao'] == dimensao]
        
    dfPolaridade['data'] = pd.to_datetime(pd.to_datetime(dfPolaridade['data']).dt.date)
    
    dfPolaridade = dfPolaridade.set_index('data')
    dfPolaridade = dfPolaridade.groupby(by='data').agg({'polaridade' : 'sum', 'titulo': 'count'})
    
    dfPolaridade['polaridade'] = dfPolaridade['polaridade'] / dfPolaridade['titulo']
    dfPolaridade = dfPolaridade.sort_index()

    
    if len(dfPolaridade) <= tam_minimo:
        return None
    
    dfPolaridade = dfPolaridade.rename(columns={'titulo' : 'Quantidade Noticias na Data'})
    
    dfPolaridade['polaridade_ewma'] = dfPolaridade.ewm(alpha=alfa, adjust=True).mean()['polaridade']
    
    dfPolaridade['polaridade_fit'] = dfPolaridade['polaridade_ewma']   
    
    dfPolaridade['empresa'] = empresa
    
    dfPolaridade['Dimensão'] = dimensao
    
    
    
    dfPolaridade = dfPolaridade.loc[:, ['empresa',  'Dimensão', 'Quantidade Noticias na Data', 'polaridade_fit']]
    

    return dfPolaridade
