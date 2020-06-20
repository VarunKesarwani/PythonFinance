import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import ta

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=.\SQLEXPRESS;'
                        'Database=ShareData;'
                        'UID=sa; PWD=Bally@123;')

symbol = 'VOLTAS'
resample='N'

def get_Stock_Data():
    query = "Select D.[Date] as DateValue,C.Symbol, D.[Open], D.[Close], D.[High], D.[Low], D.[Adj Close],D.[Volume] from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)
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

rsi =  ta.momentum.RSIIndicator(close=ohlc["Close"], n= 14, fillna= True)
n1 = 50
n2 = 100

Av1 = movingaverage(df_ohlc['Close'],n1)
AV2= pd.DataFrame(simple_move_avg(df_ohlc,n2))
SP = len(df_ohlc['DateValue'][n1-1:])

rsi_res = rsi.rsi()

macd = ta.trend.MACD(close=df_ohlc["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd()
macd_signal = ta.trend.MACD(close=df_ohlc["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd_signal()
macd_diff = ta.trend.MACD(close=df_ohlc["Close"],n_slow=26,n_fast=12,n_sign=9,fillna=True).macd_diff()
print(macd)

label1 = str(n1)+' days SMA'
label2 = str(n2)+' days SMA'

#plot
fig = plt.figure()

ax0 =plt.subplot2grid((6,4),(0,0),rowspan=1,colspan=4)
rsiColor="#00ffe8"
posCol = "#386d13"
ax0.plot(df_ohlc['DateValue'][-SP:],rsi_res[-SP:])
ax0.axhline(70,color=rsiColor)
ax0.axhline(30,color=posCol)
ax0.spines['bottom'].set_color("#5998ff")
ax0.spines['top'].set_color("#5998ff")
ax0.spines['left'].set_color("#5998ff")
ax0.spines['right'].set_color("#5998ff")
ax0.set_yticks([30,70])
#
plt.ylabel("RSI")
#plt.title(symbol)


ax1 = plt.subplot2grid((6,4),(1,0),rowspan=4,colspan=4)
candlestick_ohlc(ax1, ohlc.values, width=.6, colorup='#77d879', colordown='#db3f3f')
ax1.plot(df_ohlc['DateValue'][-SP:],Av1[-SP:],color="#5998ff",label=label1,linewidth=1.5)
ax1.plot(AV2.index,AV2[str(n2)+' days SMA'],color="#0EEDF9",label=label2,linewidth=1.5)
ax1.plot()
ax1.grid(True)
plt.ylabel('Price')

ax1v = ax1.twinx()
ax1v.bar(df_Volume.index,df_Volume)
ax1v.set_ylim(0,2*df_Volume.max())
ax1v.grid(False)

ax2 = plt.subplot2grid((6,4),(5,0),rowspan=1,colspan=4)
ax2.plot(df_ohlc['DateValue'][-SP:],macd[-SP:])
ax2.plot(df_ohlc['DateValue'][-SP:],macd_signal[-SP:])
ax2.axhline(0,color=rsiColor)
ax2.spines['bottom'].set_color("#5998ff")
ax2.spines['top'].set_color("#5998ff")
ax2.spines['left'].set_color("#5998ff")
ax2.spines['right'].set_color("#5998ff")
ax2.yaxis.set_ticks_position('left')
ax2.xaxis.set_ticks_position('bottom')
plt.ylabel('MACD')


ax2v = ax2.twinx()
ax2v.bar(df_ohlc['DateValue'][-SP:],macd_diff[-SP:])



plt.legend(prop={'size':7})
for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)


#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
plt.suptitle(symbol)

plt.setp(ax0.get_xticklabels(),visible=False)
plt.setp(ax1.get_xticklabels(),visible=False)
plt.setp(ax2v.get_yticklabels(),visible=False)
plt.setp(ax1v.get_yticklabels(),visible=False)

plt.subplots_adjust(left=.09,bottom=.18,right=.94,top=.94,wspace=.20,hspace=0)
plt.show()
