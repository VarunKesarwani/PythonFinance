import numpy as np
import pandas as pd

outside = ['G1','G1','G1','G2','G2','G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside,inside))
print(hier_index) #Output [('G1', 1), ('G1', 2), ('G1', 3), ('G2', 1), ('G2', 2), ('G2', 3)]
hier_index = pd.MultiIndex.from_tuples(hier_index)
print(hier_index)

#index hiericy
df = pd.DataFrame(np.random.randn(6,2),index=hier_index,columns=['A','B'])
print(df)

print(df.loc['G1'])
#we call outside index n then keeping digging inside index.
print(df.loc['G1'].iloc[1])
print(df.loc['G1'].iloc[2]['B'])


#index name
df.index.names = ['Groups','Num']
print(df)

#Cross section
print(df.xs(1,level='Num'))
