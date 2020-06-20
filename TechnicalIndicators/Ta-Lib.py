import pandas as pd
import ta
import pyodbc
import matplotlib.pyplot as plt
import matplotlib as style

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=.\SQLEXPRESS;'
                        'Database=ShareData;'
                        'UID=sa; PWD=Bally@123;')

symbol = 'INFY'
query = "Select D.[Date] as DateValue,C.Symbol, D.[Open], D.[Close], D.[High], D.[Low], D.[Adj Close],D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)
df = pd.read_sql(query, conn)
rsi =  ta.momentum.RSIIndicator(close=df["Close"], n= 14, fillna= True).rsi()

stock = ta.momentum.StochasticOscillator(high=df["High"],low=df["Low"],close=df["Close"],n = 14, d_n = 3, fillna = False).stoch_signal()

macd_signal = ta.trend.MACD(close=df["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd_signal()
macd_diff = ta.trend.MACD(close=df["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd_diff()
macd = ta.trend.MACD(close=df["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd()

ema9 = ta.trend.EMAIndicator(macd,9,True).ema_indicator()
print(rsi)
print(stock)
print(macd.tail())

fig = plt.figure(figsize=(8,4), dpi=100)

macd.plot()
#macd_signal.plot()
ema9.plot()


plt.show()