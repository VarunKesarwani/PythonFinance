import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

df_HCL = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'HCLTECH'", conn)
df_HCL['Date'] = pd.to_datetime(df_HCL['Date'])
df_HCL.set_index('Date',inplace=True)

df_HCL['50 days SMA'] = df_HCL['Adj Close'].rolling(window=50).mean()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)

ax1.plot(df_HCL.index,df_HCL['Adj Close'])
ax1.plot(df_HCL.index,df_HCL['50 days SMA'])
ax2.bar(df_HCL.index,df_HCL['Volume'])

plt.tight_layout()

plt.show()