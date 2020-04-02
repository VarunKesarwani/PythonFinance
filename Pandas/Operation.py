import pandas as pd

df = pd.DataFrame({'col1':[1,2,3,4],'col2':[444,555,666,444],'col3':['abc','def','ghi','wxyz']})
print(df.head())

print(df['col2'].unique())

print(df['col2'].nunique())#count of unique value
#Output: 3

print(df['col2'].value_counts())#count of value in col
#Output
#   444    2
#   555    1
#   666    1

#Apply
print('Apply')
def time2(x):
    return x*2
#customer function
res = df['col1'].apply(time2)
print(res)
#built in function
print(df['col3'].apply(len))
#lamda expression
print(df['col1'].apply(lambda x: x*2))

#DF attributes
print('')
print(df.columns)
print(df.index)

#Sorting and ordering
print(df.sort_values(by='col2',axis=0))

#find null
print(df.isnull())
