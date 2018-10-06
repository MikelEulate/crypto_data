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

import argparse

parser = argparse.ArgumentParser(description='This script is made to retrieve historical cryptocurrencies data from Binance')

parser.add_argument('--I', dest='initial_date',
                    help='initial date to retrieve data')
parser.add_argument('--F', dest='final_date',
                    help='Final date to retrieve data')

parser.add_argument('--Freq', dest='freq',
                    help='Frequency of de data stored')

# The arguments will be saved into args variable
args = parser.parse_args()

print(args)

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

    if args.freq == '1m':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1MINUTE , args.initial_date, args.final_date)

    if args.freq == '3m':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_3MINUTE , args.initial_date, args.final_date)

    if args.freq == '5m':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_5MINUTE , args.initial_date, args.final_date)

    if args.freq == '15m':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_15MINUTE , args.initial_date, args.final_date)

    if args.freq == '30m':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_30MINUTE , args.initial_date, args.final_date)

    if args.freq == '1h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR , args.initial_date, args.final_date)

    if args.freq == '2h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_2HOUR , args.initial_date, args.final_date)

    if args.freq == '4h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_4HOUR , args.initial_date, args.final_date)

    if args.freq == '6h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_6HOUR , args.initial_date, args.final_date)

    if args.freq == '8h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_8HOUR , args.initial_date, args.final_date)

    if args.freq == '12h':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_12HOUR , args.initial_date, args.final_date)

    if args.freq == '1d':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY , args.initial_date, args.final_date)

    if args.freq == '3d':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_3DAY , args.initial_date, args.final_date)

    if args.freq == '1w':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1WEEK , args.initial_date, args.final_date)

    if args.freq == '1M':
        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1MONTH , args.initial_date, args.final_date)

    
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

name_df = f"crypto_df_{args.initial_date}-{args.final_date}-FREQ-{args.freq}"
df_all.to_csv(name_df+'.csv')
