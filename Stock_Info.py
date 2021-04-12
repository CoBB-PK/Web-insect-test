import requests , json , jsonpath , csv , pymysql
from bs4 import BeautifulSoup


conn = pymysql.connect(
  host = "127.0.0.1",
  user = "root",
  password = "Pokai-Liou-0988181272",
  database="Stock_db"
)

cursor = conn.cursor()

#主要main
data = {}  

A = 0
for i in range(0,28):
    URL = 'https://www.cnyes.com/twstock/stock_astock.aspx?ga=nav'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text , 'html.parser')
    page_title = soup.select('div#kinditem_0 li')[i].text
    page_url = soup.select('div#kinditem_0 a')[i]['href']
    URL = "https://www.cnyes.com/twstock/"+page_url
    print(page_title + "產業")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text , 'html.parser')
    try:
        for x in range(0,55000):
            if x % 11 == 1  :
                page_ID = soup.select('div.TableBox td')[x]
                Name = soup.select('div.TableBox td')[x+1].text
                URL_Stock = page_ID.text
                URL = "https://marketinfo.api.cnyes.com/mi/api/v1/TWS:" + URL_Stock + ":STOCK/info"
                response = requests.get(URL)
                Info = json.loads(response.text)

                ID = Info["data"]["symbolId"]
                companyName = Info["data"]["companyName"]
                Type = Info["data"]["industryType"]
                description = Info["data"]["description"]
                stockType = Info["data"]["stockType"]
                foreignStockOwnRatio = Info["data"]["foreignStockOwnRatio"]
                listingDateS = Info["data"]["listingDateS"]
                conferenceContentCH = Info["data"]["conferenceContentCH"]
                cursor.execute("INSERT INTO stock_info(ID,Name,CompanyName,Type,description,industryType,listingDateS,foreignStockOwnRatio,conferenceContentCH)VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(ID,Name,companyName,Type,description,stockType,listingDateS,foreignStockOwnRatio,conferenceContentCH))

                #data[Info["data"]["symbolId"]]={"ID":Info["data"]["symbolId"],'Name':Info["data"]["companyName"] ,'description': Info["data"]["description"],'conferenceContentCH': Info["data"]["conferenceContentCH"],'foreignStockOwnRatio':Info["data"]["foreignStockOwnRatio"]}
                conn.commit() 
                    #data['Stock_Info'].append({Info["data"]["symbolId"]:[x]}
                        #"ID":Info["data"]["symbolId"],
                        #'Name':Info["data"]["companyName"] ,
                        #'description': Info["data"]["description"],
                        #'conferenceContentCH': Info["data"]["conferenceContentCH"],
                        #'foreignStockOwnRatio':Info["data"]["foreignStockOwnRatio"]
                    #)
                A += 1
    except:
        print("")
print(" 共 : %d 筆" %(A))

cursor.close() 
conn.close()


with open('Stock_Info.json', 'w',encoding='utf-8') as outfile:  
    json.dump(data, outfile,ensure_ascii=False,indent=3)
