import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import requests
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from requests.exceptions import HTTPError
import sqlite3
import time
import csv
import random
import os
names=[]
urls=[]
clear="\033[A                                                                                                    \033[A"
# download xml
# print("collecting url xml...",patentList_df.shape[0])
con = sqlite3.connect("data/db/patent_list_db.sqlite")
cur = con.cursor()
patentList_df=cur.execute('SELECT xml_link ,UID  from PatentXmlTable WHERE Is_downloaded="False"')
patentList_df = pd.DataFrame(patentList_df,columns=['xml_link','UID'])  

#  sql create 4 txt file garb deom text

#  collecting urls and corresponding filenames
pbar = tqdm(total=patentList_df.shape[0])
for idx,row in patentList_df.iterrows():
    urls.append(row['xml_link'])
    names.append(row['UID'])
    pbar.update(1)
    # if idx==xmllimit:
    #     break


uagent=[]
Lines=[]
with open('useragent.txt','r') as f:
    Lines = f.readlines()
for line in Lines:
    headers={
    "User-Agent":line.strip(), 
    "Accept-Language":"en-gb",
    "Accept-Encoding":	"br, gzip, deflate",
    "Accept":"test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer":"http://www.google.com/", 
    "DNT":'1',
    }
    uagent.append(headers)


patentList_df=''


async def get_page(session,url):
    async with session.get(url) as r:
        return await r.text()
async def get_all(session,urls):
    tasks=[]
    for url in urls:
        task =  asyncio.create_task(get_page(session,url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results
async def main(urls,h):
    async with aiohttp.ClientSession(headers=h) as session:
        async with limiter:
            data = await get_all(session,urls)
            return data


# if __name__ == '__main__':
s = time.perf_counter()
now = datetime.now() # current date and time
print("time : ",now.strftime("%H:%M:%S"))
chunks_urls=[]
chunks_names=[]

limiter = AsyncLimiter(1, 1)

chunk_size=3
# urls=urls[:100]

# names=names[:100]

size=len(urls)
pbar=tqdm(total=int(size/chunk_size))#total=int(size/chunk_size)

while(urls!=''):
    if(len(urls)<chunk_size):
        chunks_urls.append([urls])
        chunks_names.append([names])
        urls=''
        names=''
        pbar.update(1)
        continue
    chunks_urls.append([urls[:chunk_size]])
    urls=urls[chunk_size:]
    chunks_names.append([names[:chunk_size]])
    names=names[chunk_size:]
    pbar.update(1)

failed_links=[]

# Clearing the Screen
os.system('clear')
now = datetime.now() # current date and time
print("time : ",now.strftime("%H:%M:%S"))
for c_i in tqdm(range(len(chunks_urls))):
    links=chunks_urls[c_i][0]
    header=uagent[c_i%(len(uagent))]
    try:
        results = asyncio.run(main(links,header))
        for i  in range(len(results)):
            with open('./data/xml/'+str(chunks_names[c_i][0][i])+".xml",'w') as f:
                f.write(str(results[i]))
            cur.execute('UPDATE PatentXmlTable  SET Is_downloaded = "True"  WHERE UID = "'+chunks_names[c_i][0][i]+'"')
            con.commit()
            time.sleep(0.01)
    except:
        failed_links.append(links)
        print(len(failed_links)," failled")
    time.sleep(0.5)

# results = asyncio.run(main(urls))
with open("log.txt",'w') as f:
    for i in failed_links:
        f.write("\n".join(i))
print(failed_links)
elapsed = time.perf_counter() - s
con.close()
print(f"Execution time: {elapsed:0.2f} seconds.")