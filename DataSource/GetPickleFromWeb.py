import bs4 as bs
import pickle
import requests
import re
import os

symbol = 'HCLTECH'
filename = 'DB/fundamentalData_'+symbol+'.pickle'

def get_fundamental_Data():
    try:
        if not os.path.exists(filename):
            resp = requests.get('https://www.screener.in/company/'+symbol+'/consolidated/')
            soup = bs.BeautifulSoup(resp.text,"lxml")

            #Fundamenta Data
            section = soup.find('ul', {'class':'row-full-width'}).parent
            lst = section.find_next('ul').find_all('li', {'class':'four columns'})
            tickers = []
            for row in lst:
                key = str(re.sub('[^a-zA-Z0-9:%/.]+','',row.text)) 
                if '52weeks' in key:
                    key = key[ : 15] + ":" + key[15 : ] 
                tickers.append(key)
            
            #Sector Data
            section = soup.find("section", {'id':'peers'})
            smallText = section.findNext(name="small",attrs= {'class':'sub'}).text
            result = str(re.sub('[^a-zA-Z0-9-.://]+','',smallText)).split('//')
            tickers.append(result[0])
            tickers.append(result[1])

            #Pros and Cons
            section = soup.find("section", {'id':'analysis'})
            innerDiv = section.findNext(name="div",attrs= {'class':'row row-full-width'})
            pros = innerDiv.find(name="div",attrs= {'class':'six columns callout success'}).text
            tickers.append(pros)
            cons = innerDiv.find(name="div",attrs= {'class':'six columns callout warning'}).text
            tickers.append()

            with open(filename,"wb") as f:
                pickle.dump(tickers,f)
        else:
            print("file already exist")
    except Exception as e:
        print("Error: ",e)

get_fundamental_Data()
