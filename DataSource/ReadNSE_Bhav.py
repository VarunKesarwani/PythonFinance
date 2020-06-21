import pandas as pd
import pandas_datareader.data as web
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import io
import zipfile
from datetime import datetime, timedelta
from time import sleep
#import datetime as dt
import math

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

def get_symbol():
    query = "SELECT [Id] as CompanyId,[Symbol] as SYMBOL,[Symbol] as Symbol FROM [dbo].[Company] (nolock) Where IsActive = 1"
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

def nse_company_details_save(df_web):
    for row in df_web.iterrows():
        result = row[1]
        symbol = str(result.get(key = 'SYMBOL'))
        getSymbolQuery = "SELECT * FROM [dbo].[Company] (nolock) where Symbol = '{}'".format(symbol)
        df_comp = pd.read_sql(getSymbolQuery,engine)
        if df_comp.empty:
            CompanyName = str(result.get(key = 'NAME_OF_COMPANY'))
            Series = str(result.get(key = 'SERIES'))
            DateOfListing = str(result.get(key = 'DATE_OF_LISTING'))
            #FaceValue = str(result.get(key = 'FACE_VALUE'))
            insertSymbolQuery="INSERT INTO [dbo].[Company] ([Symbol],[CompanyName],[Series],[DateOfListing]) VALUES('{}','{}','{}','{}')".format(symbol,CompanyName,Series,DateOfListing)
            with engine.connect() as con:
                con.execute(insertSymbolQuery)
        else:
            updateCompanyActive = "update Company Set IsActive = 1 where Symbol = '{}'".format(symbol)
            with engine.connect() as con:
                con.execute(updateCompanyActive)
            #print(symbol+' already Found')

def nse_company_details_get():
    df_web = pd.read_csv('https://www1.nseindia.com/content/equities/EQUITY_L.csv')
    df_web.columns=['SYMBOL','NAME_OF_COMPANY','SERIES','DATE_OF_LISTING','PAID_UP_VALUE','MARKET_LOT','ISIN NUMBER','FACE_VALUE']
    updateCompanyActive = "update Company Set IsActive = 0"
    with engine.connect() as con:
        con.execute(updateCompanyActive)
    nse_company_details_save(df_web)

def get_companyDetails():
    query = 'SELECT [Id],[Symbol],[CompanyName] FROM [dbo].[Company](nolock)'
    df = pd.read_sql(query, engine)
    table = pd.read_html('https://www.samco.in/knowledge-center/articles/nse-listed-companies/')
    df_Web = table[0]
    df_Web['CompanyName'] = table[0]['NAME OF COMPANY']
    pd_Merge = pd.merge(df_Web,df,on=['CompanyName'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute('''TRUNCATE TABLE [dbo].[CompanyDetails]''')
    session.commit()
    session.close()
    save_companyDetails(pd_Merge)

def save_companyDetails(df_web):
    for row in df_web.iterrows():
        result = row[1]
        CompanyId = result.get(key = 'Id')
        CompanyName = str(result.get(key = 'CompanyName'))
        faceValue = result.get(key = 'FACE VALUE') if result.get(key = 'FACE VALUE') is not None and not math.isnan(result.get(key = 'FACE VALUE')) else 0
        marketCap = result.get(key = 'Market Cap') if result.get(key = 'Market Cap') is not None and not math.isnan(result.get(key = 'Market Cap'))  else 0
        EPS = str(result.get(key = 'EPS')) if result.get(key = 'EPS') is not None and not math.isnan(result.get(key = 'EPS')) else 0
        PE = result.get(key = 'PE') if result.get(key = 'PE') is not None and not math.isnan(result.get(key = 'PE')) else 0
        Shares_Issued = result.get(key = 'Shares Issued') if result.get(key = 'Shares Issued') is not None and not math.isnan(result.get(key = 'Shares Issued')) else 0
        insetSamcoData = "INSERT INTO [dbo].[CompanyDetails]([CompanyId],[CompanyName],[FaceValue],[MarketCap],[EPS],[PE],[SharedIssued])VALUES({},'{}',{},{},{},{},{})".format(CompanyId,CompanyName,faceValue,marketCap,EPS,PE,Shares_Issued )
        with engine.connect() as con:
            con.execute(insetSamcoData)

def GetData(value,currentDate):
        str_Start = currentDate - timedelta(days=1)
        str_end = currentDate
        return web.DataReader(value,'yahoo',str_Start,str_end)

def InsertData(data):
        data.to_sql(name='CompanyDailyPriceData', con=engine, if_exists = 'append', index=False)

def get_yahooData(currentDate):
    df_comp = get_symbol()
    for row_index,row in df_comp[['CompanyId','Symbol']].iterrows():
        try:
            df = GetData(row['Symbol'],currentDate)
            df['CompanyId'] = row_index
            df['Date'] = df.index 

            InsertData(df)
            print(row['Symbol'])
            sleep(1)
        except Exception as e:
            print('error',e)

def getIndexData(tradingDate):
    current_year = str(tradingDate.year)
    month_Name= str(tradingDate.strftime("%m")).upper()
    dateName = str(tradingDate.strftime("%d"))
    fileName = "ind_close_all_"+dateName+month_Name+current_year+".csv"

    getIndexMasterDateQuery = "SELECT [ID],[IndexName],[IndexNameOnReport] as [IndexName],[IndexType] FROM [dbo].[IndexDetails]"
    df_comp = pd.read_sql(getIndexMasterDateQuery,engine)

    Url="http://niftyindices.com/Daily_Snapshot/{}".format(fileName)
    print(Url)
    response = requests.get(Url)

    df_web = pd.read_csv(response)
    df_web.columns = ['IndexName','Date','Open','High','Low','Close','PointsChange','PercentChange','Volume','TurnoverInCr','PE','PB','DivYield']
    
    df_merge = pd.merge(df_web,df_comp,on=['IndexName'])
    #df_merge['Date'] = pd.to_datetime(df_merge['Date'])
    df_merge.to_sql("IndexDailySnapshortReport",engine, if_exists='append', index=False)
    print('Future value inserted successfully')
    
    

#refresh company list
nse_company_details_get()

#refresh company detail list
get_companyDetails()

#save todays BhavanaCopy
df_bhavacopy = download_bhava_copy()
print(df_bhavacopy)

#save todays FUT price copy
download_derivative_extract_zip(df_bhavacopy)

#get_yahooData(df_bhavacopy)

#get index data csv
#getIndexData(df_bhavacopy)

print('Process Completed!!!')






#filename ='DB/'+ url.split('/')[-1] +'_'+dt_date

#with open(filename,'wb') as output_file:
    #output_file.write(r.content)