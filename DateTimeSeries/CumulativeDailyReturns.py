import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


tesla =  pd.read_csv(r'D:\ShareData\FinApp\07-Stock-Market-Analysis-Capstone-Project\Tesla_Stock.csv',index_col='Date',parse_dates=True)
ford = pd.read_csv(r'D:\ShareData\FinApp\07-Stock-Market-Analysis-Capstone-Project\Ford_Stock.csv',index_col='Date',parse_dates=True)
gm = pd.read_csv(r'D:\ShareData\FinApp\07-Stock-Market-Analysis-Capstone-Project\GM_Stock.csv',index_col='Date',parse_dates=True)

#Daily Percentage Change
tesla['returns'] = tesla['Close'].pct_change(1)
ford['returns'] = ford['Close'].pct_change(1)
gm['returns'] = gm['Close'].pct_change(1)


#Cumulative Daily Returns
tesla['Cumulative Return'] = (1 + tesla['returns']).cumprod()
ford['Cumulative Return'] = (1 + ford['returns']).cumprod()
gm['Cumulative Return'] = (1 + gm['returns']).cumprod()

print(tesla.head())

tesla['Cumulative Return'].plot(label='Tesla',figsize=(16,8),title='Cumulative Return')
ford['Cumulative Return'].plot(label='Ford')
gm['Cumulative Return'].plot(label='GM')
plt.legend()


plt.show()

"""
With daily cumulative returns, the question we are trying to answer is the following, 
if I invested $1 in the company at the beginning of the time series, how much would is be worth today? 
This is different than just the stock price at the current day, because it will take into account the daily returns. 
Keep in mind, our simple calculation here won't take into account stocks that give back a dividend. 
Let's look at some simple examples:
"""