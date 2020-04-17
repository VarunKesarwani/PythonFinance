import pandas as pd

#print(df.head())

table = pd.read_html('https://www.nseindia.com/reports/fii-dii')

df_Web = table[0]


print(df_Web)