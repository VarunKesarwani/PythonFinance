import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader
import datetime
import pandas_datareader.data as web

start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 1, 1)
tesla = web.DataReader("TSLA", 'yahoo', start, end)
ford = web.DataReader("F", 'yahoo', start, end)
gm = web.DataReader("GM",'yahoo',start,end)

#tesla.to_csv('Tesla_Stock.csv')
#ford.to_csv('Ford_Stock.csv')
#gm.to_csv('GM_Stock.csv')

#Daily Percentage Change
tesla['returns'] = tesla['Close'].pct_change(1)
ford['returns'] = ford['Close'].pct_change(1)
gm['returns'] = gm['Close'].pct_change(1)

tesla['returns'].hist(bins=100,label='Tesla',figsize=(10,8),alpha=0.5)
gm['returns'].hist(bins=100,label='GM',alpha=0.5)
ford['returns'].hist(bins=100,label='Ford',alpha=0.5)
plt.legend()

plt.show()

"""
Basically this just informs you of your percent gain (or loss) if you bought the stock on day and then sold it the next day. 
While this isn't necessarily helpful for attempting to predict future values of the stock, 
its very helpful in analyzing the volatility of the stock. 
If daily returns have a wide distribution, the stock is more volatile from one day to the next
"""