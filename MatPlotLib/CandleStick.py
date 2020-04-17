import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

symbol = 'INFY'
sample='N'
query = "Select D.[Date] as DateValue,C.Symbol, D.[Open], D.[Close], D.[High], D.[Low], D.[Adj Close],D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)
df = pd.read_sql(query, conn)

df['DateValue'] = pd.to_datetime(df['DateValue'])
df.set_index(df['DateValue'],inplace=True)

df_ohlc = pd.DataFrame()
df_Volume = pd.DataFrame()

if sample=='Y':
    df_ohlc = df['Adj Close'].resample(rule='10d').ohlc()
    df_Volume = df['Volume'].resample('10d').sum()

    df_ohlc.columns = ['Open', 'High', 'Low','Close']
else:
    df_ohlc = df[['Open','High','Low','Close']]
    df_Volume = df['Volume']

df_ohlc['Date'] = df['DateValue'].map(mdates.date2num)
df_ohlc.reset_index(inplace=True)
 
ohlc= df_ohlc[['Date', 'Open', 'High', 'Low','Close']].copy()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=4,colspan=1)
ax2 = plt.subplot2grid((6,1),(4,0),rowspan=2,colspan=1,sharex=ax1)
ax1.grid(True)

candlestick_ohlc(ax1, ohlc.values, width=.6, colorup='#77d879', colordown='#db3f3f')

#ax2.fill_between(df_Volume.index.map(mdates.date2num),df_Volume.values,0)


ax2.bar(df_Volume.index,df_Volume)
ax2.axes.yaxis.set_ticklabels([])
for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

plt.xlabel('Date')
plt.ylabel('Price')

plt.setp(ax1.get_xticklabels(),visible=False)
plt.subplots_adjust(left=.09,bottom=.18,right=.94,top=.94,wspace=.20,hspace=0)
plt.show()
