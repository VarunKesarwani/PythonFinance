import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=Bally@123;')

query = 'SELECT [Id],[Symbol],[CompanyName] FROM [dbo].[Company](nolock)'

df = pd.read_sql(query, conn)

#print(df.head())

table = pd.read_html('https://www.samco.in/knowledge-center/articles/nse-listed-companies/')

df_Web = table[0]
df_Web['CompanyName'] = table[0]['NAME OF COMPANY']
#df_Web['Shares Issued 2'] = table[0]['Shares Issued'].astype(int)
#print(df_Web)

pd_Merge = pd.merge(df_Web,df,on=['CompanyName'])

header = ["Id", "CompanyName", "FACE VALUE",'Price', "Market Cap","EPS","PE","Shares Issued"]
#pd_Merge.column = header
print(pd_Merge.head())

deleteCompanyDetail = "truncate table [dbo].[CompanyDetails]"

for row in pd_Merge.iterrows():
    result = row[1]
    CompanyId = result.get(key = 'Id')
    CompanyName = str(result.get(key = 'CompanyName'))
    facevalue = result.get(key = 'FACE VALUE')
    MarketCap = result.get(key = 'Market Cap')
    EPS = str(result.get(key = 'EPS'))
    PE = result.get(key = 'PE')
    Shares_Issued = result.get(key = 'Shares Issued')
    insetSamcoData = "INSERT INTO [dbo].[CompanyDetails]([CompanyId],[CompanyName],[FaceValue],[MarketCap],[EPS],[PE],[SharedIssued])VALUES({},'{}',{},{},{},{},{})".format(CompanyId,CompanyName,facevalue,MarketCap,EPS,PE,Shares_Issued )
    print(insetSamcoData)


#pd_Merge.to_csv('D:\ShareData\CompanyDetail.csv',index= False,columns = header)