import matplotlib.pyplot as plt
import csv
import numpy as np

def fillList(inputFile, num):
    with open(inputFile) as file:
        myFile = csv.reader(file, delimiter=',') 
        next(myFile)
        col = num
        fileName = [row[col] for row in myFile]
    return fileName

def colorGathering(nameArray, name_dic):
    j=0
    palette=[]
    for name in nameArray:
        if name in name_dic:
            palette.append(name_dic[name])
        else:
            name_dic[name]=j
            palette.append(j)
            j=j+1
    return palette

myFile='data/file_' + 'myAuthorFileTouches' + '.csv'

name_dic = {}
fileName=np.array(fillList(myFile, 1))
nameArray=fillList(myFile, 0)
palette=colorGathering(nameArray, name_dic)
#it does not fit the whole name so i need to do use to represent them
my_dict = {}
fileNum=[]
i=0
count=0
#colors = np.random.rand(141)
#palette = np.array(mcolors.to_rgba_array(colors))

weeks=fillList(myFile, 3)
for index in fileName:
    if index in my_dict:
        fileNum.append(my_dict[index])
        #color.append("cloudy blue")
    else:
        my_dict[index]=i
        fileNum.append(i)
        i=i+1
fileNums=np.array(fileNum)

weeks=np.array(weeks)
weeks=np.flip(weeks)

plt.xlabel("file")
plt.ylabel("weeks")
plt.title("Lab 1")
plt.scatter(fileNums, weeks, c=palette)
plt.show()


