import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from dateutil.relativedelta import relativedelta
import pyodbc
from sqlalchemy import create_engine
from time import sleep

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=Bally@123;')

query = "SELECT [Id],[Symbol]+'.NS' as Symbol FROM [dbo].[Company] (nolock) where Series ='EQ' and Id in (select distinct CompanyId from LogTable where InsertDate != GETDATE()) order by 2"

start = dt.datetime.today()
end = dt.datetime.today()

#daily= 1; monthly= 2; quaterly= 3; half-yearly= 4; yearly= 5; 
#2 years= 6; 3 years= 7; 5 years= 8; weekly = 9; forth night= 10

interval = 11

if interval == 1:
    start = start + relativedelta(days=-1)
elif interval == 2:
    start = start + relativedelta(months=-1)
elif interval == 3:
    start = start + relativedelta(months=-3) 
elif interval == 4:
    start = start + relativedelta(months=-6)  
elif interval == 5:
    start = start + relativedelta(years=-1) 
elif interval == 6:
    start = start + relativedelta(years=-2)  
elif interval == 7:
    start = start + relativedelta(years=-3)  
elif interval == 8:
    start = start + relativedelta(years=-5)  
elif interval == 9:
    start = start + relativedelta(weeks=-1)  
elif interval == 10:
    start = start + relativedelta(weeks=-2) 
elif interval == 11:
    start = dt.datetime(2020,4,8)
else:
    pass

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

try:
    df = pd.read_sql(query, conn)

    def GetData(value):
        #str_Start = dt.datetime(2020,4,5)
        #str_end = dt.datetime(2020,4,7)
        return web.DataReader(value,'yahoo',start,end)
        
    def InsertData(data):
        data.to_sql(name='CompanyDailyPriceData', con=engine, if_exists = 'append', index=False)

    for row_index,row in df[['Id','Symbol']].iterrows():
        try:
            #if (row['Id'] != 144801) or (row['Id'] != 67601):
            print(row['Id'])
            df = GetData(row['Symbol'])
            df['CompanyId'] = row['Id']
            df['Date'] = df.index 
            InsertData(df)
            print(row['Symbol'])
            sleep(1)
        except Exception as e:
            print('error',e)

except Exception as e:
    print('error',e)
finally:
    print('finihed')
    





    
    