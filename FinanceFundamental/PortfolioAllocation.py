import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

df_HCL = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'HCLTECH'", conn)
df_TATAELXSI = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'TATAELXSI'", conn)
df_WIPRO = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'WIPRO'", conn)
df_INFY = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'INFY'", conn)

df_HCL.set_index('Date',inplace=True)
df_TATAELXSI.set_index('Date',inplace=True)
df_WIPRO.set_index('Date',inplace=True)
df_INFY.set_index('Date',inplace=True)

#Normalize Prices
for stock_df in (df_HCL,df_TATAELXSI,df_WIPRO,df_INFY):
    stock_df['Normed Return'] = stock_df['Adj Close']/stock_df.iloc[0]['Adj Close']
    print(stock_df)

#Allocations
# HCL 20%, Infy 30%, Wipro 30%, TataElxsi 20%
for stock_df,allo in zip([df_HCL,df_TATAELXSI,df_WIPRO,df_INFY],[.2,.2,.3,.3]):
    stock_df['Allocation'] = stock_df['Normed Return']*allo
    print(stock_df)

#Individual Portfolio Value
# if i had invested 1,00,000
def Individual_Pos_Val(isPlot = False):
    for stock_df in [df_HCL,df_TATAELXSI,df_WIPRO,df_INFY]:
        stock_df['Position Values'] = stock_df['Allocation']*1000000

    portfolio_val = pd.concat([df_HCL['Position Values'],df_TATAELXSI['Position Values'],df_WIPRO['Position Values'],df_INFY['Position Values']],axis=1)
    portfolio_val.columns = ['HCL Pos','TATAELXSI Pos','WIPRO Pos','INFY Pos']
    
    if isPlot == True:
        print(portfolio_val.head())
        #portfolio_val.drop('Total Pos',axis=1).plot(kind='line')
        portfolio_val.plot(kind='line')
    return portfolio_val


#Total Portfolio Value
def Total_Pos_Val(isPlot = False):
    portfolio_val_i = Individual_Pos_Val()
    portfolio_val_i['Total Pos'] = portfolio_val_i.sum(axis=1)
    if isPlot == True:
        print(portfolio_val_i.head())
        portfolio_val_i['Total Pos'].plot(figsize=(10,8))
        plt.title('Total Portfolio Value')
    return portfolio_val_i

#Individual_Pos_Val(isPlot=True)
def plotGraph():
    df_HCL['Adj Close'].pct_change(1).plot(kind='kde',label='HCLTECH')
    df_INFY['Adj Close'].pct_change(1).plot(kind='kde',label='INFY')
    df_WIPRO['Adj Close'].pct_change(1).plot(kind='kde',label='WIPRO')
    df_TATAELXSI['Adj Close'].pct_change(1).plot(kind='kde',label='TATAELXSI')

if __name__ == '__main__':
    #stock_correlation()
    #log_return()
    pair_wise_covariance()
    #Total_Pos_Val(isPlot=True)
    #plotGraph()
    plt.legend()
    plt.show()
