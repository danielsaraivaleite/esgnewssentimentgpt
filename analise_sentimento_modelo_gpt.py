'''
Módulo do modelo de analise de sentimento usando chat gpt
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
'''

import openai
import os
import pandas as pd
import re
from noticias_processamento_texto import *
import traceback
import logging
import datetime  as dt
from scipy import interpolate
from pandas.tseries.offsets import DateOffset

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


def __interpola_polaridade(ts, data_desejada, extrapola_fwd=True, extrapola_bwd=True):
    ts1 = ts.sort_index()

    if pd.to_datetime(data_desejada) in ts1.index:
        return  ts.loc[pd.to_datetime(data_desejada)]

    if extrapola_fwd and ts1.index.max() < pd.to_datetime(data_desejada):
        return ts.loc[ts.index.max()]

    if extrapola_bwd and ts1.index.min() > pd.to_datetime(data_desejada):
        return ts.loc[ts.index.min()]

    b = (ts1.index > data_desejada).argmax()
    s = ts1.iloc[b-1:b+1]

    s = s.reindex(pd.to_datetime(list(s.index.values) + [pd.to_datetime(data_desejada)]))
    return s.interpolate('time').loc[data_desejada]


def gera_variacoes_polaridades(df,dimensao='ESG'):
    today = pd.to_datetime(dt.date.today())
    m3 = today - DateOffset(months=3)
    m6 = today - DateOffset(months=6)
    m12 = today - DateOffset(months=12)
    m18 = today - DateOffset(months=18)

    empresas=[]
    nomes=[]
    pol_d0 = []
    pol_m3 = []
    pol_m6 = []
    pol_m12 = []
    pol_m18 = []

    for empresa in df['empresa'].unique():
        if df['data_publicacao'].max() >= m12:

            df_curvas = gera_curva_polaridade_media(df, empresa, 'ESG')

            if df_curvas is not None:
                empresas.append(empresa)
                nomes.append( df[df['empresa'] == empresa]['Nome'].iloc[0]  )
                pol_d0.append( __interpola_polaridade(df_curvas['polaridade_fit'], today  ))
                pol_m3.append( __interpola_polaridade(df_curvas['polaridade_fit'], m3  ))
                pol_m6.append( __interpola_polaridade(df_curvas['polaridade_fit'], m6  ))
                pol_m12.append( __interpola_polaridade(df_curvas['polaridade_fit'], m12  ))
                pol_m18.append( __interpola_polaridade(df_curvas['polaridade_fit'], m18  ))

    df_variacoes = pd.DataFrame({'empresa' : empresas, 'Nome': nomes, 'Pol_D0' : pol_d0, 'Pol_M3' : pol_m3, 'Pol_M6' : pol_m6, 'Pol_M12' : pol_m12 , 'Pol_M18' : pol_m18 })

    df_variacoes['Var_M3'] =  df_variacoes['Pol_D0'] - df_variacoes['Pol_M3']
    df_variacoes['Var_M6'] =  df_variacoes['Pol_D0'] - df_variacoes['Pol_M6']
    df_variacoes['Var_M12'] = df_variacoes['Pol_D0'] - df_variacoes['Pol_M12']
    df_variacoes['Var_M18'] = df_variacoes['Pol_D0'] - df_variacoes['Pol_M18']

    return df_variacoes


def gera_maiores_variacoes(df_variacoes, negativa=True, threshold=0.0, max_empresa=5, meses = ['M3', 'M6', 'M12', 'M18']):

    meses = meses[::-1]

    df_maiores_por_mes = None

    for mes in meses:
        mes = 'Var_' + mes

        df_maiores = df_variacoes

        if negativa:
            df_maiores = df_maiores[ df_maiores.Pol_D0 < threshold  ]
            df_maiores = df_maiores[ df_maiores[mes] < 0  ]
        else:
            df_maiores = df_maiores[ df_maiores.Pol_D0 > threshold  ]
            df_maiores = df_maiores[ df_maiores[mes] > 0  ]

        # remove ja listados em outros meses
        if df_maiores_por_mes is not None:
            for c in list(filter(lambda x : x.startswith('empresa'), df_maiores_por_mes.columns)):
                df_maiores = df_maiores[~ df_maiores['empresa'].isin( list(df_maiores_por_mes[c]))   ]

        df_maiores = df_maiores.sort_values(by=mes, ascending=negativa).loc[:, ['empresa', mes]].reset_index(drop=True)


        df_maiores = df_maiores[: max_empresa] # seleciona maiores
        # inclui nome da empresa, alem do nome abreviado
        df_maiores['Nome_'+mes] =  df_maiores['empresa'].map(df_variacoes.set_index('empresa')['Nome'])
        df_maiores = df_maiores.rename(columns={'empresa' : 'empresa_'+mes})

        # concatena demais meses
        if df_maiores_por_mes is None:
            df_maiores_por_mes = df_maiores
        else:
            df_maiores_por_mes = pd.concat([df_maiores_por_mes,df_maiores ], axis=1, ignore_index=False)

    return df_maiores_por_mes
