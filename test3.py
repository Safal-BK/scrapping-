import os

# Get the list of all files and directories
# in the root directory
path = "./xml"
dir_list = os.listdir(path)
print(dir_list)
for i in dir_list:
    print(i.split('.')[0])