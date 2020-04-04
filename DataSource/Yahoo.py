import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(2018,1,1)
end = dt.datetime(2020,1,1)

hcl = web.DataReader('HCLTECH.NS','yahoo',start,end)
print(hcl.head())