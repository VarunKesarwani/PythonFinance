import pandas as pd

data = {'A':['foo','foo','foo','bar','bar','bar'],
     'B':['one','one','two','two','one','one'],
       'C':['x','y','x','y','x','y'],
       'D':[1,3,2,5,4,1]}

df = pd.DataFrame(data)
print(df)
print('')
print('pivot')
print('')
pv = df.pivot_table(values='D',index=['A', 'B'],columns=['C'])
print(pv)