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

# Regular Expressions from the re library meant to specify a search pattern in text
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

# Function for validating user password using regexp from the re library
def validate_password(password):
  # If it matches that in the database, it returns True
  if(re.fullmatch(password_regex, password)):
    return True
  # If it doesn't match, False
  else:
    return False

# Function for validating user email using regexp from the re library
def validate_email(email):
   # If it matches that in the database, it returns True
   # pass the regular expression
   # and the string into the fullmatch() method
   if(re.fullmatch(email_regex, email)):
    return True
   else:
      # If it doesn't match, False
      return False

#Function to run the user login process
def user_login(engine):
  os.system("clear")
  print("Logging in:")
  
  
  is_email_registered = False
  while not is_email_registered:
    # User enters email to log in
    print("---------------------")
    user_email = questionary.text("Enter Your Email:").ask() 
    user_df = pd.read_sql_query(f"SELECT user_profiles.*, users.user_id, users.email, users.password FROM users JOIN user_profiles ON user_profiles.user_profile_id = users.user_profile_id WHERE email = '{user_email}'", con=engine).squeeze() 
    # If it's not in the database, they can re-enter it until is_email_registered becomes True
    if user_df.empty:
      print("\n  This email is not registered.\n") 
      try_again = questionary.confirm("Try to enter email again?").ask()
      # If they decide not to re-enter it, the function returns false
      if not try_again:
        return False
    # When the email addresses match, the user moves to entering their password
    else:
      is_email_registered = True
      os.system("clear")
      print("Logging in:")
      print("---------------------")
      print(f"Email: {user_email}")
  # For the password, the user is allowed three attempts
  attemtps_to_enter_password = 3
  while attemtps_to_enter_password > 0: 
    print("---------------------")
    user_password = questionary.password("Enter Your Password:").ask()
    # If passwords don't match, they re-enter it until they run out of attempts as it subtracts 1 each attempt from attemtps_to_enter_password
    if hashlib.md5(user_password.encode()).hexdigest() != user_df['password']:
      print("\n  Wrong password\n")
      attemtps_to_enter_password -= 1
    # If the password matches the database, the function returns the users account details to specify the active user
    else:
      return pd.Series({'user_id': user_df['user_id'], 'user_first_name': user_df['first_name'], 'user_last_name': user_df['last_name'], 'user_email': user_df['email'], 'is_email_verified': user_df['is_verified'], 'user_profile_id': user_df['user_profile_id']})
  # If attempts run out, the function returns False
  if attemtps_to_enter_password == 0:
    print("  You've reached the maximum number of attempts to enter the password. Please try again later (password restoring - TBD).\n")
    return False  
    

# Function for user signup (first, last names, email, password)
def user_signup(engine):
  # When the new user selects "Sign up", they are prompted to input their new account info
  os.system("clear")
  print("Creating New Account:")
  print("---------------------")
  print("First Name:")
  print("Last Name:")
  print("Email:")
  print("Password:")
  # Entering First Name
  # Variable below equals true initially because the database's slots for info on this new user are empty
  is_first_name_empty = True
  while is_first_name_empty:
    print("---------------------")
    user_first_name = questionary.text("Enter Your First Name:").ask()
    # If they typed nothing or just a space or more:
    if not user_first_name or user_first_name.isspace():
      print("\n  First Name can't be empty!\n")
      try_again = questionary.confirm("Try to enter first name again?").ask()
      # If they don't re-enter, function returns False
      if not try_again:
        return False
    # Once is_first_name_empty is False, that means a first name has been entered, and the user can now enter a last name
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
  # Variable below equals true initially because the database's slots for info on this new user are empty
  is_last_name_empty = True
  while is_last_name_empty:
    print("---------------------")
    user_last_name = questionary.text("Enter Your Last Name:").ask()
    # If they typed nothing or just a space or more:
    if not user_last_name or user_last_name.isspace():
      # this is told back to them, and they have the option to re-enter
      print("\n  Last Name can't be empty!\n")
      try_again = questionary.confirm("Try to enter last name again?").ask()
      # If they don't re-enter, function returns False
      if not try_again:
        return False
    # Once is_last_name_empty is False, that means a last name has been entered, and the user can now enter an email address
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
  # Variable below equals False initially because the database's slots for info on this new user are empty and aren't validated
  is_email_validated = False
  while not is_email_validated:
    print("---------------------")
    user_email = questionary.text("Enter Your Email:").ask()
    is_right_email = validate_email(user_email)
    # If they typed the wrong email (which at this point so far, all possiblities are wrong):
    if not is_right_email:
      # this is told back to them, and they have the option to re-enter
      print("\n  Invalid Email Format\n")
      try_again = questionary.confirm("Try to enter email again?").ask()
      # If they don't re-enter, function returns False
      if not try_again:
        return False
    # Once is_email_validated is True, that means an email address has been entered, and the user can now enter a password
    else:
      is_email_validated = True
      os.system("clear")
      print("Creating New Account:")
      print("---------------------")
      print(f"First Name: {user_first_name}")
      print(f"Last Name: {user_last_name}")
      print(f"Email: {user_email}")
      print("Password:")
  # Variable below equals False initially because the database's slots for info on this new user are empty and aren't validated
  is_password_validated = False
  while not is_password_validated:
    print("---------------------")
    user_password = questionary.password("Enter your password:").ask()
    is_right_password = validate_password(user_password)
    # If they typed the wrong password or did not follow passowrd criteria (which at this point so far, all possiblities are wrong):
    if not is_right_password:
      # this is told back to them, and they have the option to re-enter
      print("\n  Password should contain minimum eight characters, at least one letter, one number and one special character:\n")
      try_again = questionary.confirm("Try to enter password again?").ask()
      # If they don't re-enter, function returns False
      if not try_again:
        return False
    # Once an acceptable password has been entered, and the user can now confirm it by re-entering it
    else:
      print('')
      user_password_confirmation = questionary.password("Enter your password again to confirm it").ask()
      # If password re-entry matches the original, is_password_validated becomes True and it's set to enter the database:
      if user_password_confirmation == user_password:
        is_password_validated = True
        os.system("clear")
        print("Creating New Account:")
        print("---------------------")
        print(f"First Name: {user_first_name}")
        print(f"Last Name: {user_last_name}")
        print(f"Email: {user_email}")
        print("Password:********")
      # If password re-entry does not match the original, is_password_validated remains False
      else: 
        print("\n  Passwords don't match\n")
        try_again = questionary.confirm("Try to enter password again?").ask()
        # If they don't re-enter, function returns False
        if not try_again:
          return False
  print("---------------------")
  
  # The user is given the option to officailize their account and set the into into the database
  create_account = questionary.confirm('Would you like to continue and create your account?').ask()
  # If agreed to:
  if create_account:
    # The info gets put into the database with SQL queries, and the password specially gets hidden and encoded using the hash library
    try:
      insert_user_profile_query = f"INSERT INTO user_profiles(first_name, last_name, is_verified) VALUES ('{user_first_name}', '{user_last_name}', False) RETURNING user_profile_id"
      [user_profile_id] = engine.execute(insert_user_profile_query).fetchone()
      password_hash = hashlib.md5(user_password.encode()).hexdigest()
      created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      insert_user_query = f"INSERT INTO users (email, password, created_on, user_profile_id) VALUES ('{user_email}', '{password_hash}', '{created_on}', {user_profile_id}) RETURNING user_id"
      [user_id] = engine.execute(insert_user_query).fetchone()
      # User account details are then returned to specify the active user
      return pd.Series({'user_id': user_id, 'user_first_name': user_first_name, 'user_last_name': user_last_name, 'user_email': user_email, 'is_email_verified': False, 'user_profile_id': user_profile_id})
    except Exception:
      print("The following exception occurred during the registration process:")
      print(Exception.with_traceback())
      
# Function to verify the user's email address is a real one, and that it's their's
def verify_email(user_session, engine):
  def verify_email_db(user_profile_id, engine):
    engine.execute(f"UPDATE user_profiles SET is_verified = True WHERE user_profile_id = {user_profile_id}")
  # The user is given the option to verify their email address
  send_verification_code = True
  # While the user would like their email address verified:
  while send_verification_code:
    # Verification code is generated randomly and converted to a string
    verification_code = np.random.randint(100000,999999)
    verification_code = str(verification_code)
    
    # Using the smtp and email.message library, an email is sent to the user with the verification code
    msg = EmailMessage()
    msg["Subject"] = "Verification Email"
    msg["From"] = "Portfolio Account Manager"
    msg["To"] = {user_session['user_email']}
    msg.set_content(f"Your verification code to enter on the Portfolio Account Manager app: {verification_code}")
      
    # Using a Google server, the code is sent with the applictaion's Gmail account
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # Logs in
    server.login("noreply.portfoliomanager@gmail.com", "Fintech1")
    # Sends the prepared message
    server.send_message(msg)
    # Quits right after
    server.quit()

    # User is notified they were sent a message
    os.system("clear")
    print("-----------------------------------------------")
    print("You've been sent a verification code via email!")
    print("--------------------------------------")
    code_recieved = questionary.confirm("Did you recieve the verification code?").ask()
    # If they recieved it, they enter the verification code to the application
    if code_recieved:
      os.system('clear')
      print("--------------------------------------------------------------")
      entered_verification_code = questionary.text("To verify your email, please enter the verification code here: ").ask()
      # If it matched the randomly generated code, function returns True
      if verification_code == entered_verification_code:
        verify_email_db(user_session['user_profile_id'], engine)
        print("---------------------------")
        print("Your email is now verified!")
        print("----------------------------")
        questionary.text("To continue just press Enter").ask()
        return True
      # If it didn't match:
      else:
        # The user is given two additional tries
        tries = 2
        # While the tries remaining are more than 0:
        while tries > 0:
          print("-----------------------------------------------")
          print("The verification code you entered is incorrect.")
          print("----------------")
          entered_verification_code = questionary.text("Please re-enter: ").ask()
          # If it matched the randomly generated code, function returns True
          if verification_code == entered_verification_code:
            verify_email_db(user_session['user_profile_id'], engine)
            print("---------------------------")
            print("Your email is now verified!")
            print("---------------------------")
            questionary.text("To continue just press Enter").ask()
            return True
          # If it didn't match, they lose a try and is_email_verified is still False
          else:
              print("-----------------------------------------")
              print("Sorry, incorrect entry! Please try again.")  
          tries = tries - 1

        # If the code entered doesn't match the generated one, the user is asked if they would like a new code sent
        if tries == 0:
          print("--------------------------------------------")
          resend = questionary.confirm("Would you like to resend the verification code?").ask()
          # If they agree, they loop back to when it first gets sent
          if resend:
            print("------------------------------")
            print("Resending verification code...")
            print("------------------------------")
          # If they would not like a new code, they continue through the app without a verified email address
          else:
              questionary.text("To continue just press Enter").ask()
              return False
    # If code wasn't initially recieved, the user is asked if they would like a new code sent
    else:
      print("--------------------------------------------")
      resend = questionary.confirm("Would you like to resend the verification code?").ask()
      # The user is looped back to when it first gets sent
      if resend:
        print("------------------------------")
        print("Resending verification code...")
        print("------------------------------")
      # If they would not like a new code, they continue through the app without a verified email address
      else:
        return False
