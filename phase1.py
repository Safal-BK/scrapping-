import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import os
from datetime import datetime
from tqdm import tqdm
from time import sleep
import requests
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError



#set the amount 
breakcount=5000
now = datetime.now() # current date and time
print("time : ",now.strftime("%H:%M:%S"))
datesData = []

patentList_data = []

#get source code of url 
def get_response(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    # print(r.status,r.data)
    response = BeautifulSoup(response.data, 'html.parser')
    return response


# print(get_response('https://data.epo.org/publication-server/rest/v1.2/patents/EP4115404NWA1/document.xml'))

#-------------------------------main---------------------------------------------

# phase 1 get petents numbers
print("...dates collecting in range")

url = 'https://data.epo.org/publication-server/rest/v1.2/publication-dates' 
try:
    respDates_soup =get_response(url)
except:
    print("network error")
publishedDates = respDates_soup.find_all("a")
count=0
for item in publishedDates:

    date = item.get_text()
    link = r"https://data.epo.org"+item.get('href')
    datesData.append([date,link])
    datesData_df=pd.DataFrame(datesData,columns = ['Date','Link'])
    datesData_df['Date']=pd.to_datetime(datesData_df['Date'])
    datesData_df = datesData_df[datesData_df['Date']>'01/12/2021']
    count=count+1
    #break count
    if(count==breakcount):
        pass
print("completed...")


# pahse 2 create table with patent data, number, UID 
print("collecting patents in each date ")

for idx,row in datesData_df.iterrows():
    date = datetime.strptime(str(row['Date']), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
    link = row['Link']
    try:
        patents  = get_response(link)
        patentsList = patents.find_all("a")
        for item in patentsList:
            # print(item)
            patentList_data.append([date, item.get_text(),r"https://data.epo.org"+item.get('href')])
        print("     ",(idx+1)," / ",datesData_df.shape[0]," completed...")
    # except:
    #     print("network error")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
    sleep(0.3)
    if(idx==breakcount):
        break
print("completed...")

patentList_df = pd.DataFrame(patentList_data,columns=['Publish_Date','Patent_Number','Link'])  
patentList_df['UID'] = patentList_df['Patent_Number']+'_'+patentList_df['Publish_Date']



for idx,row in patentList_df.iterrows():
    patentNumber = row['Patent_Number']
    xmllink = 'https://data.epo.org/publication-server/rest/v1.2/patents/%s/document.xml'%patentNumber
    patentList_df.loc[idx,'xml_link'] = xmllink


print("saving table 1 as database....")
import sqlite3
con = sqlite3.connect("database/patent_list_db.sqlite")
patentList_df.to_sql("PatentXmlTable", con, if_exists="replace")
con.close()
print("saved....")

