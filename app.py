import pandas as pd
import numpy as np
import sqlalchemy as sql
from sqlalchemy import inspect
import questionary 
import fire
import os
import sys
import dotenv

from utils.formatters import *
from utils.authentication import *
from financial.portfolio import *
from financial.assets import *

# Defining a PostgreSQL connection string
db_connection_string = "postgresql+psycopg2://airgsfjw:lf0yqypx53HpPomnz_l3LXJZXMMufFay@kashin.db.elephantsql.com/airgsfjw"

engine = sql.create_engine(db_connection_string)


def inspect_db(engine):
  return inspect(engine).get_table_names() 

# Initialize the app
def run():
  # First step is authentication
  os.system("clear")
  print("Welcome to Portfolio Manager!!!")
  print("_______________________________", end = '\n\n')
  print("Please log in to your account or sign up if you don't have one.", end='\n\n')
  
  # Providing the user with options to pick from - "Log in", "Sign up", "Exit"    
  login_mode_choice = questionary.select("", choices = ["Log in", "Sign up", "Exit"], use_shortcuts=True).ask()
   
  # If User selects to Sign Up
  if login_mode_choice == 'Sign up':
    # Running a sign up flow
    sign_up_result = user_signup(engine) 
    #user_info = pd.Series({'user_id':1, 'user_first_name':'Kirill', 'user_last_name':'Panov', 'user_email':'us.kirpa1986@gmail.com', 'is_email_verified':False})
    if isinstance(sign_up_result, bool):
      sys.exit() 
    else:
      user_session = sign_up_result
      global_mode = True
      os.system("clear")
      print(f"Hey {user_session['user_first_name']}! Your account has been successfully created.", end = '\n\n')
  elif login_mode_choice == 'Log in':
    # Returns True and Series with user info (see user_info as a test example) when user is logged in successfully, or False otherwise
    login_result = user_login(engine)    
    if isinstance(login_result, bool):
      sys.exit() 
    else:
      user_session = login_result
      global_mode = True
      os.system("clear")
      print(f"Hey {user_session['user_first_name']}! You are successfully logged in.", end = '\n\n')
  elif login_mode_choice == 'Exit':
    print("Buy-buy! ")
    sys.exit()
  
  # Check if user's email is verified
  if user_session['is_email_verified'] == False: 
    print(f"Your email {user_session['user_email']} is not verified!", end = '\n\n')
    print("The following functionality won't be available for you:", end='\n\n')
    print("- Deep Portfolio Analysis", end = '\n\n')
    print("You can verify your email now or do it later and proceed to use the app", end = '\n\n')
    verification_choice = questionary.confirm("Do you want to verify your email now?").ask()
    if verification_choice:
      is_email_verified = verify_email(user_session, engine)  # Function that user session, generates random number and verifies it. Provide two optins: I don't get an email - send one more/ proceed; I have a code, proceed with verification - enter number (if number is not correct  - ask user to enter again, no more than three times)
    else:
      is_email_verified = False
  else:
    is_email_verified = True
    questionary.text("To continue just press Enter").ask()
    
  # Entering Global Mode
  while global_mode:
    os.system("clear") 
    print("Global Management Mode", end='\n\n')         
    
    # Not entering Portfolio Management Mode without changing this falg on one of the steps
    porfolio_management_mode = False
        
    portfolios = get_portfolios(user_session, engine) # Function that returns a DF with portfolios (with the current balance and performance(percantage)) or empty DF if there are nothing in the portfolio. It gets user_id from the current user session (user_session)
    # Test Data: 
    #portfolios = pd.DataFrame()  # Case 1: No portfolios
    #portfolios = pd.DataFrame({'portfolio_id':[1,2], 'portfolio_name':['My Crypto Portfolio', 'My Stocks Portfolio'], 'portfolio_type': ['Crypto', 'Stocks'], 'portfolio_balance':[0, 10500.00], 'portfolio_performance_percentage':[0,-3.25], 'portfolio_performance_currency':[0,-500]})  # Case 2: List of portfolios
    
    print("----------------------------")
    print("The list of your portfolios:")
    print("----------------------------")
    
    if portfolios.empty: 
      print("No portfolios added")
      print("----------------------------") 
    else:
      #portfolios['choice_mode_name'] = [generate_detailed_portfolio_string(row[0], row[1], row[2], row[3]) for row in zip(portfolios['portfolio_name'], portfolios['portfolio_balance'], portfolios['portfolio_performance_percentage'], portfolios['portfolio_performance_currency'])]
      #for portfolio in portfolios['choice_mode_name']:
      for index, entry in portfolios.iterrows():
        portf = get_portfolio_info(entry, engine)[0]
        portf['detailed_info'] = generate_detailed_portfolio_string_short(portf['portfolio_name'], portf['current_balance'], portf['assets_count'])
        print(portf['detailed_info'])
        
      print("----------------------------")
      
    global_mode_choices = get_portfolio_mode_choices('Global',is_email_verified, portfolios.empty)
    
    global_mode_choice = questionary.select("", choices = global_mode_choices, use_shortcuts=True).ask()
    
    if global_mode_choice == "Add New Portfolio":
      portfolio = add_portfolio(user_session, engine)   #   Function that adds a portfolio (asks the name of the portfolio) and returns the portfolio Series. It gets user_id from the current user session (user_session)
      
      # Enter Portfolio Name
      # Pick portfolio type (table - portfolio_types)
      # Create records in the DB:portfolios, specify the right portfolio_type_id 
      # INSERT INTO portfolios ('portfolio_name', 'portfolio_type_id',....)
      
      if not isinstance(portfolio, bool):
        is_new_portfolio = True
        porfolio_management_mode = True
      #portfolio = pd.Series({'portfolio_id': 3, 'portfolio_name':'My New Portfolio', 'portfolio_type':'Crypto'})
      #porfolio_management_mode = True
      else: 
        porfolio_management_mode = False
        
    
    elif global_mode_choice == "Verify Email":
      is_email_verified = verify_email(user_session, engine)
      ### is_email_verified = verify_email(user_session)  # Function that gets email and verifies it
      
    
    elif global_mode_choice == "Manage Portfolio":
      #selected_portfolio =  portfolios[portfolios['choice_mode_name'] == questionary.select("Select a profile", portfolios['choice_mode_name'].to_list()).ask()].squeeze()  
      selected_portfolio =  portfolios[portfolios['portfolio_name'] == questionary.select("Select a profile", portfolios['portfolio_name'].to_list(), use_shortcuts=True).ask()].squeeze()
      porfolio_management_mode = True
      is_new_portfolio = False
    
    if global_mode_choice == 'Exit':
      sys.exit()
    
    # Entering Portflio Management Mode     
    while porfolio_management_mode:
      os.system("clear")
      
      if is_new_portfolio:
        portfolio_assets = pd.DataFrame()
      else:
        full_portfolio = get_portfolio_info(selected_portfolio, engine)   # Returns the tuple - (portfolio, assets). portfolio - Series (portfolio_id, portfolio_name, portfolio_balance, portfolio_performance)
          
        # Testing data
        #portfolio_assets = pd.DataFrame()  # Case 1: No assets in the portfolio
        #portfolio_assets = pd.DataFrame({'asset_id': [1], 'asset_code': ['XRP'], 'asset_name': ['Ripple XRP'], 'asset_holdings': [10000], 'asset_avg_buy_price': [0.8], 'asset_balance': [8351.45], 'asset_performance_percentage': [7.25], 'asset_performance_currency': [500.25]})
        #full_portfolio = (selected_portfolio, portfolio_assets)
        
        portfolio = full_portfolio[0]
        portfolio_assets = full_portfolio[1]
        

        #portfolio = pd.Series({'portfolio_id': 3, 'portfolio_name':'My New Portfolio', 'portfolio_type':'Crypto'})
        #porfolio_management_mode = True
      
      print("Portfolio Management Mode")
      print("-------------------------")
      print(f"Managing portfolio: {portfolio['portfolio_name']}")
      print("----------------------------")
      print("The list of the assets in the portfolio:")
      print("----------------------------")  
        
      if portfolio_assets.empty: 
        print("No assets in the portfolio")
        print("----------------------------") 
      else:

        portfolio_assets['choice_mode_name'] = [generate_detailed_asset_string(row[0],row[1],row[2],row[3],row[4],row[5], row[6]) for row in zip(portfolio_assets['asset_code'], portfolio_assets['asset_holdings'],  portfolio_assets['asset_avg_buy_price'], portfolio_assets['asset_total_profit_loss_currency'], portfolio_assets['asset_total_profit_loss_percentage'], portfolio_assets['asset_balance'], portfolio_assets['current_price'])]
        for asset in portfolio_assets['choice_mode_name']:
          print(asset)                                        
        print("----------------------------")
      
      portfolio_management_choice = questionary.select("", choices = get_portfolio_mode_choices('Portfolio',is_email_verified, portfolio_assets.empty), use_shortcuts=True).ask()
      
      if portfolio_management_choice == 'Add Existing Asset':
        # Here to show the list of assets to pick from
        # Remember user's choice
        selected_asset = portfolio_assets[portfolio_assets['asset_code'] == questionary.select("Select a profile", portfolio_assets['asset_code'].to_list(), use_shortcuts=True).ask()].squeeze()
        asset_transaction = add_transaction_existing_asset(portfolio, selected_asset, engine)
        ### add_transaction_existing_asset(portfolio, asset)
        # Ask user to enter: the type of transaction (buy/sell), amount, date, price
        # If sell - check we have the amount to sell for the date specified. For example: 01/01/2022 - buy 1000, 01/03/2022 - buy 1000, 1. trying to sell 3000 on 01/04/2022 - error. 2. Trying to sell 1500 on 01/02/2022 - error (on 01/02/2022 we had only 1000). We can calculate cumulative sums (with plus for buy and minus for sell) for the dates before specified sell-date
        # If transcation passed the validation create the record in asset_transactions and update the corresponding record in asets_in_portfolio (calculate new asset_holding, new avg_buy_price)

      if portfolio_management_choice == 'Show Detailed Portfolio Analysis':
        os.system("clear")
        print("Running Portfolio Analysis")
        ### run_portfolio_analysis(portfolio) 
        
      
      if portfolio_management_choice == 'Edit Portfolio':
        
        is_portfolio_changed = edit_portfolio_name(portfolio, engine)
        # Show the current name of the portfolio
        # Ask to enter new name 
        # Update the record in the DB for the right portfolio (passing it as an argument)

      
      if portfolio_management_choice == 'Remove Portfolio':
        is_portfolio_removed = remove_portfolio(portfolio, engine)  
        if is_portfolio_removed:
          porfolio_management_mode = False
          
        # Show the message that user is removing the portfolio
        # Asking to confirm to remove the portfolio 
        # Update the record in the DB for the right portfolio (passing it as an argument) - set is_remoed = True (we won't remove portfolios phisically)

      
      if portfolio_management_choice == 'Add New Asset':
        asset_transaction = add_transaction(portfolio, engine)   
        # Interacts with user to get the aset code
        # Check if there are no assets with the same code in the portfolio. If so, call function to add transaction for the existing asset (see anove - add_transaction_existing_asset), if no:
        # Checks the type of asset based on the portfolio_type to use the right API 
        # Requests the corresponding API based on the type and searches the info about this asset. 
        # If entered aset doesn't exist (error) - return False. If it exists: 
        # Continue the dialog with the user: ask amount, transaction date and price
        # Adds records to the DB assets_in_portfolio: asset_code = <asset code>, asset_name = <asset_name>, asset_holdings = <amount entered>, avg_buy_price = <price entered> (because that's a new aset), portfolio_id = <id of selected portfolio>
        # Add linked record to asset_transaction with asset_in_portfolio_id of just created record in assets_in_portfolio table
        
      if portfolio_management_choice == 'Go Back':
        porfolio_management_mode = False
      if portfolio_management_choice == "Exit":
        sys.exit()
          
      
      
if __name__ == "__main__":
  fire.Fire(run)
  
  
