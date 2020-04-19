import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import datetime as dt
import matplotlib.dates as mdates
import numpy as np

ewma = pd.Series.ewm
# def RSI(series, n=14):
#     deltas = np.diff(series)
#     seed = deltas[:n-1]
#     up = seed[seed>0].sum()/n
#     down = -seed[seed<0].sum()/n
#     rs= up/down
#     rsi = np.zeros_like(series)
#     rsi[:n]=100. - 100./(1. +rs)
#     for i in range(n,len(series)):
#         delta = deltas[i-1]
#         if delta >0:
#             upval = delta
#             downval = 0.
#         else:
#             upval = 0.
#             downval = delta
#         up = (up*(n-1)+upval)/n
#         down =(down(n-1)+downval)/n
#         rs= up/down
#         rsi[i] = 100. - 100./(1. +rs)
#     return rsi


conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'WIPRO'

df_Stock = pd.read_sql("Select D.[Date],D.[Open], D.[Close], D.[High], D.[Low],D.[Adj Close], D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol), conn)
df_Stock['Date'] = pd.to_datetime(df_Stock['Date'])

# def RSI(series,n):    
#     delta = series.diff()
#     u = delta * 0 
#     d = u.copy()
#     i_pos = delta > 0
#     i_neg = delta < 0
#     u[i_pos] = delta[i_pos]
#     d[i_neg] = delta[i_neg]
#     rs = ewma(u, span=n).mean() / ewma(d, span=n).mean()
#     return 100 - 100 / (1 + rs)

def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
    pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)
    
n = 14
print(RSI(df_Stock.Close,n))