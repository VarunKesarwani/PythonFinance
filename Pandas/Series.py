import numpy as np
import pandas as pd

labels = ['a','b','c']
my_list = [10,20,30]
arr = np.array([10,20,30])
d = {'a':10,'b':20,'c':100}

print(pd.Series(data=my_list))
print(pd.Series(data=my_list,index=labels))
print(pd.Series(my_list,labels))

print(pd.Series(arr))

print(pd.Series(d))

print(pd.Series(data=labels))

ser1 = pd.Series([1,2,3,4],index=['India','Japan','Canada','Germany'])
print(ser1)
print(ser1['India'])

ser2 = pd.Series([1,2,3,4],index=['India','Japan','Singapore','USA'])
print(ser2)

print(ser1+ser2)#adds only countries that match
