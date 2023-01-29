import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import os
from datetime import datetime
from tqdm import tqdm
from time import sleep

readPatentBoxdates= True
xmlPath = r'/data/workspace_files/xml'
csvPath = r'/data/workspace_files/csv'
if readPatentBoxdates:
    patentList_data = []
    datesData = []
    url = 'https://data.epo.org/publication-server/rest/v1.2/publication-dates' 
    # respDates = urllib3.request.urlopen(url)

    http = urllib3.PoolManager()
    url = 'https://data.epo.org/publication-server/rest/v1.2/publication-dates' 
    respDates = http.request('GET', url)
    respDates_soup = BeautifulSoup(respDates, 'html.parser')
    publishedDates = respDates_soup.find_all("a")
    
   

    for item in publishedDates:
        date = item.get_text()
        link = r"https://data.epo.org"+item.get('href')
        datesData.append([date,link])
        datesData_df=pd.DataFrame(datesData,columns = ['Date','Link'])
        datesData_df['Date']=pd.to_datetime(datesData_df['Date'])
        datesData_df = datesData_df[datesData_df['Date']>'01/01/2021']

    for idx,row in datesData_df.iterrows():
        date = row['Date']
        link = row['Link']
        resp = urllib3.request.urlopen(link)
        patents  = BeautifulSoup(resp, 'html.parser')
        patentsList = patents.find_all("a")
        for item in patentsList:
            # if(item.get_text()[-2:])=='B1':
            patentList_data.append([date, item.get_text(),r"https://data.epo.org"+item.get('href')])
        print("%d / 392 done"%idx)
        sleep(0.5)
    patentList_df = pd.DataFrame(patentList_data,columns=['Publish Date','Patent Number','Link'])  
    patentList_df['UID'] = patentList_df['Patent Number']+'_'+patentList_df['Publish Date'].dt.strftime('%d-%m-%Y')


def getXMLLink(link):
    patentLinkresp = urllib3.request.urlopen(link)
    patentLinkresp  = BeautifulSoup(patentLinkresp, 'html.parser')
    patentDataResp_atags= patentLinkresp.find_all("a")
    #Select XML 
    xmlLink = ''
    for item in patentDataResp_atags:
        t_link = r"https://data.epo.org"+item.get('href')
        if'.xml' in t_link:
            xmlLink = t_link
    return xmlLink

for idx,row in patentList_df.iterrows():
    patentNumber = row['Patent Number']
    xmllink = 'https://data.epo.org/publication-server/rest/v1.2/patents/%s/document.xml'%patentNumber
    patentList_df.loc[idx,'xml link'] = xmllink

downloadPath =   '/data/workspace_files/xml'
localXmlfiles = [file for file in os.listdir(downloadPath) if '.xml' in file]
localXmlfiles_df = pd.DataFrame(localXmlfiles,index=localXmlfiles)
localXmlfiles_df

for idx,row in (patentList_df.iterrows()):
    UID = row['UID']
    xmlLink = row['xml link']
    filename = UID+'.xml'
    date = row['Publish Date'].strftime('%d-%m-%Y')    
    if filename in localXmlfiles_df.index:
        if (idx % 5000 == 0):
            print('%d present,skipping to next one '%idx) 
    else:
        filePath = downloadPath+'/'+filename
        resp =  urllib3.request.urlretrieve(xmlLink, filePath)
        print('<700K %d :%s Downladed ->'%(idx,date),'/'.join(xmlLink.split('/')[-3:-1])," to ",UID+'.xml')
        patentList_df.loc[idx,'Downloaded'] = 1
        sleep(0.5)


xmlPath = r'/data/workspace_files/xml'

import os
import pandas as pd 
from tqdm import tqdm 
files = [xmlPath+'\\'+file for file in os.listdir(xmlPath) if '.xml' in file]

import xml.etree.ElementTree as ET
patentData = []
errorFiles_df = []
errno=0
err2no=1
for file in tqdm(files):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
    
        x=root.findall("./SDOBI/B700/B730/B731/snm")
        assignee = ';'.join([i.text for i in x])
        # print(assignee)
    
        x=root.findall("./SDOBI/B700/B730/B731/adr/str")
        Street = ';'.join([i.text for i in x])
        # print(Street)
    
        x=root.findall("./SDOBI/B700/B730/B731/adr/city")
        City = ';'.join([i.text for i in x])
        # print(City)
    
        x=root.findall("./SDOBI/B700/B730/B731/adr/ctry")
        Country = ';'.join([i.text for i in x])
        # print(Country)
    
        x=root.findall("./SDOBI/B200/B220/date")
        FilingDate = ';'.join([i.text for i in x])
        # print(FilingDate)
    
        x=root.findall("./SDOBI/B400/B450/date")
        GrantDate = ';'.join([i.text for i in x])
        # print(GrantDate)
    
    
        x=root.findall("./SDOBI/B500/B540/B541")
        Title_lang = [i.text for i in x]
        idx = [pos  for pos,val in  enumerate(Title_lang) if 'en' in val]


        x=root.findall("./SDOBI/B500/B520EP")
        CPCClassData = [i.text for i in x]
        idx = [pos  for pos,val in  enumerate(CPCClassData) if 'en' in val]

    
        x=root.findall("./SDOBI/B500/B540/B542")
        Titles = [i.text for i in x]
        PatentTitle = Titles[idx[0]]
        PatentNumber = file.split('\\')[-1].split('_')[0]
        PatentxmlLink =  'https://data.epo.org/publication-server/rest/v1.2/patents/%s/document.xml'%PatentNumber

        Patentlang = root.attrib['lang']
        try:
            PatentArea = root.findall('''.//*[@id='p0001']''')[0].text
        # PatentNumber = 'EP'+root.attrib['doc-number']
        except:
            PatentArea = ''
            print("Error 2 -> ",err2no)
            err2no+=1

            
        patentData.append([PatentNumber, assignee,Country,FilingDate,GrantDate,Patentlang,PatentTitle,
                        PatentArea,PatentxmlLink,CPCClassData])
    except:
        print("Error no :",errno)
        errorFiles_df.append(file)
        errno+=1
        continue


df = pd.DataFrame(patentData,columns=['PatentNumber','Assignee','Country','FilingDate','GrantDate','Patentlang','PatentTitle',
                    'PatentArea','PatentxmlLink','Cpc Class'])