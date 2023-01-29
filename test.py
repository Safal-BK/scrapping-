import xml.etree.ElementTree as ET

xmlPath = r'./xml'

import os
import pandas as pd 
from tqdm import tqdm 
# files = [xmlPath+'\\'+file for file in os.listdir(xmlPath) if '.xml' in file]

import xml.etree.ElementTree as ET
patentData = []
errorFiles_df = []
errno=0
err2no=1
# for file in tqdm(['EP4114177NWA12023-01-11.xml']):
file_name='EP4115063NWA12023-01-11.xml'
path='./data/xml/'+file_name
try:
    print(os.getcwd())
    tree = ET.parse(path)
    root = tree.getroot()        
    try:
        assignee=root.findall("./SDOBI/B700/B710/B711/snm")[0].text
        print(assignee)
    
        Street = root.findall("./SDOBI/B700/B710/B711/adr/str")[0].text
        print("Street",Street)

        City = root.findall("./SDOBI/B700/B710/B711/adr/city")[0].text
        print(City)

        Country = root.findall("./SDOBI/B700/B710/B711/adr/ctry")[0].text
        print(Country)

        FilingDate = root.findall("./SDOBI/B800/B860/B861/date")[0].text
        print(FilingDate)

        GrantDate = root.findall("./SDOBI/B400/B405/date")[0].text
        print(GrantDate)

        Patentlang = root.attrib['lang']
        print(Patentlang)

        CPCClassData=root.findall("./SDOBI/B500/B520EP/classifications-cpc//text")[0].text
        print(CPCClassData)

        PatentTitle = root.findall("./SDOBI/B500/B540/B542")[1].text
        print(PatentTitle)

        PatentNumber = file_name.split('.')[0]
        print(PatentTitle)

        PatentxmlLink =  'https://data.epo.org/publication-server/rest/v1.2/patents/%s/document.xml'%PatentNumber
        print(PatentNumber)
      
        patentData.append([PatentNumber, assignee,Country,FilingDate,GrantDate,Patentlang,PatentTitle,
                        PatentxmlLink,CPCClassData])
    # PatentNumber = 'EP'+root.attrib['doc-number']
    except:
        # PatentArea = ''
        # print("Error 2 -> ",err2no)
        # err2no+=1
        pass

except:
    # print("Error no :",errno)
    # errorFiles_df.append(file)
    # errno+=1
    pass
print(patentData)
# import requests

# URL = "https://data.epo.org/publication-server/rest/v1.2/patents/EP4115404NWA1/document.xml"
# response = requests.get(URL)
# with open('./xml/feed.xml', 'wb') as file:
#     file.write(response.content)




# from datetime import datetime

# datetime_str = '2023-01-11 00:00:00'
# print(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'))
# datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S').strftime('%d-%m-%Y')

# print(type(datetime_object))
# print(datetime_object.strftime('%d-%m-%Y'))  # printed in default format