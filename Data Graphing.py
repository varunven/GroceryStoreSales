import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
#data by product, season, 

def product_total_sales_bar_graph(df):
    df = df.groupby('NAME').agg('sum', axis='columns').reset_index()
    df = df.filter(['NAME', 'PROFIT'])
    df = df.sort_values('PROFIT', ascending=False)
    df = df.head(20)
    ax = sns.barplot(x='NAME', y='PROFIT', data=df)
    plt.title("Top 20 Product's Total Profit over Time")
    plt.ylabel("Profit (AUD)")
    plt.xlabel("Product")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def product_least_total_sales_bar_graph(df):
    df = df.groupby('NAME').agg('sum', axis='columns').reset_index()
    df = df.filter(['NAME', 'PROFIT'])
    df = df.sort_values('PROFIT')
    df = df.head(10)
    ax = sns.barplot(x='NAME', y='PROFIT', data=df)
    plt.title("Bottom 10 Product's Total Profit over Time")
    plt.ylabel("Profit (AUD)")
    plt.xlabel("Product")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def product_average_sales_bar_graph(df):
    df = df.groupby('NAME').agg({'PROFIT':'mean'}).reset_index()
    df = df.filter(['NAME', 'PROFIT'])
    df = df.sort_values('PROFIT', ascending=False)
    df = df.head(20)
    ax = sns.barplot(x='NAME', y='PROFIT', data=df)
    plt.title("Top 20 Product's Average Profit over Time")
    plt.ylabel("Profit (AUD)")
    plt.xlabel("Product")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def season_profit_per_year(df):
    df = df.groupby(['season', 'Year'])['PROFIT'].agg('sum').reset_index()
    df = df.filter(['season', 'Year', 'PROFIT'])
    df = df.sort_values('PROFIT', ascending=False)
    colors = ['g', 'y', 'o', 'b']
    ax = sns.catplot(x='Year', y='PROFIT', hue='season', data=df, kind='bar')
    ax._legend.remove()
    plt.legend()
    plt.title("Profit by Season over the Years")
    plt.ylabel("Profit (AUD)")
    plt.xlabel("Year")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def customers_by_time_of_day(df):
    df = df.sort_values(by='TICKET')
    just_ticks = df['TICKET'].drop_duplicates().to_frame()
    prev_same = just_ticks['TICKET'].ne(just_ticks['TICKET'].shift())
    just_ticks['ticket_count'] = 0
    just_ticks.loc[prev_same, 'ticket_count'] += 1
    df = df.merge(just_ticks, on='TICKET')
    df['solo_time'] = df['Date'].str.split().str[1] 
    df['solo_time'] = df['solo_time'].str.split(':').str[0].astype(int) 
    df = df.groupby('solo_time')['ticket_count'].sum().reset_index()
    ax = sns.barplot(x='solo_time', y='ticket_count', data=df)
    plt.title("Total Number of Customers Every Hour")
    plt.ylabel("Total Number of Customers")
    plt.xlabel("Hour of Day (Military Time)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def customers_by_month(df):
    df = df.sort_values(by='TICKET')
    just_ticks = df['TICKET'].drop_duplicates().to_frame()
    prev_same = just_ticks['TICKET'].ne(just_ticks['TICKET'].shift())
    just_ticks['ticket_count'] = 0
    just_ticks.loc[prev_same, 'ticket_count'] += 1
    df = df.merge(just_ticks, on='TICKET')
    df['solo_time'] = df['Date'].str.split().str[0] 
    df['solo_time'] = df['solo_time'].str.split('-').str[1].astype(int) 
    df = df.groupby('solo_time')['ticket_count'].sum().reset_index()
    ax = sns.barplot(x='solo_time', y='ticket_count', data=df)
    plt.title("Total Number of Customers Every Month")
    plt.ylabel("Total Number of Customers")
    plt.xlabel("Month of Year")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def main():
    df = pd.read_csv(r'C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\datathon 3- Store\grocery_store_data_stage-1-cleaned.csv')
    df = df.drop('Unnamed: 0', axis=1)
    #product_total_sales_bar_graph(df)
    product_least_total_sales_bar_graph(df)
    #product_average_sales_bar_graph(df)
    #season_profit_per_year(df)
    #customers_by_time_of_day(df)
    #customers_by_month(df)

if __name__=="__main__":
    main()