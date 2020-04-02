import pandas as pd

import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=10.2.118.163\MSSQL2016;'
                      'Database=GLP_CMP;'
                      'UID=sa; PWD=abcd@1234;')

query = 'Select top 10 PlayerId,Title,FirstName,LastName from [dbo].[tPlayer](nolock)'

df = pd.read_sql(query, conn)

print(df)