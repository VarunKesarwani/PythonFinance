import pandas as pd
from sqlalchemy import create_engine

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])



df_web = pd.read_csv('https://www1.nseindia.com/content/equities/EQUITY_L.csv')

query = "SELECT * FROM [dbo].[Company] (nolock)"
df_comp = pd.read_sql(query,engine)

print (df_web)