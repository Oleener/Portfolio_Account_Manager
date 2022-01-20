def format_performance_percentage(number):
  if float(number) > 0:
    formatted_number = f"+{number:.2f}%"
  elif float(number) == 0:
    formatted_number = f"{number:.2f}%"
  else:
    formatted_number = f"{number:.2f}%"
  return formatted_number

def format_performance_currency(number):
  if float(number) > 0:
    formatted_number = f"+${number:.2f}"
  elif float(number) == 0:
    formatted_number = f"${number:.2f}"
  else:
    formatted_number = f"${number:.2f}"
  return formatted_number

def generate_detailed_portfolio_string(portfolio_name, portfolio_balance, portfolio_performance_percentage, porfolio_performance_currency):
  portfolio_performance_percentage = format_performance_percentage(portfolio_performance_percentage)
  porfolio_performance_currency = format_performance_currency(porfolio_performance_currency)
  return f"{portfolio_name} - ${portfolio_balance:.2f}, {portfolio_performance_percentage}({porfolio_performance_currency})"

  # {'asset_id': [1], 'asset_code': ['XRP'], 'asset_name': ['Ripple XRP'], 'asset_holdings': [10000], 'asset_avg_buy_price': [0.8], 'asset_balance': [8351.45], 'asset_performance_percentage': [7.25], 'asset_performance_currency': [500.25]}
  
def generate_detailed_asset_string(asset_name, asset_code, asset_holdings, asset_balance, asset_performance_percentage, asset_performance_currency): 
  asset_performance_percentage = format_performance_percentage(asset_performance_percentage)
  asset_performance_currency = format_performance_currency(asset_performance_currency)
  return f"{asset_name} ({asset_code}): {asset_holdings} {asset_code} - ${asset_balance:.2f}, {asset_performance_percentage}({asset_performance_currency})"