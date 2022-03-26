from email.policy import default
from dash import Dash, dash_table
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd
from financial.ml_tools import *
from financial.technical_indicators import *

default_fast = 5
default_long = 15
default_days_shift = 7
default_model = 'KNeighborsClassifier'
default_predictors = ['SMA_ratio', 'MACD', 'RSI_ratio']

def build_layout_portfolio(portfolio: pd.Series, assets_in_porfolio: pd.DataFrame):
   
    
  app = Dash() 
  df_changes = assets_in_porfolio.pct_change().dropna()
  df_cumprod = (1 + df_changes).cumprod()
  fig1 = px.line(df_changes, title = "Daily Returns", labels = ['Date', 'Daily Return'])
  fig2 = px.line(df_cumprod, title = "Cumulative Product")
  app.layout = html.Div(children=[
    html.H2(children=f"Analisys for {portfolio['portfolio_name']} (Test Mode)"),

    
    dcc.Graph(
        id='changes',
        figure=fig1 
    ),
    
    dcc.Graph(
        id='cumprod',
        figure=fig2 
    )
    
  ])
  return app

def build_layout_asset(asset_type, asset, predictors = default_predictors, model = default_model, fast = default_fast, long = default_long, days_predict = default_days_shift):
  asset_hist_with_indicators, asset_hist_for_ML = prepare_asset_for_analysis(asset_type, asset, fast, long, days_predict)
  model, X_test, Y_test = train_model(asset_hist_for_ML, model, predictors)    
  pred, class_report = validate_model(model, X_test, Y_test)  
  pred['actual'] = asset_hist_for_ML['Target_Direction']
  pred['pct_change'] = asset_hist_for_ML['Target']
  last_day_prediction = predict_the_day(model,asset_hist_with_indicators,predictors)
  
  prediction_string = ""
  if last_day_prediction['prediction'] > 0.6:
    prediction_string = f"There is a good chance the price for {asset} will go up - opening long position on {last_day_prediction['Date']} with ${last_day_prediction['open']} as an open price will most likely make you a profit after {days_predict} days"
  elif last_day_prediction['prediction'] < 0.4:
    prediction_string = f"There is a good chance the price for {asset} will go down - opening short position on {last_day_prediction['Date']} with ${last_day_prediction['open']} as an open price will most likely make you a profit after {days_predict} days"
  else: 
    prediction_string = f"It's hard to define the direction of the price and recommend whether to buy or sell {asset} today to make some profit after {days_predict} days" 
  
  app = Dash()
  fig1 = px.line(asset_hist_with_indicators[['close', f'SMA_{fast}', f'SMA_{long}']], title = "Close and SMA", labels = ['Date', 'Price'])
  fig2 = px.line(asset_hist_with_indicators[['close', f'EMA_{fast}', f'EMA_{long}']], title = "Close and EMA", labels = ['Date', 'Price'])
  fig3 = px.line(asset_hist_with_indicators[[f'ADX_{fast}', f'ADX_{long}']], title = "Average Directional Index (ADX)", labels = ['Date', 'Value'])
  fig4 = px.line(asset_hist_with_indicators[['MACD']], title = "Moving Average Convergence Divergence (MACD)", labels = ['Date', 'Value'])
  fig5 = px.line(asset_hist_with_indicators[[f'RSI_{fast}', f'RSI_{long}']], title = "Relative Strength Index (RSI)", labels = ['Date', 'Value'])
  fig6 = px.line(asset_hist_with_indicators[[f'ROC_{fast}', f'ROC_{long}']], title = "Rate of Change (ROC)", labels = ['Date', 'Value'])
  app.layout = html.Div(children=[
    html.H2(children=f"Analisys for {asset} (Test Mode)"),
    
    html.H4(children=f"Recomendation:"),
    html.P(children=prediction_string),
    
    html.H4(children=f"Classification report:"),
    dash_table.DataTable(class_report[0:4].to_dict('records'), [{"name": i, "id": i} for i in class_report.columns]),
    
    html.H4(children=f"Last 15-day: predictions vs actual:"),
    dash_table.DataTable(pred.to_dict('records'), [{"name": i, "id": i} for i in pred.columns]),

    dcc.Graph(
        id='SMA',
        figure=fig1 
    ),
    
    dcc.Graph(
        id='EMA',
        figure=fig2 
    ),
    
    dcc.Graph(
        id='ADX',
        figure=fig3 
    ),
    
    dcc.Graph(
        id='MACD',
        figure=fig4 
    ),
    
    dcc.Graph(
        id='RSI',
        figure=fig5 
    ),
    
        dcc.Graph(
        id='ROC',
        figure=fig6 
    )
  ])
  
  
  return prediction_string, app