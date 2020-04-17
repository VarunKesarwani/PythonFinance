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
resample='N'

def get_Stock_Data():
    query = "Select D.[Date] as DateValue,C.Symbol, D.[Open], D.[Close], D.[High], D.[Low], D.[Adj Close],D.[Volume] from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)
    df = pd.read_sql(query, conn)

    df['DateValue'] = pd.to_datetime(df['DateValue'])
    df.set_index(df['DateValue'],inplace=True)

    df_ohlc = pd.DataFrame()
    df_Volume = pd.DataFrame()

    if resample=='Y':
        df_ohlc = df['Adj Close'].resample(rule='10d').ohlc()
        df_Volume = df['Volume'].resample('10d').sum()
        df_ohlc.columns = ['Open', 'High', 'Low','Close']
    else:
        df_ohlc = df[['Open','High','Low','Close','Adj Close']]
        df_Volume = df['Volume']

    df_ohlc['Date'] = df['DateValue'].map(mdates.date2num)
    df_ohlc.reset_index(inplace=True)
    return df_ohlc,df_Volume

def simple_move_avg(sma_data,n):
    data = sma_data.copy()
    if resample =='Y':
        data[str(n)+' days SMA'] = data['Close'].rolling(window=n).mean()
    else:
        data[str(n)+' days SMA'] = data['Adj Close'].rolling(window=n).mean()
    data['DateValue'] = pd.to_datetime(data['DateValue'])
    data.set_index(data['DateValue'],inplace=True)
    #return data[['DateValue',str(n)+' days SMA']].dropna()
    return data[str(n)+' days SMA'].dropna()

def movingaverage(value,n):
    weights = np.repeat(1.0,n)/n
    smas= np.convolve(value,weights,'valid')
    return smas
    

df_ohlc,df_Volume = get_Stock_Data()

ohlc= df_ohlc[['Date', 'Open', 'High', 'Low','Close']].copy()

n1 = 26
n2 = 52

Av1 = movingaverage(df_ohlc['Close'],n1)
AV2= pd.DataFrame(simple_move_avg(df_ohlc,n2))
SP = len(df_ohlc['DateValue'][n1-1:])

label1 = str(n1)+' days SMA'
label2 = str(n2)+' days SMA'
#plot
fig = plt.figure()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=4,colspan=1)
candlestick_ohlc(ax1, ohlc.values, width=.6, colorup='#77d879', colordown='#db3f3f')
ax1.plot(df_ohlc['DateValue'][-SP:],Av1[-SP:],color="#5998ff",label=label1,linewidth=1.5)
ax1.plot(AV2.index,AV2[str(n2)+' days SMA'],color="#0EEDF9",label=label2,linewidth=1.5)
ax1.plot()
ax1.grid(True)
plt.ylabel('Price')
plt.title(symbol+' Candlestick')
plt.legend(prop={'size':7})

ax2 = plt.subplot2grid((6,1),(4,0),rowspan=2,colspan=1,sharex=ax1)
ax2.bar(df_Volume.index,df_Volume)
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%B'))

ax2.axes.yaxis.set_ticklabels([])
for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
plt.xlabel('Date')
plt.ylabel('Volume')

plt.setp(ax1.get_xticklabels(),visible=False)
plt.subplots_adjust(left=.09,bottom=.18,right=.94,top=.94,wspace=.20,hspace=0)
plt.show()
