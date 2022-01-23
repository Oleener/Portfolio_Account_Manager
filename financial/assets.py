from numpy import float64
import requests
import alpaca_trade_api as tradeapi
import json
from dotenv import load_dotenv
import os
import pandas as pd
from sympy import symbols

load_dotenv()
av_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
al_key_id = os.getenv("ALPACA_KEY_ID")
al_sec_key = os.getenv("ALPACA_SECRET_KEY")

def get_asset_price(asset_type, asset_code):
  if asset_type == 'Crypto':
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={asset_code}&to_currency=USD&apikey={av_api_key}"
    response = requests.get(url).json()
    price = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    print(f"The current price of {asset_code} is {price}")
  if asset_type == "Stocks":
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={asset_code}&interval=1min&apikey={av_api_key}"
    response = requests.get(url).json()
    df = pd.DataFrame(response['Time Series (1min)']).T
    print(f"The close price of {asset_code} is {df.iloc[0]['4. close']}")
    #print(json.dumps(response, indent=4))

def get_assets_price_history(assets_type, assets_code, period_years = None):
  if assets_type == 'Crypto':
    assets_df = pd.DataFrame()
    for asset in assets_code:
      url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={asset}&market=USD&apikey={av_api_key}'
      response = requests.get(url).json()
      df = pd.DataFrame(response['Time Series (Digital Currency Daily)']).T
      df = df['4a. close (USD)']
      df.index = pd.to_datetime(df.index)
      df.name = asset
      df = df.astype(float)
      if period_years:
        start_date = (pd.Timestamp.today()- pd.Timedelta(days = 365 * period_years))
        df =  df[df.index > start_date] 
      assets_df[asset] = df
    df.index.name = 'Date'
    return assets_df
  if assets_type == 'Stocks':
    alpaca = tradeapi.REST(key_id=al_key_id, secret_key=al_sec_key, api_version='v2')
    df = alpaca.get_barset(symbols = assets_code, timeframe='1D', limit=1000).df

    df.index.name = 'Date'
    if period_years:
      start_date = (pd.Timestamp.today() - pd.Timedelta(days = 365 * period_years)).isoformat()
      df =  df[df.index > start_date]
    assets_df = pd.DataFrame()
    for asset in assets_code:
      assets_df[asset] = df[asset]['close']
    assets_df.index = assets_df.index.date
    return assets_df
      

print(get_assets_price_history('Crypto', ['XRP', 'BTC'], period_years = 1))
print(get_assets_price_history('Stocks', ['AAPL', 'MSFT'], period_years = 1))