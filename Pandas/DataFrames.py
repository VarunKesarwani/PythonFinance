import numpy as np
import pandas as pd

from numpy.random import randn

print(np.random.seed(101))

#Create Df
df = pd.DataFrame(randn(5,4),['A','B','C','D','E'],['W','X','Y','Z'])
print(df)

#Get Column from DF
print(df['W'])#This is Standard
print(df.W)
print(type(df['W'])) #<class 'pandas.core.series.Series'>
print(type(df)) #<class 'pandas.core.frame.DataFrame'>

#Get multiple Column from DF
print(df[['W','Z']])# Pass list of column

#Create new column and column operation
df['New'] = df['W']+ df['Y']
print(df)

#Drop columns and Axis

#axis by default is 0 which denotes index of row, where as axis 1 denotes column
#this will not actually drop table. This will only drop on display
df.drop('New',axis = 1)
print(df)
# this will actually drop on table with parameter inplace = True
df.drop('New',axis = 1, inplace = True)
print(df)

#Drop rows
print(df.drop('E',axis = 0))#With out inplace
print(df)

#Axis 0 and Axis 1 comes from ref from Numpy. Df are index markers on top Numpy array.
print(df.shape)
# this will show Tuple of 5, 4; where 5 is no of rows and 4 is No of Col
# This is y axis 0 is referred as rows and 1 as c   ol

# Selecting Rows 
print(df.loc['C'])
print(df.iloc[2])

#Subset of table
print(df['W']['A'])
print(df.loc['C','Y'])
print(df.loc[['A','B'],['W','Y']])

#Conditional Selection
boolDf = df > 0
print(boolDf)
print(df[boolDf])#NaN is false
print(df[df>0])

#Subset conditional selection
print(df[df['W']> 0]) # will not get row C, meaning. df only get series value with True
print(df[df['Z']< 0])

res = df[df['W']> 0]
print(res['X'])

print(df[df['W']> 0]['Y']) #single steps
print(df[df['W']> 0][['Y','X']]) #single steps

#Multiple Condition
#use & instead of 'and'
print(df[(df['W']> 0) & (df['Y']> 1)]) #And
print(df[(df['W']> 0) | (df['Y']> 1)]) #OR

#Set and Reset index
print(df)
print(df.reset_index())#inplace = true for hard commit

newInd = 'UP TN AP HP RJ'.split() #creating list by splitting with ' '
print(newInd)
df['State'] = newInd #adding new col to df
print(df)

df.set_index('State') #This will update original index A,B,C,D,E; inplace = true for hard commit
print(df)

