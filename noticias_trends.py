import pandas as pd
from pytrends.request import TrendReq

'''
Google trends
'''
def busca_google_trends(company_name, timeframe='today 3-y', geo='BR'):

    interest_over_time_df = None

    try:
        pytrends = TrendReq(hl='pt-BR', tz=360)
        pytrends.build_payload(kw_list=[company_name], geo=geo,timeframe=timeframe )

        # Obtemos os dados de interesse ao longo do tempo
        interest_over_time_df = pytrends.interest_over_time()

        interest_over_time_df = interest_over_time_df.reset_index(drop=False)
        interest_over_time_df = interest_over_time_df.rename(columns={'date' :'Data'})
    except:
        return None

    return interest_over_time_df