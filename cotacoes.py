
from datetime import datetime
import requests
import pandas as pd

def busca_cotacao(simbolo):

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