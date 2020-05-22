import pandas as pd 
import numpy as np
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
from fbprophet.plot import add_changepoints_to_plot
from sklearn.metrics import mean_absolute_error

def print_df_spec(df):
    print(df.shape)
    print(df.nunique())
    print(df.info())
    print(df.dtypes.value_counts())

def check_missing_data(df):
    total_missing = df.isnull().sum()[df.isnull().sum() != 0]
    percent_missing = round((df.isnull().sum().sort_values()[df.isnull().sum() != 0] / len(df)) * 100, 4)
    #is a count
    print(pd.concat([total_missing, percent_missing], axis=1,  keys=['Missing Values','Missing Value %']))

def find_one_val_cols(df):
    for feature in df.columns:
        if (len(df[feature].unique()) == 1):
            print(feature)

def unique_products(df):
    unique_df = df[['CATEGORY', 'NAME']]
    unique_df = unique_df.drop_duplicates()
    print(unique_df.sort_values(by='CATEGORY').head())

def add_features(df, holidays):
    #turn date into accurate date time measure to find year nad month measurements
    #measure all columns by date and product id (ticket)
    df['Date'] = pd.to_datetime(df['DATE'])
    holidays['Date'] = pd.to_datetime(df['DATE'])
    holidays['is_holiday'] = 1
    df['Month'] = df['Date'].dt.month.astype(np.int64)
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df = df.merge(holidays, on = 'Date', how='left')
    df['is_holiday'] = df['is_holiday'].fillna(0)
    df = df.drop('Holiday Name', axis=1)
    months_per_season = [(df['Month'] == 1) | (df['Month'] == 2) | (df['Month'] == 12),
              (df['Month'] == 3) | (df['Month'] == 4) | (df['Month'] == 5),
             (df['Month'] == 6) | (df['Month'] == 7) | (df['Month'] == 8),
             (df['Month'] == 9) | (df['Month'] == 10) | (df['Month'] == 11)]
    seasons = ['summer', 'fall', 'winter', 'spring']
    df['season'] = np.select(months_per_season, seasons)
    return df

def edit_prices(df):
    #mark free as pay effectively being 0
    df.loc[df['PAYMENT'] == 'free', 'TOTAL_PRICESELL'] = 0.00000
    #mark free as incurring loss
    df.loc[df['PAYMENT'] == 'free', 'PROFIT'] = -1 * df[df['PAYMENT'] == 'free']['TOTAL_PRICEBUY']
    #could possibly edit for card payment? average processing cost is 1.75%
    df.loc[df['PAYMENT'] == 'magcard', 'PROFIT'] = .985 * df[df['PAYMENT'] == 'magcard']['TOTAL_PRICEBUY']
    #overall loss making products
    print(df[(df['UNIT_PRICE_MARGIN'] < 0)]['NAME'].unique())
    max_unit_priceby = df['UNIT_PRICEBUY'].max()
    #all products that have the highest price per unit
    print(df[df['UNIT_PRICEBUY'] == max_unit_priceby]['NAME'].unique())
    return df

def main():
    df = pd.read_csv(r'C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\datathon 3- Store\grocery_store_data_cleaned.csv')
    holidays = pd.read_csv(r'C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\datathon 3- Store\australian-holidays.csv')
    df = df.drop('Unnamed: 0', axis=1)
    print(df.head())
    print_df_spec(df)
    check_missing_data(df)
    find_one_val_cols(df)
    unique_products(df)
    new_df = add_features(df, holidays)
    new_df = edit_prices(new_df)
    new_df.to_csv(r'C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\datathon 3- Store\grocery_store_data_stage-1-cleaned.csv')

if __name__=="__main__":
    main()