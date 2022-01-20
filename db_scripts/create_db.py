import pandas as pd
import sqlalchemy as sql
from sqlalchemy import inspect


db_connection_string = "postgresql+psycopg2://airgsfjw:lf0yqypx53HpPomnz_l3LXJZXMMufFay@kashin.db.elephantsql.com/airgsfjw"

engine = sql.create_engine(db_connection_string)

create_user_profiles_query = """
CREATE TABLE user_profiles (
	user_profile_id serial PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	is_verified bool NOT NULL
);
"""
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

create_portfolio_types_query = """
CREATE TABLE portfolio_types (
  portfolio_type_id serial PRIMARY KEY,
  portfolio_type VARCHAR(10) NOT NULL UNIQUE,
  is_supported bool NOT NULL
);
"""
insert_portfolio_types_query = """
INSERT INTO portfolio_types(portfolio_type, is_supported) VALUES ('stocks', true);
"""

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

create_assets_transactions_query = """
CREATE TYPE transaction_types AS ENUM ('But', 'Sell');

CREATE TABLE asset_transactions (
  asset_transaction_id serial PRIMARY KEY,
  transaction_amount float8 NOT NULL,
  transaction_price float8 NOT NULL,
  tranaction_type transaction_types NOT NULL,
  asset_in_portfolio_id int NOT NULL,
  FOREIGN KEY (asset_in_portfolio_id) REFERENCES assets_in_portdolio (asset_in_portfolio_id)
);
"""

engine.execute(create_assets_transactions_query)

print(inspect(engine).get_table_names())

print(pd.read_sql_query("SELECT * from portfolio_types", con=engine))
#print(pd.read_sql_query("DROP TABLE portfolios", con=engine))