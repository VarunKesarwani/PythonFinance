import numpy as np
import Pandas as nypd

print(nypd.__version__)

labels = ['a','b','c']
my_list = [10,20,30]
arr = np.array([10,20,30])
d = {'a':10,'b':20,'c':30}

print(nypd.Series(data=my_list))

print(nypd.Series(data=my_list,index=labels))

print(nypd.Series(my_list,labels))

print(nypd.Series(arr))