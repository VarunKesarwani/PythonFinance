
import pandas as pd
import matplotlib.pyplot as plt
import datetime
#from matplotlib.finance import candlestick_ohlc #pip install mplfinance
from mpl_finance import candlestick_ohlc #pip install mplfinance


# from mpl_finance import candlestick_ohlc

import matplotlib.dates as mdates


df = pd.read_csv(r'D:\ShareData\TCS - Copy.csv')

# ensuring only equity series is considered
df = df.loc[df['Series'] == 'EQ']
print(df)
# Converting date to pandas datetime format

df['Date'] = pd.to_datetime(df['Date'])
df["Date"] = df["Date"].apply(mdates.date2num)

# Creating required data in new DataFrame OHLC
ohlc= df[['Date', 'Open Price', 'High Price', 'Low Price','Close Price']].copy()

# In case you want to check for shorter timespan
# ohlc =ohlc.tail(60)

f1, ax = plt.subplots(figsize = (10,5))

# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Saving image
plt.savefig('OHLC TCS.png')

# In case you dont want to save image but just displya it
plt.show()
