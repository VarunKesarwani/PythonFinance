import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
Symbol = 'VOLTAS'
query = "Select C.Symbol, B.* from CompanyDailyBhavData B inner join Company c on B.CompanyId = c.Id where C.Symbol like '%{}%'".format(Symbol)
df_comp = pd.read_sql(query,engine)

#print(df_comp.head())
fig = plt.figure()

ax0 =plt.subplot2grid((9,6),(0,0),rowspan=3,colspan=6)
ax0.plot(df_comp['Date'],df_comp['Close_Price'])
ax0.plot(df_comp['Date'],df_comp['Avg_Price'])


ax0v = ax0.twinx()
ax0v.bar(df_comp['Date'],df_comp['Volume'])
ax0v.set_ylim(0,2*df_comp['Volume'].max())
ax0v.grid(False)

ax1 =plt.subplot2grid((9,6),(3,0),rowspan=3,colspan=6)
ax1.plot(df_comp['Date'],df_comp['TradedValue'])

ax1v = ax1.twinx()
ax1v.bar(df_comp['Date'],df_comp['NumOfTrades'])
ax1v.grid(False)

ax2 =plt.subplot2grid((9,6),(6,0),rowspan=4,colspan=6)
ax2.plot(df_comp['Date'],df_comp['DeliveryQuantity'])
ax2v = ax2.twinx()
ax2v.bar(df_comp['Date'],df_comp['DeliveryPercentage'])
ax2v.grid(False)

plt.legend(prop={'size':7})
for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

plt.setp(ax0.get_xticklabels(),visible=False)
plt.setp(ax1.get_xticklabels(),visible=False)
plt.setp(ax0v.get_yticklabels(),visible=False)
plt.setp(ax1v.get_yticklabels(),visible=False)
plt.setp(ax2v.get_yticklabels(),visible=False)

plt.show()

