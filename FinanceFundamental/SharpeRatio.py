import PortfolioStatics as ps


portfolio_val = ps.dail_return(isPlot=False)


#Sharpe Ratio
SR = portfolio_val['Daily Return'].mean()/portfolio_val['Daily Return'].std()
print('Sharpe Ratio = {}'.format(SR))

#Anual Sharpe ratio
ASR = (252**0.12)*SR
print('Annual Sharpe Ratio = {}'.format(ASR))

ps.std_dail_return()