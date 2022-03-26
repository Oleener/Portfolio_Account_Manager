def format_performance_percentage(number):
  if float(number) > 0:
    #number *= 100     
    formatted_number = f"+{number:.2f}%"
  elif float(number) == 0:
    formatted_number = f"{number:.2f}%"
  else:
    formatted_number = f"-{number:.2f}%"
  return formatted_number

def format_performance_currency(number):
  if float(number) > 0:
    formatted_number = f"+${number:.2f}"
  elif float(number) == 0:
    formatted_number = f"${number:.2f}"
  else:
    formatted_number = f"-${number:.2f}"
  return formatted_number

def generate_detailed_portfolio_string(portfolio_name, portfolio_balance, portfolio_performance_percentage, porfolio_performance_currency):
  portfolio_performance_percentage = format_performance_percentage(portfolio_performance_percentage)
  porfolio_performance_currency = format_performance_currency(porfolio_performance_currency)
  return f"{portfolio_name}: ${portfolio_balance:.2f}, {portfolio_performance_percentage}({porfolio_performance_currency})"

def generate_detailed_portfolio_string_short(portfolio_name, portfolio_balance, portfolio_number_assets):
  return f"{portfolio_name} - Portfolio Balance: ${portfolio_balance:.2f}; Number of Assets: {portfolio_number_assets}"

  # {'asset_id': [1], 'asset_code': ['XRP'], 'asset_name': ['Ripple XRP'], 'asset_holdings': [10000], 'asset_avg_buy_price': [0.8], 'asset_balance': [8351.45], 'asset_performance_percentage': [7.25], 'asset_performance_currency': [500.25]}
  
def generate_detailed_asset_string(asset_code, asset_holdings, asset_avg_buy_price, asset_total_profit_loss_currency, asset_total_profit_loss_percentage, asset_balance, current_price): 
  asset_performance_percentage = format_performance_percentage(asset_total_profit_loss_percentage)
  asset_performance_currency = format_performance_currency(asset_total_profit_loss_currency)
  return f"{asset_code} - {asset_holdings} {asset_code}; Price: ${current_price}; Balance: ${asset_balance:.2f}; Avg Buy Price: ${asset_avg_buy_price:.2f}; Total Profit/Loss: {asset_performance_percentage}({asset_performance_currency})"

#Function to gather asset info and generate a string to show details on asset in Asset Mode
def generate_asset_mode_string(asset, portfolio):
  portfolio_performance_percentage = format_performance_percentage(asset['asset_total_profit_loss_percentage'])
  porfolio_performance_currency = format_performance_currency(asset['asset_total_profit_loss_currency'])
  asset_info_str = f"""
Asset Management Mode
-------------------------
Managing asset: {asset['asset_code']}
Portfolio: {portfolio['portfolio_name']}
----------------------------
Asset holdings: {asset['asset_holdings']}
Asset average buy price: ${asset['asset_avg_buy_price']}
Asset investment: ${asset['sum_of_investments']}
Asset current price: ${asset['current_price']}
Asset current balance: ${asset['asset_balance']}
Asset total profit/loss: {porfolio_performance_currency}({portfolio_performance_percentage})
----------------------------
"""
  return asset_info_str