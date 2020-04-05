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

#Allocations
# HCL 20%, Infy 30%, Wipro 30%, TataElxsi 20%
for stock_df,allo in zip([df_HCL,df_TATAELXSI,df_WIPRO,df_INFY],[.2,.2,.3,.3]):
    stock_df['Allocation'] = stock_df['Normed Return']*allo
#print(df_HCL.head())

#Investment
# if i had invested 1,00,000
for stock_df in [df_HCL,df_TATAELXSI,df_WIPRO,df_INFY]:
    stock_df['Position Values'] = stock_df['Allocation']*1000000

portfolio_val = pd.concat([df_HCL['Position Values'],df_TATAELXSI['Position Values'],df_WIPRO['Position Values'],df_INFY['Position Values']],axis=1)
portfolio_val.columns = ['HCL Pos','TATAELXSI Pos','WIPRO Pos','INFY Pos']



#total portfolio value at end of each day
portfolio_val['Total Pos'] = portfolio_val.sum(axis=1)
print(portfolio_val.head())

#Plot graph
#portfolio_val['Total Pos'].plot(figsize=(10,8))
#plt.title('Total Portfolio Value')

#individual graph
#portfolio_val.drop('Total Pos',axis=1).plot(kind='line')

#dail return
portfolio_val['Daily Return'] = portfolio_val['Total Pos'].pct_change(1)
#print(portfolio_val.head())

#Cumulative Return
cum_ret = 100 * (portfolio_val['Total Pos'][-1]/portfolio_val['Total Pos'][0] -1 )
print('Our return {} was percent!'.format(cum_ret))

#Avg Daily Return
portfolio_val['Daily Return'].mean()
print('Avg Dail Return = {}'.format(cum_ret))
#Std Daily Return
portfolio_val['Daily Return'].std()
print('Std Dail Return = {}'.format(cum_ret))

#portfolio_val['Daily Return'].plot(kind='kde')

#Sharpe Ratio
#The Sharpe Ratio is a measure for calculating risk-adjusted return, 
#and this ratio has become the industry standard for such calculations.
#SR = (portfolio_val['Daily Return'].mean()- 0.82)/portfolio_val['Daily Return'].std()
SR = portfolio_val['Daily Return'].mean()/portfolio_val['Daily Return'].std()
print(portfolio_val['Daily Return'].mean())
print(SR)

#Anual Sharpe ratio
ASR = (252**0.12)*SR
print(ASR)

#KDE plot
df_HCL['Adj Close'].pct_change(1).plot(kind='kde',label='HCLTECH')
df_INFY['Adj Close'].pct_change(1).plot(kind='kde',label='INFY')
df_WIPRO['Adj Close'].pct_change(1).plot(kind='kde',label='WIPRO')
df_TATAELXSI['Adj Close'].pct_change(1).plot(kind='kde',label='TATAELXSI')
plt.legend()
plt.show()