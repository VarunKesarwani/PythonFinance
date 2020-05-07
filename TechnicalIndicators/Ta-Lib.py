import pandas as pd
import ta
import pyodbc
import matplotlib.pyplot as plt
import matplotlib as style

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=.\SQLEXPRESS;'
                        'Database=ShareData;'
                        'UID=sa; PWD=varun@17;')

symbol = 'INFY'
query = "Select D.[Date] as DateValue,C.Symbol, D.[Open], D.[Close], D.[High], D.[Low], D.[Adj Close],D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)
df = pd.read_sql(query, conn)
rsi =  ta.momentum.RSIIndicator(close=df["Close"], n= 14, fillna= True)

df["rsi"] = rsi.rsi()

print(df["rsi"])

fig = plt.figure(figsize=(8,4), dpi=100)

df["rsi"].plot()

plt.show()