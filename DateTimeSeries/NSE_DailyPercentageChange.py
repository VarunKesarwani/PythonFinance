import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from dateutil.relativedelta import relativedelta
import pyodbc
from sqlalchemy import create_engine
from time import sleep

str_start = dt.datetime.today().date().strftime('%Y-%m-%d')
end= dt.datetime.today().date() + relativedelta(days=-3)
str_end = end 

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')
cursor = conn.cursor()
query = "Select top 10 [CompanyId], [Date],[Close] from CompanyDailyPriceData (nolock) where [Date] between '{}'  and '{}'".format(str_end,str_start)
print(query)
df = pd.read_sql(query, conn)

df['returns'] = df['Close'].pct_change(1)
print(df.head())
for col in df.iterrows():
    print(col['returns'])

#print(df.head(20))

