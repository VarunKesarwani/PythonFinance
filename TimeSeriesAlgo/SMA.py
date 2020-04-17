import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'TCS'
query = "Select C.Symbol, D.* from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)

df = pd.read_sql(query, conn)

#SMA
df.index = df['Date']

df['30 days SMA'] = df['Close'].rolling(window=30).mean()
df['50 days SMA'] = df['Close'].rolling(window=50).mean()
df['90 days SMA'] = df['Close'].rolling(window=90).mean()

df[['Close','30 days SMA','50 days SMA','90 days SMA']].plot()

#print(df.head())
plt.show()