import pickle
import pandas as pd
from sqlalchemy import create_engine
import re

symbol = 'ITC'
filename = 'DB/finology_data_'+symbol+'.pickle'

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}
engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])


def read_pickel():
    with open(filename,"rb") as f:
        data = pickle.load(f)
    new_row = []
    for row in data:
        if 'Add' not in row:
            list = str(row).replace('\n','').split(':')
            key = list[0].lstrip().replace('.','')
            Value = 'NaN'
            if len(list)>1:
                Value = str(re.sub('[^a-zA-Z0-9:%/.]+ ','',list[1])) 
                lst = [key,Value]
                new_row.append(lst)    
    df=pd.DataFrame(new_row,columns=['Key','Value']).T
    new_header = df.iloc[0] 
    df_sql = df[1:]
    df_sql.columns = new_header 
    print(df_sql.columns)
    df_sql.to_sql("FundamentalData",engine, if_exists='append', index=False)
       
read_pickel()