import numpy as np
import pandas as pd

#import openpyxl

df = pd.read_excel(r'D:\ShareData\TCS_xls.xlsx',sheet_name='TCS')
print(df)

df.to_excel('TCS1.xlsx',sheet_name='TCS')

