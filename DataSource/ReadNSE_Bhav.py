import pandas as pd
from sqlalchemy import create_engine
import requests
import io
import zipfile
from datetime import date

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

def get_symbol():
    query = "SELECT [Id] as CompanyId,[Symbol] as SYMBOL,[Symbol] as Symbol FROM [dbo].[Company] (nolock)"
    df_comp = pd.read_sql(query,engine)
    return df_comp

def save_Futidx_dataFrame(df_sql):
    query_validate = "select top 1 1 from FutureDerivatives (nolock) where [Date]= '{}'".format(df_sql['TIMESTAMP'][1])
    value = pd.read_sql(query_validate,engine)

    if value.empty:
        df_sql.columns=['Date','Symbol','Expiry_Date','Open','High','Low','Close','Settle_Price','Contracts','ValueInLakh','OpenInterest','ChangeInOI','InstrumentType','CompanyId']
        df_sql.to_sql("FutureDerivatives",engine, if_exists='append', index=False)
        print('Future value inserted successfully')
    else:
        print('Future value already inserted')

def save_bhacancopy_dataFrame(df_merge):
    query_validate = "select top 1 1 from CompanyDailyBhavData (nolock) where [Date]= '{}'".format(df_merge['Date'][1])
    value = pd.read_sql(query_validate,engine)

    if value.empty:
        df_merge.columns = ['CompanyId','Date','Prev_Close','Open_Price','High_Price','LowPrice','Last_Price','Close_Price','Avg_Price','Volume','TradedValue','NumOfTrades','DeliveryQuantity','DeliveryPercentage']
        #df_sql = df_merge[['CompanyId','Date','Prev_Close','Open_Price','High_Price','LowPrice','Last_Price','Close_Price','Avg_Price','Volume','TradedValue','NumOfTrades','DeliveryQuantity','DeliveryPercentage']].copy()
        df_merge.to_sql("CompanyDailyBhavData",engine, if_exists='append', index=False)
        print('Bhava Copy inserted successfully')
    else:
        print('Bhava Copy already inserted')

def download_bhava_copy():
    df_web = pd.read_csv('https://www1.nseindia.com/products/content/sec_bhavdata_full.csv')
    df_web.columns=['Symbol','Series','Date','Prev_Close','Open_Price','High_Price','LowPrice','Last_Price','Close_Price','Avg_Price','Volume','TradedValue','NumOfTrades','DeliveryQuantity','DeliveryPercentage']
    df_comp = get_symbol()
    df_merge = pd.merge(df_web,df_comp,on='Symbol')
    df_merge['Date'] = pd.to_datetime(df_merge['Date'])
    df_merge.drop('SYMBOL',axis=1,inplace=True)
    print(df_merge.head(2))
    save_bhacancopy_dataFrame(df_merge)
    return df_merge['Date'][1]

def download_derivative_extract_zip(tradingDate):
    current_year = str(tradingDate.year)
    month_Name= str(tradingDate.strftime("%b")).upper()
    dateName = str(tradingDate.strftime("%d"))
    fileName = "fo"+dateName+month_Name+current_year+"bhav.csv.zip"

    url = "https://www1.nseindia.com/content/historical/DERIVATIVES/{}/{}/{}".format(current_year,month_Name,fileName)
    #print(url)
    #url = "https://www1.nseindia.com/content/historical/DERIVATIVES/2020/JUN/fo20JUN2020bhav.csv.zip"
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                #print(zipinfo)
                with thezip.open(zipinfo) as thefile:
                    #print(zipinfo.filename, thefile.read())
                    df_web = pd.read_csv(thefile)
                    df_Futidx = df_web[['TIMESTAMP','SYMBOL','EXPIRY_DT','OPEN','HIGH','LOW','CLOSE',
                    'SETTLE_PR','CONTRACTS','VAL_INLAKH','OPEN_INT','CHG_IN_OI',
                    'INSTRUMENT']].copy()[df_web['INSTRUMENT'].str.contains('FUT')]
                    df_comp = get_symbol()
                    df_merge =pd.merge(df_Futidx,df_comp,how="left",on="SYMBOL")
                    df_merge.drop('Symbol',axis=1,inplace=True)
                    print(df_merge.head(2))
                    save_Futidx_dataFrame(df_merge)
    else:
        print("File not found")


df_bhavacopy = download_bhava_copy()
print(df_bhavacopy)

download_derivative_extract_zip(df_bhavacopy)


print('Download Completed!!!')






#filename ='DB/'+ url.split('/')[-1] +'_'+dt_date

#with open(filename,'wb') as output_file:
    #output_file.write(r.content)