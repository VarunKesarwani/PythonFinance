import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

query = 'SELECT [Id],[Symbol],[CompanyName] FROM [dbo].[Company](nolock)'

df = pd.read_sql(query, conn)

#print(df.head())

table = pd.read_html('https://www.samco.in/knowledge-center/articles/nse-listed-companies/')

df_Web = table[0]
df_Web['CompanyName'] = table[0]['NAME OF COMPANY']
#df_Web['Shares Issued 2'] = table[0]['Shares Issued'].astype(int)
#print(df_Web)

pd_Merge = pd.merge(df_Web,df,on=['CompanyName'])

header = ["Id", "CompanyName", "FACE VALUE", "Market Cap","EPS","PE","Shares Issued"]
pd_Merge.to_csv('D:\ShareData\CompanyDetail.csv',index= False,columns = header)