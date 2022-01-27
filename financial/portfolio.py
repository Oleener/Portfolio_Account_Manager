import re
import questionary
import sqlalchemy as sql
import pandas as pd
import os
from datetime import datetime

from financial.assets import *


def add_portfolio(user_session, engine):
  os.system("clear")
  print("Adding Portfolio:")
  print("---------------------")
  print("Portfolio:")
  print("Portfolio Type:")
  
  # Adding Portfolio Name. SHould be unique for the user
  is_portfolio_name_unique = False
  while not is_portfolio_name_unique:
    print("---------------------")
    portfolio_name = questionary.text("Enter Portfolio Name:").ask() 
    portfolio_df = pd.read_sql_query(f"SELECT * FROM portfolios JOIN users ON users.user_id = portfolios.user_id WHERE users.user_id = {user_session['user_id']} and portfolios.portfolio_name = '{portfolio_name}'", con=engine).squeeze()
    if not portfolio_df.empty:
      print("\n  You already have the portfolio with this name.\n") 
      try_again = questionary.confirm("Try to enter portfolio name again?").ask()
      if not try_again:
        return False
    else:
      is_portfolio_name_unique = True
      os.system("clear")
      print("Adding Portfolio:")
      print("---------------------")
      print(f"Portfolio: {portfolio_name}")
      print("Portfolio Type:")
    
  # Picking the type of the portfolio (DB table - portfolio_types)
  portfolio_types = pd.read_sql_query("select * from portfolio_types", con=engine)
  print("---------------------")
  print("Pick the type of the portfolio:")
  selected_portfolio_type = portfolio_types[portfolio_types['portfolio_type'] == questionary.select("", portfolio_types['portfolio_type'].to_list()).ask()].squeeze()
  
  os.system("clear")
  print("Adding Portfolio:")
  print("---------------------")
  print(f"Portfolio: {portfolio_name}")
  print(f"Portfolio Type: {selected_portfolio_type['portfolio_type']}")
  print("---------------------")
  
  create_portfolio = questionary.confirm("Do you want to add this portfolio?").ask()
  
  if create_portfolio:
    try:
      created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      insert_portfolio_query = f"INSERT INTO portfolios (portfolio_name, created_on, is_removed, user_id, portfolio_type_id) VALUES ('{portfolio_name}','{created_on}', False, {user_session['user_id']}, {selected_portfolio_type['portfolio_type_id']}) RETURNING portfolio_id"
      [portfolio_id] = engine.execute(insert_portfolio_query).fetchone()
      return pd.Series({'portfolio_id': portfolio_id, 'portfolio_name': portfolio_name, 'portfolio_type': selected_portfolio_type['portfolio_type']})
    except Exception:
      print("The following exception occurred while adding the portfolio:")
      print(Exception.with_traceback())
      questionary.text("Please press Enter to confirm").ask()
      return False
  else:
    return False

def get_portfolio_mode_choices(mode, is_email_verified, is_portfolios_assets_empty):
  if mode == 'Portfolio':
    choices = ['Add New Asset']
    if not is_portfolios_assets_empty:
      choices.append('Add Existing Asset') 
    if is_email_verified:
      choices.extend(['Show Detailed Portfolio Analysis', 'Remove Portfolio', 'Edit Portfolio', 'Go Back', 'Exit'])
    else:
      choices.extend(['Remove Portfolio', 'Edit Portfolio', 'Go Back', 'Exit'])
  else:
    choices = ['Add New Portfolio']
    if not is_portfolios_assets_empty:
      choices.append('Manage Portfolio')     
    if is_email_verified == True:
      choices.append('Exit')
    else:
      choices.extend(['Verify Email', 'Exit'])
  return choices
       
def get_portfolios(user_session, engine):
  portfolios_df = pd.read_sql_query(f"SELECT * FROM portfolios JOIN users ON users.user_id = portfolios.user_id  JOIN portfolio_types on portfolios.portfolio_type_id = portfolio_types.portfolio_type_id WHERE users.user_id = {user_session['user_id']} AND portfolios.is_removed = False", con=engine)
  return portfolios_df


def get_portfolio_info(portfolio, engine):
  assets_df = pd.read_sql_query(f"SELECT assets_in_portfolio.asset_in_portfolio_id, assets_in_portfolio.asset_code, assets_in_portfolio.asset_holdings, assets_in_portfolio.asset_avg_buy_price, assets_in_portfolio.asset_fixed_profit_loss_currency, assets_in_portfolio.asset_fixed_profit_loss_percentage, assets_in_portfolio.sum_of_investments, assets_in_portfolio.buy_total_amount, assets_in_portfolio.sold_total_amount, assets_in_portfolio.sold_total_currency,portfolio_types.portfolio_type FROM portfolios JOIN assets_in_portfolio ON assets_in_portfolio.portfolio_id = portfolios.portfolio_id JOIN portfolio_types ON portfolios.portfolio_type_id = portfolio_types.portfolio_type_id WHERE portfolios.portfolio_id = {portfolio['portfolio_id']}", con=engine)
  assets_df['current_price'] = [get_asset_price(row[0], row[1]) for row in zip(assets_df['portfolio_type'], assets_df['asset_code'])]
  assets_df['asset_balance'] = [float(row[0]) * float(row[1]) for row in zip(assets_df['asset_holdings'], assets_df['current_price'])]
  assets_df['asset_holdings_cost_avg_price'] = [row[0] * row[1] for row in zip(assets_df['asset_holdings'], assets_df['asset_avg_buy_price'])]
  assets_df['asset_total_profit_loss_currency'] = [row[0] + (row[1] - row[2] * row[3]) for row in zip(assets_df['asset_fixed_profit_loss_currency'], assets_df['asset_balance'], assets_df['asset_holdings'], assets_df['asset_avg_buy_price'])]
  assets_df['asset_total_profit_loss_percentage'] = [row[0] + (row[1] - row[2] * row[3])/row[4] for row in zip(assets_df['asset_fixed_profit_loss_percentage'], assets_df['asset_balance'], assets_df['asset_holdings'], assets_df['asset_avg_buy_price'], assets_df['sum_of_investments'])]

  portfolio['current_balance'] = assets_df['asset_balance'].sum()
  portfolio['sum_of_investments'] = assets_df['sum_of_investments'].sum()
 # portfolio['fixed_profit_loss_currency'] = assets_df['asset_fixed_profit_loss_currency'].sum()
 # portfolio['fixed_profit_loss_percentage'] = portfolio['fixed_profit_loss_currency'] / portfolio['sum_of_investments']
 # portfolio['all_holdings_cost'] = assets_df['asset_holdings_cost_avg_price'].sum()
 # portfolio['total_profit_loss_currency'] = (portfolio['current_balance'] - portfolio['all_holdings_cost']) + portfolio['fixed_profit_loss_currency']
 # portfolio['total_profit_loss_percentage'] = (portfolio['current_balance'] - portfolio['all_holdings_cost'])/portfolio['sum_of_investments'] + portfolio['fixed_profit_loss_percentage']
  portfolio['assets_count'] = assets_df.shape[0]
  
  return (portfolio, assets_df)

def remove_portfolio(portfolio, engine):
  os.system("clear")
  print(f"Removing Portfolio: {portfolio['portfolio_name']}")
  print("---------------------")
  remove_portfolio = questionary.confirm("Do you want to remove this portfolio?").ask()
  if remove_portfolio:
    try:
      engine.execute(f"UPDATE portfolios SET is_removed = True where portfolio_id = {portfolio['portfolio_id']}")
      print("---------------------------------")
      print("Portfolio was sucessfully removed")
      print("---------------------------------")
      questionary.text("Press Enter to continue").ask()
      return True
    except:
      print("---------------------------------")
      print("Something went wrong. Portfolio wasn't removed")
      print("---------------------------------")
      questionary.text("Press Enter to continue").ask()
      return False
  else:
    return False
      
def edit_portfolio_name(portfolio, engine):
  os.system("clear")
  print(f"Portfolio Name: {portfolio['portfolio_name']}")
  print("---------------------")
  new_portfolio_name = questionary.text("Enter new name for the portfolio: ").ask()
  os.system("clear")
  print(f"Portfolio Name (old): {portfolio['portfolio_name']}")
  print(f"Portfolio Name (new): {new_portfolio_name}")
  print("---------------------\n")
  save_new_name = questionary.confirm(f"Do you want to apply these changes?").ask()
  if save_new_name:
    try:
      engine.execute(f"UPDATE portfolios SET portfolio_name = '{new_portfolio_name}' where portfolio_id = {portfolio['portfolio_id']}")
      print("---------------------------------")
      print("Portfolio Name has been changed sucessfully")
      print("---------------------------------")
      questionary.text("Press Enter to continue").ask()
      return True
    except:
      print("---------------------------------")
      print("Something went wrong. Portfolio Name wasn't changed")
      print("---------------------------------")
      questionary.text("Press Enter to continue").ask()
      return False
  else:
    return False