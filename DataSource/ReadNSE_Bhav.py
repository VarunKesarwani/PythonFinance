import pandas as pd
from sqlalchemy import create_engine

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

query = "SELECT [Id] as CompanyId,[Symbol] as Symbol FROM [dbo].[Company] (nolock)"
df_comp = pd.read_sql(query,engine)

df_web = pd.read_csv('https://www1.nseindia.com/products/content/sec_bhavdata_full.csv')

print('Download Completed!!!')

df_web.columns=['Symbol','Series','Date','Prev_Close','Open_Price',
       'High_Price','LowPrice','Last_Price','Close_Price',
       'Avg_Price','Volume','TradedValue','NumOfTrades',
       'DeliveryQuantity','DeliveryPercentage']

df_merge = pd.merge(df_comp,df_web,on='Symbol')
df_merge['Date'] = pd.to_datetime(df_merge['Date'])
print(df_merge['Date'].head())
query_validate = "select top 1 1 from CompanyDailyBhavData (nolock) where [Date]= '{}'".format(df_merge['Date'][1])
value = pd.read_sql(query_validate,engine)

if value.empty:
    df_sql = df_merge[['CompanyId','Date','Prev_Close','Open_Price',
        'High_Price','LowPrice','Last_Price','Close_Price',
        'Avg_Price','Volume','TradedValue','NumOfTrades',
        'DeliveryQuantity','DeliveryPercentage']].copy()
    df_sql.to_sql("CompanyDailyBhavData",engine, if_exists='append', index=False)
    print('value inserted successfully')
else:
    print('value already inserted')


#filename ='DB/'+ url.split('/')[-1] +'_'+dt_date

#with open(filename,'wb') as output_file:
    #output_file.write(r.content)