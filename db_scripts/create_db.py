import pandas as pd
import sqlalchemy as sql
from sqlalchemy import inspect

# Defining a PostgreSQL connection string
db_connection_string = "postgresql+psycopg2://airgsfjw:lf0yqypx53HpPomnz_l3LXJZXMMufFay@kashin.db.elephantsql.com/airgsfjw"

# Creating the Engine function connecting to the database connection string
engine = sql.create_engine(db_connection_string)

# Create_user_profiles_query creates a user_profiles table. The table contains columns which stores user_profile_id, first_name, & last_name.
create_user_profiles_query = """
CREATE TABLE user_profiles (
	user_profile_id serial PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	is_verified bool NOT NULL
);
"""

# creae_users_query creates a table that stores the users information. This table containes columns which are user_id, users email, password, created on timestamp, last login timestamp, & users_profile_id
# A foreign key is generated for user_profile_id referencing the users_profile table.
create_users_query = """
CREATE TABLE users (
  user_id serial PRIMARY KEY,
  email VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  created_on TIMESTAMP NOT NULL,
  last_login TIMESTAMP,
  user_profile_id int NOT NULL,
  FOREIGN KEY (user_profile_id) REFERENCES user_profiles (user_profile_id)
);
"""

# portfolio_types_query is creating a table which stores the portfolio types, this table containes two columns one with the portfolio_id and the other is the portfolio_type.
create_portfolio_types_query = """
CREATE TABLE portfolio_types (
  portfolio_type_id serial PRIMARY KEY,
  portfolio_type VARCHAR(10) NOT NULL UNIQUE,
  is_supported bool NOT NULL
);
"""

# insert_portfolio_types_query generates the different types of portfolios. 
insert_portfolio_types_query = """
INSERT INTO portfolio_types(portfolio_type, is_supported) VALUES ('stocks', true);
"""

# create_portfolios_query creates a portfolios table that stores the portfolio_id, portfolio_name, created_on timestamp, last_modified_on timestamp, is_removed, user_id, and portfolio_types. 
# A foreign key is generated for every user_id referencing the users table & portfolio_type_id referencing portfolio_types table. 
create_portfolios_query = """
CREATE TABLE portfolios (
  portfolio_id serial PRIMARY KEY,
  portfolio_name VARCHAR(50) NOT NULL,
  created_on TIMESTAMP NOT NULL,
  last_modified_on TIMESTAMP,
  is_removed bool NOT NULL,
  user_id int NOT NULL,
  portfolio_type_id int NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (user_id),
  FOREIGN KEY (portfolio_type_id) REFERENCES portfolio_types (portfolio_type_id)
);
"""

# create_assets_in_portfolio_query creates a table which stores the assets in portfolio. This table stores assets_in_portfolio_id, asset_code, asset_name, asset_holdings, asset_avg_buy_price & portfolio_id.
# A foreign key is generated for portfolio_id referencing portfolios table. 
create_assets_in_portfolio_query = """
CREATE TABLE assets_in_portdolio (
  asset_in_portfolio_id serial PRIMARY KEY,
  asset_code VARCHAR(10) NOT NULL,
  asset_name VARCHAR(50) NOT NULL,
  asset_holdings float8 NOT NULL,
  asset_avg_buy_price float4 NOT NULL,
  portfolio_id int NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id)
);
"""

# create_assets_transaction_query creates the two different transaction types, buy & sell. 
create_assets_transactions_query = """
CREATE TYPE transaction_types AS ENUM ('But', 'Sell');

# create_assets_transaction_query creates a table which stores asset_transactions. This table stores the asset_transaction_id, transaction_amount, transaction_price, transaction_type, & asset_in_portfolio_id.
# A foreign key is generated asset_in_portfolio_id referencing assets_in_portfolio table. 
CREATE TABLE asset_transactions (
  asset_transaction_id serial PRIMARY KEY,
  transaction_amount float8 NOT NULL,
  transaction_price float8 NOT NULL,
  tranaction_type transaction_types NOT NULL,
  asset_in_portfolio_id int NOT NULL,
  FOREIGN KEY (asset_in_portfolio_id) REFERENCES assets_in_portdolio (asset_in_portfolio_id)
);
"""

# Using the engine function to execute the create_assets_transaction_query 
engine.execute(create_assets_transactions_query)

# Print the table names from query 
print(inspect(engine).get_table_names())

# print panadas to read sql query by selecting all information from portfolio_types
print(pd.read_sql_query("SELECT * from portfolio_types", con=engine))

#print(pd.read_sql_query("DROP TABLE portfolios", con=engine))
