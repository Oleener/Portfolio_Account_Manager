#import necassary libraries and dependencies 
from numpy import float64
import requests
import alpaca_trade_api as tradeapi
import json
from dotenv import load_dotenv
import os
import pandas as pd
import questionary
from datetime import datetime

#retrieve all api and secret keys
load_dotenv()
av_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
al_key_id = os.getenv("ALPACA_KEY_ID")
al_sec_key = os.getenv("ALPACA_SECRET_KEY")

#retreive asset's last price, 
def get_assets_last_prices(assets_type, assets_list):
  prices = pd.Series(dtype=float64)
  for asset in assets_list:
    prices[asset] = get_asset_price(assets_type, asset)
  return prices

# make sure the asset exists. 
# If it does then return that the asset exists and it's price. 
# If asset doesn't exist, returns false.
def is_asset_exist(asset_type, asset_code):
    try:
      get_asset_price(asset_type, asset_code)
      return True
    except Exception:
      return False

# function used to retrieve either stock or crypto asset price from api 
def get_asset_price(asset_type, asset_code):
  if asset_type == 'Crypto':
    url = f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={asset_code}&market=USD&interval=1min&apikey={av_api_key}"
    response = requests.get(url).json()
    df = df = pd.DataFrame(response['Time Series Crypto (1min)']).T
    price = df.iloc[0]['4. close']
    return float(price)
  if asset_type == "Stocks":
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={asset_code}&interval=1min&apikey={av_api_key}"
    response = requests.get(url).json()
    df = pd.DataFrame(response['Time Series (1min)']).T
    price = df.iloc[0]['4. close']
    return float(price)

# function used to retrieve asset price history in a time period of years
def get_assets_price_history(assets_type, assets_code, period_years = None):
  # historical data for crypto currency 
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
  # historical data for stocks
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
#Add more to an asset in a portfolio 
def add_transaction(portfolio, engine):
  os.system("clear")
  print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
  print(f"Type of the Asset: {portfolio['portfolio_type']}")
  print("---------------------")
  print("Asset Code:")
  
  # Add a new asset to the portfolio if it exists in the database 
  # and if it doesn't return a a try again prompt
  asset_exist = False
  while not asset_exist:
    print("---------------------")
    asset_code = questionary.text("Enter Asset Code:").ask()
    if is_asset_exist(portfolio['portfolio_type'], asset_code):
      asset_exist = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset_code}")
    else: 
      print(f"\n  The asset with {asset_code} code doesn't exist.\n") 
      try_again = questionary.confirm("Try to enter asset code again?").ask()
      if not try_again:
        return False
      
  #Checking if asset exists in the portfolio
  asset_in_portfolio_df = pd.read_sql_query(f"SELECT * FROM portfolios JOIN assets_in_portfolio ON portfolios.portfolio_id = assets_in_portfolio.portfolio_id WHERE portfolios.portfolio_id = {portfolio['portfolio_id']} AND assets_in_portfolio.asset_code = '{asset_code}'", con=engine).squeeze()
  if not asset_in_portfolio_df.empty:
    print("---------------------")
    proceed = questionary.confirm(f"{asset_code} is already presented in the portfolio. Do you want to proceed with the transaction?").ask()
    if not proceed:
      return False
    else: 
      return add_transaction_existing_asset(portfolio, asset_in_portfolio_df, engine)
  else:
    return add_transaction_new_asset(portfolio, asset_code, engine)
    
# New asset bought
def add_transaction_new_asset(portfolio, asset_code, engine):
  os.system("clear")
  print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
  print(f"Type of the Asset: {portfolio['portfolio_type']}")
  print("---------------------")
  print(f"Asset Code: {asset_code}")
  print("Transaction Date (YYYY-MM-DD):")
  print("Transaction Amount (in {asset_code}):")
  print("Price ({asset_code}/USD):")
  
  # Entering Transaction Date
  is_valid_date = False  
  while not is_valid_date:
    print("---------------------")
    try:
      transaction_date = datetime.strptime(questionary.text("Enter Transaction Date:").ask(), '%Y-%m-%d').date()
      is_valid_date = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset_code}")
      print(f"Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset_code}):")
      print(f"Price ({asset_code}/USD):")
    except:
      print(f"\n  Wrong date format.\n") 
      try_again = questionary.confirm("Try to enter the date of the transaction again?").ask()
      if not try_again:
        return False
      
  # Entering Transaction Amount   
  is_amount_valid = False  
  while not is_amount_valid:
    print("---------------------")
    try:
      transaction_amount = float(questionary.text(f"Enter Transaction Amount (in {asset_code}):").ask())
      is_amount_valid = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset_code}")
      print(f"Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset_code}): {transaction_amount}")
      print(f"Price ({asset_code}/USD):")
    except:
      print(f"\n  Wrong amount format.\n") 
      try_again = questionary.confirm("Try to enter the transaction amount again?").ask()
      if not try_again:
        return False
      
 # Entering Transaction Price   
  is_price_valid = False  
  while not is_price_valid:
    print("---------------------")
    try:
      transaction_price = float(questionary.text(f"Enter the Price ({asset_code}/USD):").ask())
      is_price_valid = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset_code}")
      print(f"Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset_code}): {transaction_amount}")
      print(f"Price ({asset_code}/USD): {transaction_price}")
      print("---------------------")
    except:
      print(f"\n  Wrong price format.\n") 
      try_again = questionary.confirm("Try to enter the price again?").ask()
      if not try_again:
        return False
      
  #add the asset to the database 
  create_asset = questionary.confirm("Do you want to add this transaction?").ask()
  if create_asset:
    try:
      transaction_amount_usd = transaction_amount * transaction_price
      insert_asset_query = f"INSERT INTO assets_in_portfolio (asset_code, asset_holdings, asset_avg_buy_price, asset_fixed_profit_loss_currency, asset_fixed_profit_loss_percentage, sum_of_investments, buy_total_amount, sold_total_amount, sold_total_currency, portfolio_id) VALUES ('{asset_code}', {transaction_amount}, {transaction_price}, 0, 0, {transaction_amount_usd}, {transaction_amount}, 0, 0, {portfolio['portfolio_id']}) RETURNING asset_in_portfolio_id"
      [asset_id] = engine.execute(insert_asset_query).fetchone()
      engine.execute(f"INSERT INTO asset_transactions (transaction_amount, transaction_price, tranaction_type, asset_in_portfolio_id) VALUES ({transaction_amount}, {transaction_price}, 'Buy', {asset_id})")
    except: 
      print("The following exception occurred while adding the asset:")
      print(Exception.with_traceback())
      questionary.text("Please press Enter to confirm").ask()
      return False
  else:
    return False

#turn database into a pandas DataFrame
def get_assets(portfolio, engine):
  assets_df = pd.read_sql_query(f"SELECT * FROM assets_in_portfolio JOIN portfolios ON portfolios.portfolio_id = assets_in_portfolio.portfolio_id WHERE portfolios.portfolio_id = {portfolio['portfolio_id']}", con=engine)
  return assets_df

#function to show adding an existing asset
def add_transaction_existing_asset(portfolio, asset, engine):
  os.system("clear")
  print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
  print(f"Type of the Asset: {portfolio['portfolio_type']}")
  print("---------------------")
  print(f"Asset Code: {asset['asset_code']}")
  print("Transaction Type:")
  print("Transaction Date (YYYY-MM-DD):")
  print(f"Transaction Amount (in {asset['asset_code']}):")
  print(f"Price ({asset['asset_code']}/USD):")
  print("---------------------")
  
  transaction_type = questionary.select("Select the transaction type:", ['Buy', 'Sell']).ask()
  os.system("clear")
  print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
  print(f"Type of the Asset: {portfolio['portfolio_type']}")
  print("---------------------")
  print(f"Asset Code: {asset['asset_code']}")
  print(f"Transaction Type: {transaction_type}")
  print("Transaction Date (YYYY-MM-DD):")
  print(f"Transaction Amount (in {asset['asset_code']}):")
  print(f"Price ({asset['asset_code']}/USD):")
  
  # Entering Transaction Date
  is_valid_date = False  
  while not is_valid_date:
    print("---------------------")
    try:
      transaction_date = datetime.strptime(questionary.text("Enter Transaction Date:").ask(), '%Y-%m-%d').date()
      is_valid_date = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset['asset_code']}")
      print(f"Transaction Type: {transaction_type}")
      print(f"Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset['asset_code']}):")
      print(f"Price ({asset['asset_code']}/USD):")
    except:
      print(f"\n  Wrong date format.\n") 
      try_again = questionary.confirm("Try to enter the date of the transaction again?").ask()
      if not try_again:
        return False
      
  # Entering Transaction Amount   
  is_amount_valid = False  
  while not is_amount_valid:
    print("---------------------")
    try:
      transaction_amount = float(questionary.text(f"Enter Transaction Amount (in {asset['asset_code']}):").ask())
      is_amount_valid = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset['asset_code']}")
      print(f"Transaction Type: {transaction_type}")
      print(f"Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset['asset_code']}): {transaction_amount}")
      print(f"Price ({asset['asset_code']}/USD):")
    except:
      print(f"\n  Wrong amount format.\n") 
      try_again = questionary.confirm("Try to enter the transaction amount again?").ask()
      if not try_again:
        return False
      
 # Entering Transaction Price   
  is_price_valid = False  
  while not is_price_valid:
    print("---------------------")
    try:
      transaction_price = float(questionary.text(f"Enter the Price ({asset['asset_code']}/USD):").ask())
      is_price_valid = True
      os.system("clear")
      print(f"Adding new transaction for the Portfolio: {portfolio['portfolio_name']}")
      print(f"Type of the Asset: {portfolio['portfolio_type']}")
      print("---------------------")
      print(f"Asset Code: {asset['asset_code']}")
      print(f"Transaction Type: {transaction_type}")
      print("Transaction Date (YYYY-MM-DD): {transaction_date}")
      print(f"Transaction Amount (in {asset['asset_code']}): {transaction_amount}")
      print(f"Price ({asset['asset_code']}/USD): {transaction_price}")
      print("---------------------")
    except:
      print(f"\n  Wrong price format.\n") 
      try_again = questionary.confirm("Try to enter the price again?").ask()
      if not try_again:
        return False
  create_transaction = questionary.confirm("Do you want to add this transaction?").ask()
  if create_transaction:
    try:
      transaction_amount_usd = transaction_amount * transaction_price
      if transaction_type == 'Sell':
        new_holdings = asset['asset_holdings'] - transaction_amount
        new_sold_total_amount = asset['sold_total_amount'] + transaction_amount
        new_sold_total_currency = asset['sold_total_currency'] + transaction_amount_usd
        new_asset_fixed_profit_loss_currency = asset['asset_fixed_profit_loss_currency'] + (transaction_amount_usd - transaction_amount * asset['asset_avg_buy_price'])
        new_asset_fixed_profit_loss_percentage = new_asset_fixed_profit_loss_currency / asset['sum_of_investments']
        engine.execute(f"UPDATE assets_in_portfolio SET asset_holdings = {new_holdings}, asset_fixed_profit_loss_currency = {new_asset_fixed_profit_loss_currency}, asset_fixed_profit_loss_percentage = {new_asset_fixed_profit_loss_percentage}, sold_total_amount = {new_sold_total_amount}, sold_total_currency = {new_sold_total_currency}  WHERE asset_in_portfolio_id = {asset['asset_in_portfolio_id']}")
        engine.execute(f"INSERT INTO asset_transactions (transaction_amount, transaction_price, tranaction_type, asset_in_portfolio_id) VALUES ({transaction_amount}, {transaction_price}, '{transaction_type}', {asset['asset_in_portfolio_id']})")
      elif transaction_type == 'Buy':
        new_holdings = asset['asset_holdings'] + transaction_amount
        new_sum_of_investments = asset['sum_of_investments'] + transaction_amount_usd
        new_buy_total_amount = asset['buy_total_amount'] + transaction_amount
        new_asset_avg_buy_price = new_sum_of_investments / new_buy_total_amount
        new_asset_fixed_profit_loss_currency = asset['sold_total_currency'] - asset['sold_total_amount'] * new_asset_avg_buy_price
        new_asset_fixed_profit_loss_percentage = new_asset_fixed_profit_loss_currency / new_sum_of_investments
        engine.execute(f"UPDATE assets_in_portfolio SET asset_holdings = {new_holdings}, sum_of_investments = {new_sum_of_investments}, buy_total_amount = {new_buy_total_amount}, asset_fixed_profit_loss_currency = {new_asset_fixed_profit_loss_currency}, asset_fixed_profit_loss_percentage = {new_asset_fixed_profit_loss_percentage}, asset_avg_buy_price = {new_asset_avg_buy_price}  WHERE asset_in_portfolio_id = {asset['asset_in_portfolio_id']}")
        engine.execute(f"INSERT INTO asset_transactions (transaction_amount, transaction_price, tranaction_type, asset_in_portfolio_id) VALUES ({transaction_amount}, {transaction_price}, '{transaction_type}', {asset['asset_in_portfolio_id']})")
    except: 
      print("The following exception occurred while adding the asset:")
      print(Exception.with_traceback())
      questionary.text("Please press Enter to confirm").ask()
      return False
  else:
    return False  
  print(get_assets_price_history('Crypto', ['BTC', 'ETH', 'XRP'], period_years = 1))