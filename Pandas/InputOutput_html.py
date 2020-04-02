import pandas as pd

df = pd.read_html('https://www.moneyworks4me.com/best-index/nse-stocks/top-nifty50-companies-list/')
print(df[0].head())#heads get first 5 records only