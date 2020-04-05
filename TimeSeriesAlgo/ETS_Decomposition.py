import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
symbol = 'ASIANPAINT'
query = "Select C.Symbol, D.[Date],D.[Close] from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = '{}'".format(symbol)

df = pd.read_sql(query, conn)

df.dropna(inplace=True)

df.index = pd.to_datetime(df['Date'])

df_2019 = df.loc['2019-4-1':]

result = seasonal_decompose(df_2019['Close'], model='multiplicative', period=30)

result.plot()

fig, axs = plt.subplots(nrows = 2,ncols =2, figsize=(12,12))

#fig=plt.figure(figsize=(12,12))
#a1 = plt.subplot2grid((3,3),(0,0),colspan = 2)
#a2 = plt.subplot2grid((3,3),(0,2), rowspan = 3)
#a3 = plt.subplot2grid((3,3),(1,0),rowspan = 2, colspan = 2)

#a1.plot(df['Close']['2019-4-1':],'b')
#a2.plot(result.seasonal,'b')
#a3.plot(result.trend,'b')

axs.flatten()

axs[0,0].plot(df_2019['Date'],df_2019['Close'])
axs[0,0].set_title('CLose')

axs[0, 1].plot(df_2019['Date'],result.seasonal, 'orange')
axs[0, 1].set_title('Seasonal')

axs[1, 0].plot(df_2019['Date'],result.trend, 'green')
axs[1, 0].set_title('Trend')

axs[1, 1].plot(df_2019['Date'],result.observed, 'red')
axs[1, 1].set_title('Observed')

plt.tight_layout()

plt.show()

