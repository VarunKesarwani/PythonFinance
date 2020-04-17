import pandas as pd
import ta
import matplotlib.pyplot as plt
import pyodbc
import matplotlib.dates as mdates

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'WIPRO'

df_Stock = pd.read_sql("Select D.[Date] as DateVal,D.[Open], D.[Close], D.[High], D.[Low] from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol), conn)
df_Stock['DateVal'] = pd.to_datetime(df_Stock['DateVal'])

df_Stock['Date'] = df_Stock['DateVal'].map(mdates.date2num)

df_Stock.set_index('Date',inplace=True)
df_ohlc = df_Stock[['Open','Close','High','Low']]

df_RSI = ta.momentum.RSIIndicator(close=df_ohlc['Close'],n=14,fillna=True)

print(df_RSI)