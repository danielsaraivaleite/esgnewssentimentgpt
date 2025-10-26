#!/usr/bin/env python
# coding: utf-8

# In[51]:



from datetime import datetime
import requests
import pandas as pd
from pandas.tseries.offsets import DateOffset

def busca_cotacao(simbolo):

    # busca site itau corretora, maximo 1 ano
    url = 'https://www.itaucorretora.com.br/Grafico/CotacoesMultilinha?papeis=' + simbolo + '&periodo=D'

    df = None

    try:
        r = requests.get(url)

        j = r.json()

        df = pd.concat([pd.DataFrame.from_dict(j['categories']['category']), pd.DataFrame.from_dict(j['dataset'][0]['data'])], axis=1)

        df['Data'] = pd.to_datetime(df['name'].apply(lambda x: datetime.utcfromtimestamp(int(x)/1000).strftime('%Y-%m-%d %H:%M:%S UTC') )).dt.tz_localize(None).dt.date

        df = df.rename(columns={'value': 'Cotação'})

        df = df.loc[:, ['Data', 'Cotação']]

    except:
        pass;
    
    return df


# In[86]:





# In[74]:


pd.read_html('https://www.idinheiro.com.br/investimentos/cnpj-empresas-listadas-b3/')[0]
listagem['cnpj_raiz'] = listagem.CNPJ.str[:-8].str.replace('.', '').astype(int)


# In[ ]:





# In[58]:


listagem_filtro = listagem[:50]


# In[89]:


import pandas as pd
import numpy as np
import re

def explode_codigos(df, col_codigos='Código(s)', novo_nome='Código'):
    """
    Transforma um DataFrame onde a coluna de códigos/tickers contém várias ações
    na mesma célula (ex.: 'ALPA3 ALPA4' ou 'RPAD3 RPAD5 RPAD6') em um DataFrame
    com um único ticker por linha, repetindo as demais colunas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada com a coluna `col_codigos`.
    col_codigos : str, default 'Código(s)'
        Nome da coluna que contém 1..n tickers por célula.
    novo_nome : str, default 'Código'
        Nome da coluna resultante com um único ticker por linha.

    Retorna
    -------
    pd.DataFrame
        Novo DataFrame com uma linha por ticker.
    """

    if col_codigos not in df.columns:
        raise ValueError(f"Coluna '{col_codigos}' não encontrada no DataFrame.")

    df2 = df.copy()

    # Normaliza o tipo para string onde houver valores não nulos
    serie = df2[col_codigos].astype('string')

    # Função para:
    # - dividir por separadores comuns (espaço, vírgula, ponto-e-vírgula)
    # - limpar espaços
    # - remover vazios
    # - padronizar para maiúsculas
    # - remover duplicados preservando a ordem
    def split_normalizar(s):
        if pd.isna(s):
            return [pd.NA]
        # separa por vírgula, ponto-e-vírgula ou qualquer espaço
        partes = re.split(r'[,\s;]+', str(s).strip())
        partes = [p.strip().upper() for p in partes if p and p.strip()]
        # remove duplicados preservando ordem
        seen = set()
        unicos = []
        for p in partes:
            if p not in seen:
                seen.add(p)
                unicos.append(p)
        return unicos if unicos else [pd.NA]

    # Cria lista de tickers por linha
    df2['_lista_tickers'] = serie.apply(split_normalizar)

    # Explode para ter uma linha por ticker
    out = df2.explode('_lista_tickers', ignore_index=True)

    # Renomeia a coluna explodida
    out = out.rename(columns={'_lista_tickers': novo_nome})

    # Opcional: remover linhas sem ticker válido (NaN)
    out = out[~out[novo_nome].isna()].copy()

    # Se quiser, reposicionar a coluna de ticker ao lado da antiga:
    # (ou remover a coluna original de códigos múltiplos)
    cols = list(out.columns)
    # Move a nova coluna 'Código' para imediatamente após a coluna original
    if novo_nome in cols and col_codigos in cols:
        cols.remove(novo_nome)
        pos = cols.index(col_codigos) + 1
        cols = cols[:pos] + [novo_nome] + cols[pos:]
        out = out[cols]

    return out


# In[59]:


def calcular_variacoes(df):
    """
    Calcula variações percentual mensal (1M), trimestral (3M), semestral (6M) e anual (12M)
    considerando que pode não haver negociação no dia exato alvo.
    Nesses casos, usa a data de negociação mais próxima (anterior ou posterior).
    
    Parâmetros:
        df (pd.DataFrame): colunas ['Data', 'Cotação']; 'Data' pode ser str ou datetime.
    Retorna:
        tuple: (var_mensal, var_trimestral, var_semestral, var_anual)
               Cada variação = (preco_final / preco_ref) - 1, ou None se não houver base.
    """
    if df is None or df.empty:
        return (None, None, None, None)

    # Preparação
    df = df.copy()
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values('Data').set_index('Data')
    if 'Cotação' not in df.columns:
        raise ValueError("DataFrame deve conter a coluna 'Cotação'.")

    idx = df.index
    preco_final = df['Cotação'].iloc[-1]
    data_final = idx[-1]

    # Alvos por deslocamento de meses
    alvos = {
        'mensal':    data_final - DateOffset(months=1),
        'trimestral':data_final - DateOffset(months=3),
        'semestral': data_final - DateOffset(months=6),
        'anual':     data_final - DateOffset(months=12),
    }

    def preco_mais_proximo(data_alvo):
        # Usa indexador 'nearest' do DatetimeIndex; requer índice ordenado (já está)
        try:
            pos = idx.get_indexer([data_alvo], method='nearest')[0]
            if pos == -1:
                return None
            return df['Cotação'].iloc[pos]
        except Exception:
            # Fallback manual se 'nearest' não estiver disponível por alguma razão
            import numpy as np
            diffs = np.abs((idx - data_alvo).values.astype('timedelta64[ns]').astype('int64'))
            if len(diffs) == 0:
                return None
            pos = diffs.argmin()
            return df['Cotação'].iloc[pos]

    variacoes = []
    for _, data_ref in alvos.items():
        preco_ref = preco_mais_proximo(data_ref)
        if preco_ref is None or pd.isna(preco_ref) or pd.isna(preco_final):
            variacoes.append(None)
        else:
            variacoes.append((preco_final / preco_ref) - 1)

    # Ordem: mensal, trimestral, semestral, anual
    return tuple(variacoes)


# In[60]:


calcular_variacoes(df_cotacoes)


# In[ ]:





# In[61]:





# In[92]:


listagem_filtro = explode_codigos(listagem_filtro)
listagem_filtro['variacoes'] = listagem_filtro['Código'].apply(lambda x : calcular_variacoes(busca_cotacao(x)))
listagem_filtro


# In[ ]:





# In[ ]:




