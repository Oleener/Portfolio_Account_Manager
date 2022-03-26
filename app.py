import pandas as pd
import numpy as np
import sqlalchemy as sql
from sqlalchemy import inspect
import questionary 
import fire
import os
import sys
import dotenv
import dash


from utils.formatters import *
from utils.authentication import *
from financial.portfolio import *
from financial.assets import *
from financial.web_app import *

# Defining a PostgreSQL connection string
db_connection_string = "postgresql+psycopg2://airgsfjw:lf0yqypx53HpPomnz_l3LXJZXMMufFay@kashin.db.elephantsql.com/airgsfjw"

# Creating the engine for the connection
engine = sql.create_engine(db_connection_string)

# Running the main logic/flow of the app
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
    # If function returns boolean value (can return False only if user wasn't signed up successfully) then terminating the program
    if isinstance(sign_up_result, bool):
      sys.exit() 
    # If user was created successfully the function will return user's data that is used to create user's session
    else:
      user_session = sign_up_result
      global_mode = True
      os.system("clear")
      print(f"Hey {user_session['user_first_name']}! Your account has been successfully created.", end = '\n\n')
  
  # If user selects to Login
  elif login_mode_choice == 'Log in':
        # Running a login flow
    login_result = user_login(engine)  
    # If function returns boolean value (can return False only if user wasn't logged in successfully) then terminating the program
    if isinstance(login_result, bool):
      sys.exit() 
    # If user logged in successfully the function will return user's data that is used to create user's session
    else:
      user_session = login_result
      global_mode = True
      os.system("clear")
      print(f"Hey {user_session['user_first_name']}! You are successfully logged in.", end = '\n\n')
  
  # If user selects to Exit
  elif login_mode_choice == 'Exit':
    # Just terminating the program    
    print("Buy-buy! ")
    sys.exit()
  
  # After the successfull sign up or login - checking if user's email is verified
  # Uaer can verify email after logging in or in the global mode
  if user_session['is_email_verified'] == False: 
    print(f"Your email {user_session['user_email']} is not verified!", end = '\n\n')
    print("The following functionality won't be available for you:", end='\n\n')
    print("- Deep Portfolio Analysis", end = '\n\n')
    print("You can verify your email now or do it later and proceed to use the app", end = '\n\n')
    verification_choice = questionary.confirm("Do you want to verify your email now?").ask()
    if verification_choice:
      # Running the verification flow
      is_email_verified = verify_email(user_session, engine) 
    # User decided to verify the email later
    else:
      is_email_verified = False
  # User's email is already verified
  else:
    is_email_verified = True
    questionary.text("To continue just press Enter").ask()
    
  # Entering Global Mode
  while global_mode:
    os.system("clear") 
    # Not entering Portfolio Management Mode autamatically without changing this falg on one of Global Mode steps
    porfolio_management_mode = False
    # Requestion the list of user's portfolios from the DB   
    portfolios = get_portfolios(user_session, engine) 
    print("Global Management Mode\n" + 
          "----------------------------\n" +
          "The list of your portfolios:\n" + 
          "----------------------------")         
    
    # The case when there are no portgolios connected with user's profile
    if portfolios.empty: 
      print("No portfolios added\n" + 
            "----------------------------")
    # Case when at least one portfolio exists
    else:
      # Iterating through the list of available (not removed) portfolios
      for index, entry in portfolios.iterrows():
        # Getting the details portfolio info - portfolio and assets. get_portfolio_info return a tuple (portfolio, assets). We just need a portfolio info on this step
        portf = get_portfolio_info(entry, engine)[0]
        # Generating a string with the additional portfolio info to show to the user
        portf['detailed_info'] = generate_detailed_portfolio_string_short(portf['portfolio_name'], portf['current_balance'], portf['assets_count'])
        print(portf['detailed_info'])
        
      print("----------------------------")
    
    # Generating the list of available for the Global Mode options based on the flags - email verification and portfolio existence
    global_mode_choices = get_portfolio_mode_choices('Global',is_email_verified, portfolios.empty)
    
    # Asking user to pick one of the available options 
    global_mode_choice = questionary.select("", choices = global_mode_choices, use_shortcuts=True).ask()
    
    # Adding new portfolio flow
    if global_mode_choice == "Add New Portfolio":
      # Running a function to add a new portflio for the current user
      portfolio = add_portfolio(user_session, engine) 
      
      # Checking if portfolio is created sucessfully. If not, the function returns False, otherwise it returns new portfolio object (Series)
      if not isinstance(portfolio, bool):
        # That's a new portfolio, the flag will be used to skip getting assets step in Portfolio Management Mode
        is_new_portfolio = True
        # Can enter the Portfolio Management Mode
        porfolio_management_mode = True
      else: 
        # Will stay in the Global Mode
        porfolio_management_mode = False
        
    # If user selects to verify email in the Global Mode
    elif global_mode_choice == "Verify Email":
      # Running the email verification flow
      is_email_verified = verify_email(user_session, engine)
    
    # This option is available if at least one portfolio exists. It shows the list of the portfolios to selecty from and runs Portfolio Management Mode for the selected portfolio
    elif global_mode_choice == "Manage Portfolio":
      # It gets the names of user's portfolios and generates a list to pick from  
      selected_portfolio =  portfolios[portfolios['portfolio_name'] == questionary.select("Select a profile", portfolios['portfolio_name'].to_list(), use_shortcuts=True).ask()].squeeze()
      # Can enter the Portfolio Management Mode
      porfolio_management_mode = True
      # Not a new portfolio
      is_new_portfolio = False
    
    # Exit the program
    if global_mode_choice == 'Exit':
      sys.exit()
    
    # Entering Portflio Management Mode     
    while porfolio_management_mode:
      os.system("clear")
      asset_management_mode = False
      # Checking if the portfolio is new
      if is_new_portfolio:
        # Creating an empty DataFrame - new portfolio means no assets added
        portfolio_assets = pd.DataFrame()
      # Not a new portflio (was selected from the list using Manage Portfolio option) 
      else:
        # Getting full info about the portfolio. The function returns a tuple (portfolio, assets), where portfolio is a Series object, assets is a DataFrame.
        full_portfolio = get_portfolio_info(selected_portfolio, engine)   
        portfolio = full_portfolio[0]
        portfolio_assets = full_portfolio[1]
      
      print(f"Portfolio Management Mode\n" +
            "-------------------------\n" +
            f"Managing portfolio: {portfolio['portfolio_name']}\n" +
            "----------------------------\n" +
            "The list of the assets in the portfolio:\n" +
            "----------------------------")
     
      # Flow when there are no assets added  
      if portfolio_assets.empty: 
        print("No assets in the portfolio")
        print("----------------------------") 
      # At least one assets exists in the portfolio
      else:
        # Generating the list of assets with the detailed info (balance, performance, etc)
        portfolio_assets['choice_mode_name'] = [generate_detailed_asset_string(row[0],row[1],row[2],row[3],row[4],row[5], row[6]) for row in zip(portfolio_assets['asset_code'], portfolio_assets['asset_holdings'],  portfolio_assets['asset_avg_buy_price'], portfolio_assets['asset_total_profit_loss_currency'], portfolio_assets['asset_total_profit_loss_percentage'], portfolio_assets['asset_balance'], portfolio_assets['current_price'])]
        # Iterating throug the assets to print the list 
        for asset in portfolio_assets['choice_mode_name']:
          print(asset)                                        
        print("----------------------------")
      
      # Asking user to pick one of the available options based on the flags - email verification and assets existence
      portfolio_management_choice = questionary.select("", choices = get_portfolio_mode_choices('Portfolio',is_email_verified, portfolio_assets.empty), use_shortcuts=True).ask()
      
      # Managing one of the exising in portfolio assets to add new transaction (buy/sell). The option is not available if ther are no assets in the portfolio
      if portfolio_management_choice == 'Manage Existing Asset':
        # Getting the list of the asset codes and asks user to select on them to create a new transaction
        selected_asset = portfolio_assets[portfolio_assets['asset_code'] == questionary.select("Select a profile", portfolio_assets['asset_code'].to_list(), use_shortcuts=True).ask()].squeeze()
        # Running adding a new transaction flow for the selected asset
        asset_management_mode = True
        
 
      # Generates the web-page to show some porfolio-based statistics. This option is not available for user if user's email in unverified
      if portfolio_management_choice == 'Show Detailed Portfolio Analysis':
        # Getting prices history for the assets in the portfolio
        assets_history = get_assets_price_history(portfolio['portfolio_type'], portfolio_assets['asset_code'].to_list(), period_years=1)
        assets_history = assets_history.xs(key = 'close', level = 1, axis = 1)
        # Building layout. It returns an app with build-in HTML and visual components
        app = build_layout_portfolio(portfolio, assets_history)
        # Running a web-server based on the app object
        app.run_server()
         
      # User selects to edit the portfolio name
      if portfolio_management_choice == 'Edit Portfolio':
        # Running Edit Portfolio name flow
        is_portfolio_changed = edit_portfolio_name(portfolio, engine)

      # User selects to remove the portfolio. The portfolio will not be removed phisically from the DB
      if portfolio_management_choice == 'Remove Portfolio':
        is_portfolio_removed = remove_portfolio(portfolio, engine)  
        # If the porfolio removed successfully (changed is_removed flag) we can't be in the Portfolio Management Mode anymore
        if is_portfolio_removed:
          porfolio_management_mode = False
          
      # User selects to add new asset to the portfolio
      if portfolio_management_choice == 'Add New Asset':
        # Adding new 'buy' transaction for new asset
        asset_transaction = add_transaction(portfolio, engine)  
        # In case of the new portfolio, after adding the first asset right after adding the portfolio need to specify that the portfolio is not new anymore
        is_new_portfolio = False

      # Going back to the Global Mode to pick another portfolio or cretae a new one
      if portfolio_management_choice == 'Go Back':
        # Exiting the Portfolio Management Mode in this case
        porfolio_management_mode = False
        
      # Terminating the program 
      if portfolio_management_choice == "Exit":
        sys.exit()
      
      #Entering Asset Management Mode for the selected asset
      while asset_management_mode:
        os.system("clear")
        asset_mode_str = generate_asset_mode_string(selected_asset, portfolio)
        print(asset_mode_str) 

        
        asset_management_choice = questionary.select("", choices = ['Add transaction', 'Show asset analysis', 'Go Back', 'Exit'], use_shortcuts=True).ask()   

        if asset_management_choice == 'Add transaction':
          asset_transaction = add_transaction_existing_asset(portfolio, selected_asset, engine, asset_mode_str)
          asset_management_mode = False
        
        if asset_management_choice == 'Show asset analysis':  
          if is_email_verified:
            analysis_choice = questionary.select("", choices = ['Simple Mode', 'Professional Mode', 'Go Back'], use_shortcuts=True).ask()
          else:
            print("Professional Mode is not available for users with unverified emails. Please verify your email to unblock Professional Mode or use Simple Mode prediction")
            analysis_choice = questionary.select("", choices = ['Verify Email', 'Show Simple Mode prediction', 'Go Back'], use_shortcuts=True).ask()

          if analysis_choice == 'Go Back':
            pass
          
          if analysis_choice == 'Simple Mode' or analysis_choice == 'Show Simple Mode prediction':
            analisys = build_layout_asset(selected_asset['portfolio_type'], selected_asset['asset_code'])
            prediction = analisys[0]
            print("----------------------------")
            print(prediction)  
            questionary.text("To continue just press Enter").ask()
          else:
            fast, long, days_predict, predictors_selected, model_selected = get_asset_analysis_parameters()
            analisys = build_layout_asset(selected_asset['portfolio_type'], selected_asset['asset_code'], predictors_selected, model_selected, fast, long, days_predict)
            analisys[1].run_server()
            
          
        if asset_management_choice == 'Go Back':
        # Exiting the Asset Management Mode in this case
          asset_management_mode = False
        
        # Terminating the program 
        if asset_management_choice == "Exit":
          sys.exit()
        
        
        
# Running the app      
if __name__ == "__main__":
  fire.Fire(run)
  
  
