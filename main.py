from binance.client import Client
from datetime import datetime
import pandas as pd
import requests
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

from bs4 import BeautifulSoup


## Converting the open_time and close_time to a readable timestamps
def conversion_date(timestamp):
    date = int(timestamp)/1000
    return datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    


api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

symbols = client.get_exchange_info()

crypto_tot = []

for i in range(len(symbols['symbols'])):
    crypto_tot.append(symbols['symbols'][i]['symbol'])



all_coins_dict = json.loads(BeautifulSoup(
        requests.get('http://coincap.io/front').content, "html.parser").prettify())
all_coins_df = pd.DataFrame(all_coins_dict)
coins_by_mcap = all_coins_df[all_coins_df.mktcap > 1e9]
coin_portfolio = coins_by_mcap['short']
print("Portfolio coins with MCAP > 1 Billion :\n",coin_portfolio.values)




print('Lenght of the crypto_portfolio: ', len(coin_portfolio)) 

crypto_portfolio = coin_portfolio.tolist()
crypto_portfolio.remove('USDT') 

crypto_portfolio.remove('BCH') 
crypto_portfolio.remove('IOT') 

crypto_portfolio.append('BCC')
crypto_portfolio.append('IOTA')

columns = coin_portfolio.tolist()

df_all= pd.DataFrame(columns=columns)

crypto_search_tickers = []
for crypto in crypto_portfolio:
    if crypto + 'USDT' in crypto_tot:
        crypto_search_tickers.append(crypto + 'USDT')
    else:
        crypto_search_tickers.append(crypto + 'BTC')

i = 0
for crypto in crypto_search_tickers:
    klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR , "1 Dec, 2017", "25 Sept, 2018")
    
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',\
                                   'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', \
                                   'taker_buy_quote_asset_volume', 'ignored'])
    df['open_time'] = df['open_time'].apply(lambda x : conversion_date(x))
    df['close_time'] = df['close_time'].apply(lambda x : conversion_date(x))
    df = df[['open_time', 'close']]
    df['close'] = df['close'].astype('float64')
    df.rename({'close': crypto}, axis=1, inplace=True)
    df.set_index('open_time', inplace=True)
    
    if i == 0:
        df_all = df.copy()
    else:
    #df_all = df_all.join(df)
        df_all.loc[:,crypto] = pd.Series(df[crypto], index=df.index)
    i += 1

df_all.to_csv('crypto_df_1H_prices'+ str(int(time.time()))+'.csv')
