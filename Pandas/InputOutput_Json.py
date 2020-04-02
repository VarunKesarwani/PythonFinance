import pandas as pd

df_ITC = pd.read_json(r'D:\ShareData\ITC.json')

print(df_ITC.head())

#df_TATAELEXI.head().to_json('TATAEL.csv',orient='table')