import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

#function for assigning data containers as variables
def build_layout(portfolio: pd.Series, assets_in_porfolio: pd.DataFrame):
   #activate Dash
  app = dash.Dash()
   # create DataFrames
  df_changes = assets_in_porfolio.pct_change().dropna()
  df_cumprod = (1 + df_changes).cumprod()
  # create the line graphs
  fig1 = px.line(df_changes, title = "Daily Returns", labels = ['Date', 'Daily Return'])
  fig2 = px.line(df_cumprod, title = "Cumulative Product")
  #style the web application
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

