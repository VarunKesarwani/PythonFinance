import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
import PortfolioAllocation as pa


#Total Portfolio Value
portfolio_val = pa.Total_Pos_Val(isPlot=False)

#dail return
def dail_return(isPlot = False):
    portfolio_val['Daily Return'] = portfolio_val['Total Pos'].pct_change(1)
    portfolio_val['Cumulative Return'] = (1 + portfolio_val['Daily Return']).cumprod()
    if(isPlot == True):
        print(portfolio_val.head())
        portfolio_val['Daily Return'].plot(kind='kde')
    return portfolio_val

#Cumulative Return
def cummulative_return():
    cum_ret = 100 * (portfolio_val['Total Pos'][-1]/portfolio_val['Total Pos'][0] -1 )
    print('Our return was {}% !'.format(cum_ret))

#Avg Daily Return
def avg_dail_return():
    ret = portfolio_val['Daily Return'].mean()
    print('Avg Dail Return = {}'.format(ret))

#Std Daily Return
def std_dail_return():
    ret= portfolio_val['Daily Return'].std()
    print('Std Dail Return = {}'.format(ret))

if __name__ == '__main__':
    dail_return(isPlot = True)
    #cummulative_return()
    plt.show()