'''
Módulo que implementa o modelo de avaliação de sentimentos aplicado as noticias ESG
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
Trabalho de conclusão de curso - MBA Digital Business USP Esalq
'''


import warnings
import pandas as pd
import numpy as np
import datetime  as dt
from scipy import interpolate
import scipy.stats
from scipy.interpolate import make_interp_spline
from noticias_timeline import plota_timeline
from noticias_processamento_texto import *
import re
    

def gera_curva_polaridade_media(dfNoticiasComPolaridade, empresa, dimensao, maxima_data=None, alfa=0.07, grau_polinomio=5):
    '''
    Gera a curva de polaridade média - modelo EWMA e interpolação
    '''
    dfPolaridade = dfNoticiasComPolaridade
    
    if maxima_data is not None:
        dfPolaridade = dfPolaridade[dfPolaridade['data_publicacao'].dt.date <= maxima_data]
    
    if empresa != '':
        dfPolaridade = dfPolaridade[dfPolaridade['empresa'] == empresa]
    if dimensao != '' and dimensao != 'ESG':
        dfPolaridade = dfPolaridade[dfPolaridade['classificacao'] == dimensao]
        
    dfPolaridade['data_publicacao'] = pd.to_datetime(pd.to_datetime(dfPolaridade['data_publicacao']).dt.date)
    
    dfPolaridade = dfPolaridade.set_index('data_publicacao')
    dfPolaridade = dfPolaridade.groupby(by='data_publicacao').agg({'polaridade' : 'sum', 'titulo': 'count'})
    
    #dfPolaridade = dfPolaridade.set_index('data_publicacao').groupby([pd.Grouper(freq="D")]).agg({'polaridade' : 'sum', 'titulo': 'count'})
    dfPolaridade['polaridade'] = dfPolaridade['polaridade'] / dfPolaridade['titulo']
    dfPolaridade = dfPolaridade.sort_index()
    #dfPolaridade['polaridade'] = dfPolaridade.interpolate(method='time')['polaridade']
    
    if len(dfPolaridade) <= grau_polinomio:
        return None
    
    dfPolaridade['polaridade_ewma'] = dfPolaridade.ewm(alpha=alfa, adjust=True).mean()['polaridade']
 
    #c = np.polyfit( np.linspace(0,1,len(dfPolaridade))  , dfPolaridade['polaridade_ewma'], grau_polinomio) #polinomio grau X
    #poly_eqn = np.poly1d(c)
    #y_hat = poly_eqn(np.linspace(0,1,len(dfPolaridade)))
    #dfPolaridade['polaridade_fit'] = y_hat    
    
    dfPolaridade['polaridade_fit'] = dfPolaridade['polaridade_ewma']   
    

    return dfPolaridade





