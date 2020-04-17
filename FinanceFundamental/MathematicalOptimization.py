import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=.\SQLEXPRESS;'
                      'Database=ShareData;'
                      'UID=sa; PWD=varun@17;')

df_HCL = pd.read_sql("Select C.Symbol, D.* from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'HCLTECH'", conn)
df_TATAELXSI = pd.read_sql("Select C.Symbol, D.* from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'TATAELXSI'", conn)
df_WIPRO = pd.read_sql("Select C.Symbol, D.* from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'WIPRO'", conn)
df_INFY = pd.read_sql("Select C.Symbol, D.* from CompanyDailyPriceData D(nolock) inner join Company C(nolock) on D.CompanyId = C.Id  where C.Symbol = 'INFY'", conn)

df_HCL.set_index('Date',inplace=True)
df_TATAELXSI.set_index('Date',inplace=True)
df_WIPRO.set_index('Date',inplace=True)
df_INFY.set_index('Date',inplace=True)



stocks = pd.concat([df_HCL['Adj Close'],df_INFY['Adj Close'],df_TATAELXSI['Adj Close'],df_WIPRO['Adj Close']],axis=1)
stocks.columns = ['HCL','Infy','TataElxsi','Wipro']

#log return of stocks
log_ret = np.log(stocks/stocks.shift(1))

np.random.seed(101)
num_ports = 5000

#Craete Empty Array to Hold values.
all_weights = np.zeros((num_ports,len(stocks.columns)))
ret_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for ind in range(num_ports):
    weights = np.array(np.random.random(4))
    weights = weights / np.sum(weights)
    all_weights[ind,:] = weights
    ret_arr[ind] = np.sum((log_ret.mean() * weights) *252)
    vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

def get_ret_vol_sr(weights):
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    sr = ret/vol
    return np.array([ret,vol,sr])

#since we actually want to maximize the Sharpe Ratio, 
#we will need to turn it negative so we can minimize the negative sharpe
def neg_sharpe(weights):
    return  get_ret_vol_sr(weights)[2] * -1

# Contraints
#check if all weights add up to 1
def check_sum(weights):
    '''
    Returns 0 if sum of weights is 1.0
    '''
    return np.sum(weights) - 1

# By convention of minimize function it should be a function that returns zero for conditions
cons = ({'type':'eq','fun': check_sum})

# 0-1 bounds for each weight, weight cannot be greater the 1
bounds = ((0, 1), (0, 1), (0, 1), (0, 1))

# Initial Guess for weight(equal distribution)
init_guess = [0.25,0.25,0.25,0.25]

# Sequential Least SQuares Programming (SLSQP) also.
opt_results = minimize(neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)

print(opt_results)

#most optimised allocation
alloc = get_ret_vol_sr(opt_results.x)
print('Most optimised allocation: {}'.format(alloc))

#All Optimal Portfolios (Efficient Frontier)
#expected return out of desired volatility
# Random allocation graph we notice Our returns go from 0 to somewhere along 0.15 (y axis)
# Create a linspace number of points to calculate x on
frontier_y = np.linspace(0,0.15,50)

def minimize_volatility(weights):
    return  get_ret_vol_sr(weights)[1] 

frontier_volatility = []

for possible_return in frontier_y:
    cons = ({'type':'eq','fun': check_sum},
            {'type':'eq','fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})
    
    result = minimize(minimize_volatility,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
    
    frontier_volatility.append(result['fun'])

plt.figure(figsize=(12,8))
plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')



# Add frontier line
plt.plot(frontier_volatility,frontier_y,'g--',linewidth=3)

plt.show()