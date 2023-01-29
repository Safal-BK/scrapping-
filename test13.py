ua=[]
with open("a.txt","r") as f:
    for line in f:
        if(line[:7]=="Mozilla"):
            ua.append(line)
print(ua)

with open("useragent.txt","w") as f:
    for line in ua:
        f.write(line)