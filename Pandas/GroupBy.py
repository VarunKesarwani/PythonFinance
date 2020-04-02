import numpy as np
import pandas as pd

data = {'Company':['GOOG','GOOG','MSFT','MSFT','FB','FB'],
       'Person':['Sam','Charlie','Amy','Vanessa','Carl','Sarah'],
       'Sales':[200,120,340,124,243,350]}

df = pd.DataFrame(data)
print(df)

#GroupBy Column Company
by_comp = df.groupby('Company')
#this will only consider column with numeric value
print(by_comp.mean())
print(by_comp.sum())
print(by_comp.std())
print('')
print(by_comp.sum().loc['FB'])
print('')
by_comp1 = df.groupby('Company').sum().loc['FB']
print(by_comp1)
print('')
print(by_comp.count())
print('')
print(by_comp.max())
print('')
print(by_comp.min())
print('')
print(by_comp.describe())
print('')
print(by_comp.describe().transpose())
