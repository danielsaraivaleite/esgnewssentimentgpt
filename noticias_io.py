'''
Módulo do modelo de analise de sentimento usando chat gpt
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
'''

import pandas as pd

arquivo_termos_esg = 'datasets/palavras_chave_esg.xlsx'
base_noticias = 'datasets/base_noticias.parquet'
lista_empresas = 'datasets/lista_empresas.xlsx'
arquivo_termos_esg = 'datasets/palavras_chave_esg.xlsx'
base_noticias_saida = 'datasets/sentimento_base_noticias.parquet'
base_noticias_saida_short = 'datasets/sentimento_base_noticias_short.parquet'
caminho_cache='datasets/gpt_cache.xlsx'
colunas_data = ['data_publicacao', 'ultima_data_publicacao', 'data']

def __ajusta_datas_df(df):
    
    for c in colunas_data:
        if c in list(df.columns):
            if not pd.api.types.is_datetime64_dtype(  df[c]  ):
                df[c] = pd.to_datetime(df[c])
    return df
            

def __le_excel_df(caminho):
    return pd.read_excel(caminho)


def __le_parquet_df(caminho):
    return __ajusta_datas_df(pd.read_parquet(caminho))


def __salva_excel_df(df, caminho):
    return df.to_excel(caminho, index=False)


def __salva_parquet_df(df, caminho):
    df = __ajusta_datas_df(df)
    return df.to_parquet(caminho)


def __le_base_df(caminho):
    if caminho.upper().endswith('.XLSX') or caminho.upper().endswith('.XLS') or caminho.upper().endswith('.XLSB'):
        return __le_excel_df(caminho)
    elif caminho.upper().endswith('.PARQUET'):
        return __le_parquet_df(caminho)
    else:
        
        return None

def __salva_base_df(df, caminho):
    if caminho.upper().endswith('.XLSX') or caminho.upper().endswith('.XLS') or caminho.upper().endswith('.XLSB'):
        return __salva_excel_df(df, caminho)
    elif caminho.upper().endswith('.PARQUET'):
        return __salva_parquet_df(df, caminho)
    else:
        return None
        

def le_base_noticias_bruta_para_df():
    return __le_base_df(base_noticias)

def salva_base_noticias_bruta(df):
    return __salva_base_df(df, base_noticias)

def le_base_noticias_processada_para_df():
    return __le_base_df(base_noticias_saida)

def salva_base_noticias_processada(df):
    return __salva_base_df(df, base_noticias_saida)

def le_base_noticias_compacta_para_df():
    return __le_base_df(base_noticias_saida_short)

def salva_base_noticias_compacta(df):
    return __salva_base_df(df, base_noticias_saida_short)

def le_termos_esg_para_df():
    return __le_base_df(arquivo_termos_esg)

def le_cache_gpt_para_df():
    return __le_base_df(caminho_cache)

def salva_cache_gpt(df):
    return __salva_base_df(df, caminho_cache)

def le_lista_empresas_para_df():
    return __le_base_df(lista_empresas)

def salva_lista_empresas(df):
    return __salva_base_df(df, lista_empresas)






    
    