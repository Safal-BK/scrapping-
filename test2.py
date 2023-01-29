# Python program to explain os.listdir() method
	
# importing os module
import os

# Get the list of all files and directories
# in the root directory
# path = "./xml"
# dir_list = os.listdir(path)

# print("Files and directories in '", path, "' :")

# # print the list
# print(dir_list)
# from tqdm import tqdms


# for i in tqdm(range(int(9e6))):
# 	pass
import pandas as pd
import xml.etree.ElementTree as ET
filename="EP4114165NWA1.xml"
path='./xml/'+filename
# tree = ET.parse(path)
# root = tree.getroot()


# print(root.findall("./SDOBI/B500/B520EP/classifications-cpc//text")[0].text)

patentData = []
errorFiles_df = []
errno=0
err2no=1
for i in range(1):
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        assignee=root.findall("./SDOBI/B700/B710/B711/snm")[0].text
        # print(assignee)

        Street = root.findall("./SDOBI/B700/B710/B711/adr/str")[0].text
        # print(Street)

        City = root.findall("./SDOBI/B700/B710/B711/adr/city")[0].text
        # print(City)

        Country = root.findall("./SDOBI/B700/B710/B711/adr/ctry")[0].text
        # print(Country)

        FilingDate = root.findall("./SDOBI/B800/B860/B861/date")[0].text
        # print(FilingDate)

        GrantDate = root.findall("./SDOBI/B400/B405/date")[0].text
        # print(GrantDate)

        Patentlang = root.attrib['lang']

        CPCClassData=root.findall("./SDOBI/B500/B520EP/classifications-cpc//text")[0].text
        # print(CPCClassData)

        # classification cpc

        PatentTitle = "patent title"

        PatentNumber = "4534352525"

        PatentxmlLink =  'https://data.epo.org/publication-server/rest/v1.2/patents/%s/document.xml'%PatentNumber
        
        PatentArea = ''
            
        patentData.append([PatentNumber, assignee,Country,FilingDate,GrantDate,Patentlang,PatentTitle,
                        PatentArea,PatentxmlLink,CPCClassData])
        print(patentData)
    except:
        print("Error no :",errno)
        errno+=1
        continue

    


df = pd.DataFrame(patentData,columns=['PatentNumber','Assignee','Country','FilingDate','GrantDate','Patentlang','PatentTitle',
                    'PatentArea','PatentxmlLink','Cpc Class'])

print(df.shape[0])
    