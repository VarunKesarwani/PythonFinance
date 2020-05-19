import pandas as pd
from sqlalchemy import create_engine
import csv
import urllib.request

DB = {'servername': '.\SQLEXPRESS', 'database': 'ShareData', 'driver': 'driver=SQL Server Native Client 11.0'}

engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

query ="Select ID,IndexName,IndexFileURL,IndexType from IndexDetails where IndexFileURL is not null"

df_index = pd.read_sql(query,engine)

for row in df_index.itertuples():
    print(row.IndexFileURL)
    #df_web = pd.read_csv(row.IndexFileURL)
    #df_web["IndexId"] = row.ID
    #df_web.columns=['IndexId','CompanyName','Industry','Symbol','Series']
    #print(df_web)

print('Download Start!!!')
url = "http://niftyindices.com/IndexConstituent/ind_niftynext50list.csv"
response = urllib.request.urlopen(url)
cr = csv.reader(response)

for row in cr:
    print(row)








