


import requests
import csv
from tqdm import tqdm



# proxylist=[]
# ua={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)\n', 'DNT': '1'}
# r=requests.get('https://httpbin.org/ip',timeout=3,headers=ua)
# print(r.status_code)
# with open('proxylist.csv','r') as f :
#     reader=csv.reader(f)
#     for row in reader:
#         proxylist.append(row[0])
# wproxy=[]
# for proxy in proxylist:
#     try:
#         r=requests.get('https://httpbin.org/ip',proxies={'http':proxy,'https':proxy},timeout=3,headers=headers
#         )
#         if(proxy!=''):
#             wproxy.append([proxy])
#         print(proxy)
#     except:
#         pass
# print(wproxy)
# with open('workingproxy.csv',"w") as f:
#     writter=csv.writer(f)
#     writter.writerows(wproxy) 




uagent=[]
Lines=[]
with open('useragent.txt','r') as f:
    Lines = f.readlines()
for line in tqdm(Lines):
    headers={
    "User-Agent":line.strip(), 
    "DNT":'1',
    }
    try:
        r=requests.get('https://data.epo.org/publication-server/rest/v1.2/patents/EP4114165NWA1/document.xml',timeout=3,headers=headers)
        uagent.append(line)
    except:
        pass
print(uagent)

#     uagent.append(headers)
# for ua in tqdm(uagent):
#     try:
#         r=requests.get('https://httpbin.org/ip',timeout=3,headers=ua)
#         print(ua)
#     except:
#         pass

# headers={
#     "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36", 
#     "DNT":'1',
#     }

# try:
#     r=requests.get('https://httpbin.org/ip',timeout=3,headers=headers)
#     print(headers)
# except:
#     pass