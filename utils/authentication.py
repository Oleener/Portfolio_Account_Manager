import questionary
import sqlalchemy as sql
import re  # Regexp for validating email and password
import os
from datetime import datetime
import hashlib
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

def validate_password(password):
  if(re.fullmatch(password_regex, password)):
    return True
  else:
    return False

def validate_email(email):
   
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False

def user_login(engine):
  os.system("clear")
  print("Logging in:")
  
  
  is_email_registered = False
  while not is_email_registered:
    print("---------------------")
    user_email = questionary.text("Enter Your Email:").ask() 
    user_df = pd.read_sql_query(f"SELECT user_profiles.*, users.user_id, users.email, users.password FROM users JOIN user_profiles ON user_profiles.user_profile_id = users.user_profile_id WHERE email = '{user_email}'", con=engine).squeeze() 
    if user_df.empty:
      print("\n  This email is not registered.\n") 
      try_again = questionary.confirm("Try to enter email again?").ask()
      if not try_again:
        return False
    else:
      is_email_registered = True
      os.system("clear")
      print("Logging in:")
      print("---------------------")
      print(f"Email: {user_email}")
  attemtps_to_enter_password = 3
  while attemtps_to_enter_password > 0: 
    print("---------------------")
    user_password = questionary.password("Enter Your Password:").ask()
    if hashlib.md5(user_password.encode()).hexdigest() != user_df['password']:
      print("\n  Wrong password\n")
      attemtps_to_enter_password -= 1
    else:
      return pd.Series({'user_id': user_df['user_id'], 'user_first_name': user_df['first_name'], 'user_last_name': user_df['last_name'], 'user_email': user_df['email'], 'is_email_verified': user_df['is_verified'], 'user_profile_id': user_df['user_profile_id']})
  if attemtps_to_enter_password == 0:
    print("  You've reached the maximum number of attempts to enter the password. Please try again later (password restoring - TBD).\n")
    return False  
    

def user_signup(engine):
  os.system("clear")
  print("Creating New Account:")
  print("---------------------")
  print("First Name:")
  print("Last Name:")
  print("Email:")
  print("Password:")
  # Entering First Name
  is_first_name_empty = True
  while is_first_name_empty:
    print("---------------------")
    user_first_name = questionary.text("Enter Your First Name:").ask()
    if not user_first_name or user_first_name.isspace():
      print("\n  First Name can't be empty!\n")
      try_again = questionary.confirm("Try to enter first name again?").ask()
      if not try_again:
        return False
    else:
      is_first_name_empty = False
      os.system("clear")
      print("Creating New Account:")
      print("---------------------")
      print(f"First Name: {user_first_name}")
      print("Last Name:")
      print("Email:")
      print("Password:")
  # Entering Last Name
  is_last_name_empty = True
  while is_last_name_empty:
    print("---------------------")
    user_last_name = questionary.text("Enter Your Last Name:").ask()
    if not user_last_name or user_last_name.isspace():
      print("\n  Last Name can't be empty!\n")
      try_again = questionary.confirm("Try to enter last name again?").ask()
      if not try_again:
        return False
    else:
      is_last_name_empty = False
      os.system("clear")
      print("Creating New Account:")
      print("---------------------")
      print(f"First Name: {user_first_name}")
      print(f"Last Name: {user_last_name}")
      print("Email:")
      print("Password:")
  # Entering Email
  is_email_validated = False
  while not is_email_validated:
    print("---------------------")
    user_email = questionary.text("Enter Your Email:").ask()
    is_right_email = validate_email(user_email)
    if not is_right_email:
      print("\n  Invalid Email Format\n")
      try_again = questionary.confirm("Try to enter email again?").ask()
      if not try_again:
        return False
    else:
      is_email_validated = True
      os.system("clear")
      print("Creating New Account:")
      print("---------------------")
      print(f"First Name: {user_first_name}")
      print(f"Last Name: {user_last_name}")
      print(f"Email: {user_email}")
      print("Password:")
  is_password_validated = False
  while not is_password_validated:
    print("---------------------")
    user_password = questionary.password("Enter your password:").ask()
    is_right_password = validate_password(user_password)
    if not is_right_password:
      print("\n  Password should contain minimum eight characters, at least one letter, one number and one special character:\n")
      try_again = questionary.confirm("Try to enter password again?").ask()
      if not try_again:
        return False
    else:
      print('')
      user_password_confirmation = questionary.password("Enter your password again to confirm it").ask()
      if user_password_confirmation == user_password:
        is_password_validated = True
        os.system("clear")
        print("Creating New Account:")
        print("---------------------")
        print(f"First Name: {user_first_name}")
        print(f"Last Name: {user_last_name}")
        print(f"Email: {user_email}")
        print("Password:********")
      else: 
        print("\n  Passwords don't match\n")
        try_again = questionary.confirm("Try to enter password again?").ask()
        if not try_again:
          return False
  print("---------------------")
  
  create_account = questionary.confirm('Would you like to continue and create your account?').ask()
  if create_account:
    try:
      insert_user_profile_query = f"INSERT INTO user_profiles(first_name, last_name, is_verified) VALUES ('{user_first_name}', '{user_last_name}', False) RETURNING user_profile_id"
      [user_profile_id] = engine.execute(insert_user_profile_query).fetchone()
      password_hash = hashlib.md5(user_password.encode()).hexdigest()
      created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      insert_user_query = f"INSERT INTO users (email, password, created_on, user_profile_id) VALUES ('{user_email}', '{password_hash}', '{created_on}', {user_profile_id}) RETURNING user_id"
      [user_id] = engine.execute(insert_user_query).fetchone()
      return pd.Series({'user_id': user_id, 'user_first_name': user_first_name, 'user_last_name': user_last_name, 'user_email': user_email, 'is_email_verified': False, 'user_profile_id': user_profile_id})
    except Exception:
      print("The following exception occurred during the registration process:")
      print(Exception.with_traceback())
      
# Function that user session, generates random number and verifies it. Provides two opti0ns: I don't get an email - send one more/proceed; I have a code, proceed with verification - enter number (if number is not correct  - ask user to enter again, no more than three times)
def verify_email(user_session, engine):
  def verify_email_db(user_profile_id, engine):
    engine.execute(f"UPDATE user_profiles SET is_verified = True WHERE user_profile_id = {user_profile_id}")
  send_verification_code = True
  while send_verification_code:
    verification_code = np.random.randint(100000,999999)
    verification_code = str(verification_code)
    msg = EmailMessage()
    msg["Subject"] = "Verification Email"
    msg["From"] = "Portfolio Account Manager"
    msg["To"] = {user_session['user_email']}
    msg.set_content(f"Your verification code to enter on the Portfolio Account Manager app: {verification_code}")
      
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("noreply.portfoliomanager@gmail.com", "Fintech1")
    server.send_message(msg)
    server.quit()

    os.system("clear")
    print("-----------------------------------------------")
    print("You've been sent a verification code via email!")
    print("--------------------------------------")
    code_recieved = questionary.confirm("Did you recieve the verification code?").ask()
    if code_recieved:
      os.system('clear')
      print("--------------------------------------------------------------")
      entered_verification_code = questionary.text("To verify your email, please enter the verification code here: ").ask()
      if verification_code == entered_verification_code:
        verify_email_db(user_session['user_profile_id'], engine)
        print("---------------------------")
        print("Your email is now verified!")
        print("----------------------------")
        questionary.text("To continue just press Enter").ask()
        return True
      else:
        tries = 2
        while tries > 0:
          print("-----------------------------------------------")
          print("The verification code you entered is incorrect.")
          print("----------------")
          entered_verification_code = questionary.text("Please re-enter: ").ask()
          if verification_code == entered_verification_code:
            verify_email_db(user_session['user_profile_id'], engine)
            print("---------------------------")
            print("Your email is now verified!")
            print("---------------------------")
            questionary.text("To continue just press Enter").ask()
            return True
          else:
              print("-----------------------------------------")
              print("Sorry, incorrect entry! Please try again.")  
          tries = tries - 1

        if tries == 0:
          print("--------------------------------------------")
          resend = questionary.confirm("Would you like to resend the verification code?").ask()
          if resend:
            print("------------------------------")
            print("Resending verification code...")
            print("------------------------------")
          else:
              questionary.text("To continue just press Enter").ask()
              return False
    else:
      print("--------------------------------------------")
      resend = questionary.confirm("Would you like to resend the verification code?").ask()
      if resend:
        print("------------------------------")
        print("Resending verification code...")
        print("------------------------------")
      else:
        return False
