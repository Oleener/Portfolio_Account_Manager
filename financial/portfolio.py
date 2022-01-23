import questionary
import sqlalchemy as sql
import pandas as pd
import os
from datetime import datetime


def add_portfolio(user_session, engine):
  os.system("clear")
  print("Adding Portfolio:")
  print("---------------------")
  print(f"Portfolio:")
  print(f"Portfolio Type:")
  
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
      print("The following exception occurred during the registration process:")
      print(Exception.with_traceback())