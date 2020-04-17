import bs4 as bs
import pickle
import requests
import re
import os

symbol = 'ITC'
filename = 'DB/finology_data_'+symbol+'.pickle'

def get_fundamental_Data():
    try:
        if not os.path.exists(filename):
            resp = requests.get('https://ticker.finology.in/company/'+symbol+'?mode=C')
            soup = bs.BeautifulSoup(resp.text,"lxml")
            tickers = []
            #Fundamenta Data
            section1 = soup.find('div', {'id':'compheader'})
            section2 = soup.find('div', {'class':'card cardscreen'})
            section3 = soup.find('div', {'id':'mainContent_ProsAndCons'})

            sector = section1.findNext(name='p',attrs={"id":"mainContent_compinfoId"}).text

            sector_list = str(sector).split()
            sector_str = " ".join(sector_list)
            YearlyHigh = section1.findNext(name="span",attrs={"id":"mainContent_ltrl52WH"}).text
            YearlyLow = section1.findNext(name="span",attrs={"id":"mainContent_ltrl52WL"}).text

            tickers.append('52 Week High:'+YearlyHigh)
            tickers.append('52 Week Low:'+YearlyLow)
            tickers.append(sector_str)

            #statements = section1.findNext(name="div",attrs={"class":"card cardscreen cardblue"})
            #statements2 = section1.findNext(name="div",attrs={"class":"row no-gutters mt-5 ratingdetails"})
            
            ratios = section2.findNext(name='div', attrs= {'id':'mainContent_updAddRatios'})
            pros_cons = section3.findAll(name="div", attrs={"class":"col-12 col-md-6"})
            #print(pros_cons)

            # for row in statements2.findAll(name="div"):
            #     key_lst = str(row.findNext(name="h6").text).split()
            #     key = " ".join(key_lst)
            #     value_lst = str(row.findNext(name="span").text).split()
            #     value = " ".join(value_lst)
            #     print(key+':'+value)
            for div in ratios.findAll("div"):
                key_lst = str(div.findNext(name="small").text).split()
                key = " ".join(key_lst)
                value_lst = str(div.findNext(name="p").text).split()
                value= " ".join(value_lst)
                tickers.append(key+":"+value)
            
            for item in pros_cons:                
                key = item.findNext("h4").get_text()
                lst = item.find_next('ul').find_all('li')
                value = ''
                for li in lst:
                    value = value+li.text+"|"
                tickers.append(key+":"+value)

            with open(filename,"wb") as f:
                pickle.dump(tickers,f)
            
            print('Completed')
            
        else:
            print("file already exist")
    except Exception as e:
        print("Error: ",e)

get_fundamental_Data()
