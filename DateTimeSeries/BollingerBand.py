import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'walmart_stock.csv',index_col='Date',parse_dates=True).sort_values(by='Date', ascending=True)

#20 day MA on close
df['Close: 30 Day Mean'] = df['Close'].rolling(window=20).mean()

#20 day positive Standard deviation 
df['Upper'] = df['Close: 30 Day Mean'] + 2*df['Close'].rolling(window=20).std()
#20 day negative Standard deviation 
df['Lower'] = df['Close: 30 Day Mean'] - 2*df['Close'].rolling(window=20).std()

#plot
df[['Close','Close: 30 Day Mean','Upper','Lower']].tail(200).plot(figsize=(16,6))

plt.show()