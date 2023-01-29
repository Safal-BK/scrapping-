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
import sqlite3
import pandas as pd


con = sqlite3.connect("database/patent_list_db.sqlite")
# Load the data into a DataFrame
patentList_df = pd.read_sql_query("SELECT * from patent_list", con)
con.close()



breakcount=3
start=datetime.now()
# download xml
print("initialize downbloading xml...")

for idx,row in patentList_df.iterrows():
    link = row['xml_link']
    response = requests.get(link)
    with open('./xml/'+row['Patent_Number']+'.xml', 'wb') as file:
        file.write(response.content)
    print("    ",(idx+1)," / ",patentList_df.shape[0]," completed...")
    sleep(0.3)
    if(idx==breakcount):
        break
print("completed...")
finish=datetime.now()
print(finish-start)