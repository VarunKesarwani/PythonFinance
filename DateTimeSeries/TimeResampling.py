import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#Step1 Getting Data

#There are two method of getting Financial data.
#direct method of defing Index and this faster way but less Controll

df_sh = pd.read_csv(r'D:\ShareData\TCS.csv',index_col='Date',parse_dates=True)

#Longer and Controlled Method of defining idex
df = pd.read_csv(r'D:\ShareData\TCS.csv')
#print(df.head())
print(df.info())

#Step 2 Convert datetime format and assign Index
#convert Date column to type datetime data type
df['Date'] = pd.to_datetime(df['Date'])
#Method 2
#df['Date'] = df['Date'].apply(pd.to_datetime)

print(df.info())

#Step 2.1 Assign index
df.set_index('Date',inplace=True)

print(df.head())

#Step 3 resampling data as required
#Resampling
print('Resampling')
#Using In built functions
#Monthly mean
print(df.resample(rule='M').mean())
print(df.resample(rule='M').max())
print(df['TotalTradedQuantity'].resample(rule='M').sum())

#Customer Method
def first_day(entry):
    #Returns the first instance of the period, regardless of samplling rate.
    return entry[0]

print(df.resample(rule='M').apply(first_day))

#Step 4 Plotting Graph
df['OpenPrice'].resample('M').mean().plot(kind='bar')
plt.title('Monthly Mean Open Price for TCS')

plt.show()