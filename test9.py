from requests_html import HTMLSession
s=HTMLSession()
r=s.get('https://httpbin.org/headers')
print(r.text)

headers={
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8", 
"DNT":'1',
}