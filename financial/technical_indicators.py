
import pandas as pd
import numpy as np
#from assets import get_assets_price_history
from financial.assets import get_assets_price_history

# Wilder's Smoothing - places more weight on the recent events
def Wilder(data, periods):
    start = np.where(~np.isnan(data))[0][0] #Check if nans present in beginning
    Wilder = np.array([np.nan]*len(data))
    Wilder[start+periods-1] = data[start:(start+periods)].mean() #Simple Moving Average
    for i in range(start+periods,len(data)):
        Wilder[i] = (Wilder[i-1]*(periods-1) + data[i])/periods #Wilder Smoothing
    return(Wilder)

# Calcs Simple Moving Averages based on Close prices for fast and long windows
def calc_SMA(close, fast, long):
    df = pd.DataFrame(index=close.index)
    fast_sma = f"SMA_{fast}"
    long_sma = f"SMA_{long}"
    df[fast_sma] = close.transform(lambda x: x.rolling(window = fast).mean())
    df[long_sma] = close.transform(lambda x: x.rolling(window = long).mean())
    df['SMA_ratio'] = df[fast_sma] / df[long_sma]
    return df

# Calcs Simple Moving Averages based on Volumes for fast and long windows
def calc_SMA_volume(volume, fast, long):
    df = pd.DataFrame(index=volume.index)
    fast_sma_volume = f"SMA{fast}_Volume"
    long_sma_volume = f"SMA{long}_Volume"
    df[fast_sma_volume] = volume.transform(lambda x: x.rolling(window = fast).mean())
    df[long_sma_volume] = volume.transform(lambda x: x.rolling(window = long).mean())
    df['SMA_Volume_ratio'] = df[fast_sma_volume] / df[long_sma_volume]
    return df

# Calcs Exp Moving Averages based on Volumes for fast and long windows
def calc_EMA(close, fast, long):
    df = pd.DataFrame(index=close.index)
    fast_ema = f"EMA_{fast}"
    long_ema = f"EMA_{long}"
    df[fast_ema] = close.ewm(span = fast, min_periods = fast - 1).mean()
    df[long_ema] = close.ewm(span = long, min_periods = long - 1).mean()
    df['EMA_ratio'] = df[fast_ema] / df[long_ema]
    return df

# Shifts values by 1 to define previous values in values_df for passed column_names
def calc_prev_values(column_names, values_df):
    df = pd.DataFrame(index=values_df.index)
    for col in column_names:
        col_name = f"prev_{col}"
        df[col_name] = values_df[col].shift(1)
    return df

# Calcs Average True Range (ATR) index for fast and long rolling windows
def calc_ATR(prev_close, high, low, fast, long):
    df = pd.DataFrame(index=high.index)
    fast_atr = f"ATR_{fast}"
    long_atr = f"ATR_{long}" 
    df['TR'] = np.maximum((high - low), 
                     np.maximum(abs(high - prev_close), 
                     abs(prev_close - low)))
    df[fast_atr] = Wilder(df['TR'], fast)
    df[long_atr] = Wilder(df['TR'], long)
    df['ATR_ratio'] = df[fast_atr] / df[long_atr]
    return df

# Calcs Average Directional Index (ADX) for fast and long rolling windows
def calc_ADX(high, prev_high, low, prev_low, prev_close, fast, long):
    df = pd.DataFrame(index=high.index)
    df['+DM'] = np.where(~np.isnan(prev_high), 
                         np.where((high > prev_high) & (((high - prev_high) > (prev_low - low))), 
                                  high - prev_high, 0),np.nan)
    df['-DM'] = np.where(~np.isnan(prev_low),
                         np.where((prev_low > low) & (((prev_low - low) > (high - prev_high))), 
                                  prev_low - low, 0),np.nan)

    df['+DM_fast'] = Wilder(df['+DM'], fast)
    df['+DM_long'] = Wilder(df['+DM'], long)
    df['-DM_fast'] = Wilder(df['-DM'], fast)
    df['-DM_long'] = Wilder(df['-DM'], long)
    
    plus_DI_fast = f"+DI_{fast}"
    minus_DI_fast = f"-DI_{fast}"
    plus_DI_long = f"+DI_{long}" 
    minus_DI_long = f"-DI_{long}"
    fast_atr = f"ATR_{fast}"
    long_atr = f"ATR_{long}" 
    atr = pd.DataFrame(calc_ATR(prev_close, high, low, fast, long))

    df[plus_DI_fast] = (df['+DM_fast']/atr[fast_atr])*100
    df[minus_DI_fast] = (df['-DM_fast']/atr[fast_atr])*100
    df[plus_DI_long] = (df['+DM_long']/atr[long_atr])*100
    df[minus_DI_long] = (df['-DM_long']/atr[long_atr])*100
    
    DX_fast = f"DX_{fast}"
    DX_long = f"DX_{long}"
    df[DX_fast] = (np.round(abs(df[plus_DI_fast] - df[minus_DI_fast])/(df[plus_DI_fast] + df[minus_DI_fast]) * 100))
    df[DX_long] = (np.round(abs(df[plus_DI_long] - df[minus_DI_long])/(df[plus_DI_long] + df[minus_DI_long]) * 100))
    
    ADX_fast = f"ADX_{fast}"
    ADX_long = f"ADX_{long}"
    df[ADX_fast] = Wilder(df[DX_fast], fast)
    df[ADX_long] = Wilder(df[DX_long], long)
    
    return df

# Function to calculate long and short RSI
def calc_RSI(close, fast, long):
    df = pd.DataFrame(index=close.index)
    df['Diff'] = close.transform(lambda x: x.diff())
    df['Up'] = df['Diff']
    df.loc[(df['Up'] < 0), 'Up'] = 0

    df['Down'] = df['Diff']
    df.loc[(df['Down']>0), 'Down'] = 0 
    df['Down'] = abs(df['Down'])

    df['avg_fast_up'] = df['Up'].transform(lambda x: x.rolling(window=fast).mean())
    df['avg_fast_down'] = df['Down'].transform(lambda x: x.rolling(window=fast).mean())

    df['avg_long_up'] = df['Up'].transform(lambda x: x.rolling(window=long).mean())
    df['avg_long_down'] = df['Down'].transform(lambda x: x.rolling(window=long).mean())

    df['RS_fast'] = df['avg_fast_up'] / df['avg_fast_down']
    df['RS_long'] = df['avg_long_up'] / df['avg_long_down']

    rsi_fast = f"RSI_{fast}"
    rsi_long = f"RSI_{long}"
    df[rsi_fast] = 100 - (100/(1+df['RS_fast']))
    df[rsi_long] = 100 - (100/(1+df['RS_long']))

    df['RSI_ratio'] = df[rsi_fast]/df[rsi_long]
    
    return df[[rsi_fast, rsi_long, 'RSI_ratio']]

# Function to calculate macd indicator
def calc_MACD(close, fast, long):
    df = pd.DataFrame(index=close.index)
    
    df['fast_Ewm'] = close.transform(lambda x: x.ewm(span=fast, adjust=False).mean())
    df['long_Ewm'] = close.transform(lambda x: x.ewm(span=long, adjust=False).mean())
    df['MACD'] = df['fast_Ewm'] - df['long_Ewm']
    return df

#Calcs Rate of Change (ROC) indicators for fast and long rolling windows
def calc_ROC(close, fast, long):
    df = pd.DataFrame(index=close.index)
    roc_fast = f"ROC_{fast}"
    roc_long = f"ROC_{long}"
    df[roc_fast] = close.diff(fast)/close.shift(fast)
    df[roc_long] = close.diff(long)/close.shift(long)
    df['ROC_ratio'] = df[roc_fast] / df[roc_long]
    return df

#Calcs Target (return) and the Target Direction based on the close price shifted by N days
def targets_Xdays_shift(open, close, days):
    df = pd.DataFrame(index=close.index)
    df['Close_Shifted'] = close.transform(lambda x: x.shift(-(days-1)))
    df['Target'] = (((df['Close_Shifted'] - open)/open) * 100).shift(-1)
    df['Target_Direction'] = np.where(df['Target'] > 0, 1, 0) 
    return df

#Function call calculation of all available technical indicators and combines them with the current history DF 
def calc_tech_indicators(prices_df, fast, long):   
    prev_values_columns = ['close', 'high', 'low']
    prices_df = pd.concat([prices_df, calc_prev_values(prev_values_columns, prices_df[prev_values_columns])], axis=1)
    
    prices_df = pd.concat([ prices_df, 
                          calc_SMA(prices_df['close'], fast, long), 
                          calc_EMA(prices_df['close'], fast, long),
                          calc_ATR(prices_df['prev_close'],prices_df['high'], prices_df['low'], fast, long)[[f"ATR_{fast}", f"ATR_{long}", "ATR_ratio"]],
                          calc_ADX(prices_df['high'], prices_df['prev_high'], prices_df['low'], prices_df['prev_low'], prices_df['prev_close'], fast, long)[[f"ADX_{fast}", f"ADX_{long}", f'+DI_{fast}', f'-DI_{fast}', f'+DI_{long}', f'-DI_{long}']],
                          calc_RSI(prices_df['close'], fast, long)[[f"RSI_{fast}", f"RSI_{long}", "RSI_ratio"]],
                          calc_MACD(prices_df['close'], fast, long)["MACD"],
                          calc_ROC(prices_df['close'], fast, long)[[f"ROC_{fast}", f"ROC_{long}", 'ROC_ratio']]
                          ], axis = 1)
    return prices_df

#Function to prepare an asset for further analysis - getting the history data, calculating technical indicators and tergets.
#Function returns two data frames: 1. prices and technical indicators 2. data frame for ML with technical indicators and targets
def prepare_asset_for_analysis(asset_type, asset, fast_roll_wnd, long_roll_wnd, days_predicted):
    prices_df = pd.DataFrame(get_assets_price_history(asset_type, [asset], period_years=3), dtype='float64')
    prices_df = prices_df.xs(key=slice(None), axis=1, level=0)
    prices_df.index = pd.to_datetime(prices_df.index)
    prices_df.sort_index(ascending=True, inplace=True)
    
    df_with_indicators = calc_tech_indicators(prices_df, fast_roll_wnd, long_roll_wnd)
    
    df_for_model_training = pd.concat([df_with_indicators, targets_Xdays_shift(prices_df['open'], prices_df['close'], days_predicted)], axis=1)
    df_for_model_training = df_for_model_training.dropna().copy()
    return df_with_indicators, df_for_model_training


#asset_hist_with_indicators, asset_hist_for_ML = prepare_asset_for_analysis('Crypto', 'XRP', 5, 15, 7)
#print(asset_hist_with_indicators[['ROC_5','ROC_15']])
