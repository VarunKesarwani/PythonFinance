import requests
import datetime as dt
from io import StringIO
import pandas as pd

dt_date = dt.datetime.now().strftime('%m_%d_%Y')

url = 'https://www1.nseindia.com/products/content/sec_bhavdata_full.csv'

r = requests.get(url)
print(type(r.content))

s=str(r.content,'utf-8')

data = StringIO(s) 

df=pd.read_csv(data)
print(df.head())

#filename ='DB/'+ url.split('/')[-1] +'_'+dt_date

#with open(filename,'wb') as output_file:
    #output_file.write(r.content)


print('Download Completed!!!')