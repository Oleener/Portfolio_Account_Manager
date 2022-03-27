import numpy as np
import pandas as pd
from scipy.stats import mstats
from pandas.tseries.offsets import DateOffset
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import RandomizedSearchCV, validation_curve, TimeSeriesSplit, GridSearchCV
from datetime import date

#from technical_indicators import prepare_asset_for_analysis
from financial.technical_indicators import prepare_asset_for_analysis

# Function to train a machine learning model
def train_model(data:pd.DataFrame, model,target_variables):
    training_begin = data.index.min()
    training_end = training_begin + DateOffset(months=24)
    train_data = data.loc[training_begin:training_end]
    test_data = data.loc[training_end:]
    X_train = train_data.loc[:,target_variables]
    Y_train = train_data.loc[:,['Target_Direction']]
    X_test = test_data.loc[:,target_variables]
    Y_test = test_data.loc[:,['Target_Direction']]
    if model == 'RandomForestClassifier':
        params = {'max_depth': [1, 3, 5, 7, 9],
                  'max_features': ['sqrt'],
                  'min_samples_leaf': [20,22,24,26,28,30],
                  'n_estimators': [3,5,7,9],
                  'min_samples_split':[15, 20, 25, 30, 35]}
        model_cv = GridSearchCV(RandomForestClassifier(), params, cv = TimeSeriesSplit(n_splits = 3), n_jobs = -1)
        model = model_cv.fit(X_train,Y_train.to_numpy().ravel()).best_estimator_
    if model == 'KNeighborsClassifier':
        parameter_range = np.arange(1, 10, 1)
        params = {'n_neighbors': parameter_range}
        model_cv = GridSearchCV(KNeighborsClassifier(), params, cv = TimeSeriesSplit(n_splits = 3), n_jobs = -1)
        model = model_cv.fit(X_train,Y_train.to_numpy().ravel()).best_estimator_
    return model, X_test, Y_test

# Function to create a prediction from the model trained in the above function
def validate_model(model, X_test, Y_test):
    Y_pred = model.predict(X_test)
    report = pd.DataFrame(classification_report(Y_test, Y_pred, output_dict=True)).transpose().reset_index()
    report.columns = ['', 'precision', 'recall', 'f1-score', 'support']
    last_data = X_test.iloc[-15:]
    pred = pd.DataFrame({'Date': last_data.index,'prediction':model.predict_proba(last_data)[:,1], 'pred_class': model.predict(last_data)})
    pred.index = pred['Date']
    pred.drop(columns=['Date'], inplace=True)
    return pred, report

# Function that gives a prediction based on the day
def predict_the_day(model, data, target_variables):
    day_data = data[target_variables][-1:]
    #print(day_data)
    pred = pd.Series({'Date': day_data.index.to_pydatetime()[0].date(), 'prediction': model.predict_proba(day_data)[0][1], 'pred_class': model.predict(day_data)[0], 'open': data['open'][-1]})
    return pred


#asset_hist_with_indicators, asset_hist_for_ML = prepare_asset_for_analysis('Stocks', 'AAPL', 3, 15, 5)
#model, X_test, Y_test = train_model(asset_hist_for_ML, 'KNeighborsClassifier', ['SMA_ratio', 'EMA_ratio', 'ATR_ratio', 'MACD', 'RSI_ratio'])

#pred, class_report = validate_model(model, X_test, Y_test)
#pred['actual'] = asset_hist_for_ML['Target_Direction']
#pred['pct_change'] = asset_hist_for_ML['Target']


#last_day_prediction = predict_the_day(model,asset_hist_with_indicators, ['SMA_ratio', 'EMA_ratio', 'ATR_ratio', 'MACD', 'RSI_ratio'])
#print(last_day_prediction)

#print(class_report)

#print(pred)

