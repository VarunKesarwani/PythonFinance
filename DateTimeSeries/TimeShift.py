import numpy as np
import pandas as pd

df = pd.read_csv(r'D:\ShareData\TCS.csv',index_col='Date',parse_dates=True).sort_values(by='Date', ascending=True)
print(df)
#Period
print(df.head())
print(df.tail())
print(df.shift(periods=1).head())
print(df.shift(periods=1).tail())

print(df.head())
print(df.tail())
print(df.shift(periods=-1).head())
print(df.shift(periods=-1).tail())

#tShift
print(df.tshift(periods=1,freq='M').head())
