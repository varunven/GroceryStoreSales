import pandas as pd 
import numpy as np
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
from fbprophet.plot import add_changepoints_to_plot
from sklearn.metrics import mean_absolute_error

def remove_high_correlation(df):
    correlated_features = set()
    correlation_matrix = df.drop('TOTAL_PRICESELL', axis=1).corr()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > .9:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)
    df = df.drop(correlated_features, axis=1)
    return df

def update_df(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month.astype(np.int64)
    df['TransYear'] = pd.DatetimeIndex(df['Date']).year
    df['Date'] = df['Date'].dt.date
    df = df.rename(columns={'Date':'ds', 'TOTAL_PRICESELL':'y'})
    return df

def forecast_graph(df, category):
    input1 = pd.DataFrame(df.groupby('ds').sum()).reset_index()
    new_prophet = Prophet()
    new_prophet.fit(input1)
    #for 93 future dates
    future = new_prophet.make_future_dataframe(periods=93)
    #predicts based on current time series model prediction
    forecast = new_prophet.predict(future)
    #plots the forecast
    fig1 = new_prophet.plot(forecast)
    ax = fig1.gca()
    fig2 = new_prophet.plot_components(forecast)
    ax2 = fig2.gca()
    ax.autoscale()
    ax2.autoscale()
    ax.set_title(category)
    plt.show()

def find_series(df, category):
    ts = df[df['CATEGORY']==category]
    ts = ts[['ds','y']]
    ts = pd.DataFrame(ts.groupby('ds').sum()).reset_index()
    #forecast_graph(ts) #graph for just banana
    train = ts[:1200]
    test = ts[1200:]
    new_prophet = Prophet()
    new_prophet.fit(train)
    future = new_prophet.make_future_dataframe(periods=100)
    forecast = new_prophet.predict(future)
    print('Item: ' + category)
    print('RMSE:', np.sqrt(mean_squared_error(test['y'], forecast['yhat'][-79:])))
    print('MAE:', mean_absolute_error(test['y'], forecast['yhat'][-79:]))

def main():
    df = pd.read_csv(r'C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\datathon 3- Store\grocery_store_data_stage-1-cleaned.csv')
    df = remove_high_correlation(df)
    #redoing because new file so just in case requires refreshing
    df = update_df(df)
    items = ['Apples', 'Potatoes', 'Bananas', 'Onions', 'Tomatoes']
    #graphs everything
    #forecast_graph(df, 'all')
    #graphs item by item for however many you want
    for x in items:
        find_series(df, x)
    
    

if __name__ == "__main__":
    main()