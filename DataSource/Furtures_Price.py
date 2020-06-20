import requests
import io
import zipfile
import pandas as pd
from sqlalchemy import create_engine

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}
engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

def download_extract_zip(url):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            #print(zipinfo)
            with thezip.open(zipinfo) as thefile:
                #print(zipinfo.filename, thefile.read())
                df_web = pd.read_csv(thefile)
                print()
                #df_Futidx = df_web[['TIMESTAMP','SYMBOL','EXPIRY_DT','OPEN','HIGH','LOW','CLOSE','SETTLE_PR','CONTRACTS','VAL_INLAKH','OPEN_INT','CHG_IN_OI']].copy()[df_web["INSTRUMENT"]=="FUTIDX" or df_web["INSTRUMENT"]=="FUTSTK"]
                df_Futidx = df_web[['TIMESTAMP','SYMBOL','EXPIRY_DT','OPEN','HIGH','LOW','CLOSE','SETTLE_PR','CONTRACTS',
                'VAL_INLAKH','OPEN_INT','CHG_IN_OI','INSTRUMENT']].copy()[df_web['INSTRUMENT'].str.contains('FUT')]
                #df_Futidx.set_index("TIMESTAMP",inplace=True)
                return df_Futidx

def get_symbol():
    
    query = "SELECT [Id] as CompanyId,[Symbol] as SYMBOL FROM [dbo].[Company] (nolock)"
    df_comp = pd.read_sql(query,engine)
    return df_comp

def save_dataFrame(df_sql):
    df_sql.columns=['Date','Symbol','Expiry_Date','Open','High','Low','Close','Settle_Price','Contracts','ValueInLakh',
    'OpenInterest','ChangeInOI','InstrumentType','CompanyId']
    #print(df_sql)
    df_sql.to_sql("FutureDerivatives",engine, if_exists='append', index=False)

df = download_extract_zip("https://www1.nseindia.com/content/historical/DERIVATIVES/2020/MAY/fo08MAY2020bhav.csv.zip")
df_company = get_symbol()
df_merge =pd.merge(df,df_company,how="left",on="SYMBOL")
#print(df_merge.head(30))
save_dataFrame(df_merge)
