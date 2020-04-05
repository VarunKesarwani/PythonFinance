import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'TCS'
query = "Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)

df = pd.read_sql(query, conn)


df['Date'] = pd.to_datetime(df['Date'])

df.set_index('Date',inplace=True)

print(df.head())

df['50 days EMA'] = df['Close'].ewm(span=50).mean()

df[['Close','50 days EMA']].plot()

plt.show()