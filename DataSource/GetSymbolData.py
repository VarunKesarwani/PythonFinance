import pandas as pd
from sqlalchemy import create_engine

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

df_web = pd.read_csv('https://www1.nseindia.com/content/equities/EQUITY_L.csv')
df_web.columns=['SYMBOL','NAME_OF_COMPANY','SERIES','DATE_OF_LISTING','PAID_UP_VALUE','MARKET_LOT','ISIN NUMBER','FACE_VALUE']
print(df_web.head())


for row in df_web.iterrows():
    result = row[1]
    symbol = str(result.get(key = 'SYMBOL'))
    getSymbolQuery = "SELECT * FROM [dbo].[Company] (nolock) where Symbol = '{}'".format(symbol)
    df_comp = pd.read_sql(getSymbolQuery,engine)
    if df_comp.empty:
        CompanyName = str(result.get(key = 'NAME_OF_COMPANY'))
        Series = str(result.get(key = 'SERIES'))
        DateOfListing = str(result.get(key = 'DATE_OF_LISTING'))
        FaceValue = str(result.get(key = 'FACE_VALUE'))
        insertSymbolQuery="INSERT INTO [dbo].[Company] ([Symbol],[CompanyName],[Series],[DateOfListing],[Sector]) VALUES('{}','{}','{}','{}','')".format(symbol,CompanyName,Series,DateOfListing)
        with engine.connect() as con:
            con.execute(insertSymbolQuery)
    else:
        print(symbol+' already Found')
    



