from datetime import date
import pandas as pd
from nsepy import get_history
from nsepy import get_history
from nsepy.history import get_price_list
from nsepy import get_index_pe_history  
from nsepy.derivatives import get_expiry_date
from sqlalchemy import create_engine
from datetime import datetime
from dateutil.relativedelta import relativedelta


DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

def get_symbol():
    query = "SELECT [Id] as CompanyId,[Symbol] as Symbol FROM [dbo].[Company] (nolock) Where IsActive = 1 and Symbol in('TCS')"
    df_comp = pd.read_sql(query,engine)
    return df_comp

def get_index():
    query = "Select top 1 ID as IndexId, IndexName,IndexNameOnReport from IndexDetails"
    df_index = pd.read_sql(query,engine)
    return df_index

def InsertData(data):
    data.to_sql(name='CompanyDailyPriceData', con=engine, if_exists = 'append', index=True)
    print('Data inserted!!')

def getIndexPrice():
    df_index = get_index()
    for row in df_index[['IndexId','IndexName']].iterrows():
        try:
            result = row[1]
            index_id = int(result.get(key = 'IndexId'))
            index_name = str(result.get(key = 'IndexName'))
            startDt = datetime.now().date()- relativedelta(months=1)
            endDt = datetime.today().date() 
            print(index_id,index_name,startDt,endDt)
            df_web = get_history(symbol=index_name,
                                start=date(startDt.year,startDt.month,startDt.day),
                                end=date(endDt.year,endDt.month,endDt.day),
                                index=True)
            df_web["IndexId"] = index_id
            print(df_web.head())
        except Exception as e:
            print('error',e)


def getHistoryPrice():
    df_comp = get_symbol()
    for row in df_comp[['CompanyId','Symbol']].iterrows():
        try:
            result = row[1]
            symbol_name = str(result.get(key = 'Symbol'))
            startDt = datetime.now().date()- relativedelta(years=1)
            endDt = datetime.today().date() 
            df_prices = get_history(symbol=symbol_name,start=date(startDt.year,startDt.month,startDt.day),end=date(endDt.year,endDt.month,endDt.day))
            df_prices['CompanyId'] = int(result.get(key = 'CompanyId'))
            df_prices_new = df_prices[['CompanyId','Open','High','Low','Close','Volume','Last']].copy()
            df_prices_new.columns=['CompanyId','Open','High','Low','Close','Volume','Adj Close']
            InsertData(df_prices_new)
        except Exception as e:
            print('error',e)

def getDerivativeHistoryPrice():
    df_comp = get_symbol()
    for row in df_comp[['CompanyId','Symbol']].iterrows():
        try:
            result = row[1]
            symbol_name = str(result.get(key = 'Symbol'))
            company_id = int(result.get(key = 'CompanyId'))

            endDt = datetime.now().date() 

            previousExipry = max(get_expiry_date(year=endDt.year, month=(endDt.month-1)))
            currentExpiry = max(get_expiry_date(year=endDt.year, month=endDt.month))

            print(company_id,symbol_name,endDt,previousExipry,currentExpiry)
            
            df_prices = get_history(symbol='TCS',
                                    start=date(previousExipry.year,previousExipry.month,(previousExipry.day+1)),
                                    end=date(endDt.year,endDt.month,endDt.month),
                                    futures=True,
                                    expiry_date=date(currentExpiry.year,currentExpiry.month,currentExpiry.day))
            df_prices['CompanyId'] = company_id
            print(df_prices.head())
        except Exception as e:
            print('error',e)
      

getHistoryPrice()
#
#getIndexPrice()
#getDerivativeHistoryPrice()
'''

# Stock options (Similarly for index options, set index = True)
stock_fut = get_history(symbol="SBIN",
                        start=date(2015,1,1),
                        end=date(2015,1,10),
                        futures=True,
                        expiry_date=date(2015,1,29))
print(stock_fut.head())

# NIFTY Next 50 index
nifty_next50 = get_history(symbol="NIFTY NEXT 50",
                            start=date(2015,1,1),
                            end=date(2015,1,10),
                            index=True)
# NIFTY50 Equal wight index (random index from the list)
nifty_eq_wt = get_history(symbol="NIFTY50 EQUAL WEIGHT",
                            start=date(2017,6,1),
                            end=date(2017,6,10),
                            index=True)
#Index futures price history
nifty_fut = get_history(symbol="NIFTY",
                        start=date(2015,1,1),
                        end=date(2015,1,10),
                        index=True,
                        futures=True,
                        expiry_date=date(2015,1,29))
# Index P/E Ratio History
nifty_pe = get_index_pe_history(symbol="NIFTY",
                                start=date(2015,1,1),
                                end=date(2015,1,10))
# Fetching Expiry Dates
expiry = get_expiry_date(year=2015, month=1)

# Use Expiry Dates function with get_history
stock_fut_exp = get_history(symbol="SBIN",
                            start=date(2015,1,1),
                            end=date(2015,1,10),
                            futures=True,
                            expiry_date=get_expiry_date(2015,1))

# Daily Bhav Copy
prices = get_price_list(dt=date(2015,1,1))

'''
