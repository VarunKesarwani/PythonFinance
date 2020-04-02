import pandas as pd

#read
df = pd.read_csv(r'D:\ShareData\TCS.csv')
print(df)

#Wrire
df.to_csv('eg.csv',index= False)

df2 = pd.read_csv(r'eg.csv')
print(df2)

