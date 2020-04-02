import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'walmart_stock.csv',index_col='Date',parse_dates=True).sort_values(by='Date', ascending=True)

#Rolling
#Example moving Avg
df['Close: 30 Day Mean'] = df['Close'].rolling(window=30).mean()
df[['Close','Close: 30 Day Mean']].plot(figsize=(16,6))




plt.show()