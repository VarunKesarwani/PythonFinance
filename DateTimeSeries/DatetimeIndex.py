import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

first_two = [datetime(2016, 1, 1), datetime(2016, 1, 2)]

print(first_two)

dt_ind = pd.DatetimeIndex(first_two)
print(dt_ind)

data = np.random.randn(2,2)
print(data)
cols = ['A','B']

df = pd.DataFrame(data,dt_ind,cols)
print(df)

#Index
print(df.index)
print(df.index.argmax())
print(df.index.max())