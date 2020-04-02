import numpy as np
import pandas as pd

d = {'A':[1,2,np.nan],'B':[5,np.nan,np.nan],'C':[6,7,8]}
df= pd.DataFrame(d)
print(df)

#dropna
#dataframe will drop rows if it has null value.
#row 1 and 2 wil be dropped as they have Nan value; axis parameter is 0 which is default
print(df.dropna())

#To perform this on column, specific axis parameter to 1
print(df.dropna(axis=1))

#we can also set treshold value when ro drop row or col.
#for example we want to drop only when row or col has more the 2 nan value
print(df.dropna(axis=0,thresh=2))

#Fill Nan
print(df.fillna(value='Fill'))

#mean of value
print(df.fillna(value=df['A'].mean()))