import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

df_HCL = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'HCLTECH'", conn)
df_TATAELXSI = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'TATAELXSI'", conn)
df_WIPRO = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'WIPRO'", conn)
df_INFY = pd.read_sql("Select C.Symbol, D.* from CompanyDailyData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'INFY'", conn)

df_HCL.set_index('Date',inplace=True)
df_TATAELXSI.set_index('Date',inplace=True)
df_WIPRO.set_index('Date',inplace=True)
df_INFY.set_index('Date',inplace=True)

#Get only Adj Close of Stock
stocks = pd.concat([df_HCL['Adj Close'],df_INFY['Adj Close'],df_TATAELXSI['Adj Close'],df_WIPRO['Adj Close']],axis=1)
stocks.columns = ['HCL','Infy','TataElxsi','Wipro']

#log return of stocks
log_ret = np.log(stocks/stocks.shift(1))

print('Single Run for Some Random Allocation')
# Set seed (optional)
np.random.seed(101)

# Create Random Weights
print('Creating Random Weights')
weights = np.array(np.random.random(4))
print(weights)
print('\n')

# Rebalance Weights
print('Rebalance to sum to 1.0')
weights = weights / np.sum(weights)
print(weights)
print('\n')

# Expected Return
print('Expected Portfolio Return')
exp_ret = np.sum(log_ret.mean() * weights) *252
print(exp_ret)
print('\n')

# Expected Variance
print('Expected Volatility')
exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
print(exp_vol)
print('\n')

# Sharpe Ratio
SR = exp_ret/exp_vol
print('Sharpe Ratio')
print(SR)