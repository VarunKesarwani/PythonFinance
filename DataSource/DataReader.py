import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(2018,1,1)
end = dt.datetime(2020,1,1)

facebook = web.DataReader('FB','yahoo',start,end)
print(facebook.head())