import bs4 as bs
import pickle
import requests
import os
import pandas as pd

symbol = 'ITC'
filename = 'DB/finology_fundamental_'+symbol+'.pickle'

def read_pickel():
    with open(filename,"rb") as f:
        data = pickle.load(f)
    new_row = []
    for row in data:
        list = str(row).replace('\n','').split(':')
        key = list[0]
        Value = 'NaN'
        if len(list)>1:
            Value = list[1]
            lst = [key,Value]
            new_row.append(lst)    
    df=pd.DataFrame(new_row,columns=['Key','Value'])
    print(df)
read_pickel()