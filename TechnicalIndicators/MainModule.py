from Technical_Indicators import *
#from Tech__Indicator2 import RSI
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import datetime as dt
import matplotlib.dates as mdates

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'WIPRO'

df_Stock = pd.read_sql("Select D.[Date],D.[Open], D.[Close], D.[High], D.[Low] from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol), conn)
df_Stock['Date'] = pd.to_datetime(df_Stock['Date'])

#df_Stock['Date'] = df_Stock['Date'].map(mdates.date2num)

df_Stock.set_index('Date',inplace=True)
#print(df_Stock)

RSI_date = dt.datetime(2020,3,15)
df_MA = moving_average(df_Stock,14)

df_momentum = momentum(df_Stock,14)

df_ATR = average_true_range(df_Stock,14)

print(df_ATR)