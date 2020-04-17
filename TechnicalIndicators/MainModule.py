import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import datetime as dt
import matplotlib.dates as mdates
import numpy as np

def RSI(series, n=14):
    deltas = np.diff(series)
    seed = deltas[:n-1]
    up = seed[seed>0].sum()/n
    down = -seed[seed<0].sum()/n
    rs= up/down
    rsi = np.zeros_like(series)
    rsi[:n]=100. - 100./(1. +rs)
    for i in range(n,len(series)):
        delta = deltas[i-1]
        if delta >0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = delta
        up = (up*(n-1)+upval)/n
        down =(down(n-1)+downval)/n
        rs= up/down
        rsi[i] = 100. - 100./(1. +rs)
    return rsi


conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'WIPRO'

df_Stock = pd.read_sql("Select D.[Date] as DateVal,D.[Open], D.[Close], D.[High], D.[Low],D.[Adj Close], D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol), conn)
df_Stock['DateVal'] = pd.to_datetime(df_Stock['DateVal'])

df_Stock['Date'] = df_Stock['DateVal'].map(mdates.date2num)

df_Stock.set_index('Date',inplace=True)
df_ohlc = df_Stock[['Open','High','Low','Close']]

res = RSI(df_ohlc,14)
print(res)