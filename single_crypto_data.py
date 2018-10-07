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

parser.add_argument('--C', dest='crypto',
                    help='Ticker of the cryptocurrency to get data')

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





crypto_search_ticker = ''
if args.crypto + 'USDT' in crypto_tot:
    crypto_search_ticker = args.crypto + 'USDT'
else:
    crypto_search_ticker  = args.crypto + 'BTC'



if args.freq == '1m':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_1MINUTE , args.initial_date, args.final_date)

if args.freq == '3m':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_3MINUTE , args.initial_date, args.final_date)

if args.freq == '5m':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_5MINUTE , args.initial_date, args.final_date)

if args.freq == '15m':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_15MINUTE , args.initial_date, args.final_date)

if args.freq == '30m':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_30MINUTE , args.initial_date, args.final_date)

if args.freq == '1h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_1HOUR , args.initial_date, args.final_date)

if args.freq == '2h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_2HOUR , args.initial_date, args.final_date)

if args.freq == '4h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_4HOUR , args.initial_date, args.final_date)

if args.freq == '6h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_6HOUR , args.initial_date, args.final_date)

if args.freq == '8h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_8HOUR , args.initial_date, args.final_date)

if args.freq == '12h':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_12HOUR , args.initial_date, args.final_date)

if args.freq == '1d':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_1DAY , args.initial_date, args.final_date)

if args.freq == '3d':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_3DAY , args.initial_date, args.final_date)

if args.freq == '1w':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_1WEEK , args.initial_date, args.final_date)

if args.freq == '1M':
    klines = client.get_historical_klines(crypto_search_ticker, Client.KLINE_INTERVAL_1MONTH , args.initial_date, args.final_date)

    
df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',\
                                   'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', \
                                   'taker_buy_quote_asset_volume', 'ignored'])
df['open_time'] = df['open_time'].apply(lambda x : conversion_date(x))
df['close_time'] = df['close_time'].apply(lambda x : conversion_date(x))
df['open'] = df['open'].astype('float64')
df['high'] = df['high'].astype('float64')
df['low'] = df['low'].astype('float64')
df['close'] = df['close'].astype('float64')
df['volume'] = df['volume'].astype('float64')
df.set_index('open_time', inplace=True)
    
name_df = f"df_{args.crypto}-{args.initial_date}-{args.final_date}-FREQ-{args.freq}"
df.to_csv(name_df+'.csv')
