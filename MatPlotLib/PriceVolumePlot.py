import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'WIPRO'

df_Stock = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol), conn)
df_Stock['Date'] = pd.to_datetime(df_Stock['Date'])
df_Stock.set_index('Date',inplace=True)

df_Stock['50 days SMA'] = df_Stock['Adj Close'].rolling(window=50).mean()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=4,colspan=1)
ax2 = plt.subplot2grid((6,1),(4,0),rowspan=2,colspan=1,sharex=ax1)


ax1.plot(df_Stock.index,df_Stock['Adj Close'],label='Close')
ax1.plot(df_Stock.index,df_Stock['50 days SMA'],label='50 Day SMA')
ax1.legend()
ax1.grid(True)


ax2.bar(df_Stock.index,df_Stock['Volume'])
plt.ylabel('Volume')
#ax2.xaxis.set_major_locator(dates.MonthLocator())
#ax2.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
ax2.axes.yaxis.set_ticklabels([])
plt.xlabel('Date')


plt.suptitle(symbol+' Close Price')

#remove x axis of price chart
plt.setp(ax1.get_xticklabels(),visible=False)
#plt.tight_layout()
plt.subplots_adjust(left=.09,bottom=.18,right=.94,top=.94,wspace=.20,hspace=0)
plt.show()