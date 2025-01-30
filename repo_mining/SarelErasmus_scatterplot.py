import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv
from datetime import datetime

# @startDate, The date of the first commit to compare all other dates to
# @lstTokens, Date to be compared to
def findWeeks(startDate,endDate):
    start_object = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%SZ').date()
    end_object = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%SZ').date()

    delta = end_object - start_object

    weeks = delta.days // 7

    return weeks


# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# Open the csv file from authorsFileTouches script
file = repo.split('/')[1]
fileInput = open('data/authors_'+ file + '.csv')
reader = csv.reader(fileInput)
next(reader)

authorCSV = list(reader)

# Need to reverse since the script went through commits from most recent to least recent
authorCSV.reverse()

# Some empty lists are added in between entries so remove those
authorCSV = list(filter(None, authorCSV))

startDate = authorCSV[0][0]

files = dict()
authors = dict()

# Need to get the amount of unique authors to generate colors
for rows in authorCSV:
    authors[rows[2]] = ""

# Get a colormap and normalize it
cm = plt.get_cmap('gist_rainbow')
cNorm = plt.Normalize(0, len(authors)-1)
scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=cm)

# Reset authors dictionary to make assigning the colors easier
authors = dict()
authorIndex = 0

for rows in authorCSV:
    currentDate = rows[0]
    currentFile = rows[1]
    currentAuthor = rows[2]

    # Calculate the amounts weeks between the start date and the date of the current commit
    weekIndex = findWeeks(startDate,currentDate)

    # Enumerate the files to be able to plot
    if(not currentFile in files):
        files.update({currentFile:len(files) - 1})

    # Assign a distinctive color to each author
    if(not currentAuthor in authors):
        authors.update({currentAuthor:scalarMap.to_rgba(authorIndex)})
        authorIndex += 1

    fileIndex = files.get(currentFile)
    
    plt.scatter(fileIndex,weekIndex,color=authors[currentAuthor])

colors = authors.values()
custom_lines = [Line2D([0], [0], color=color, lw=4) for color in colors]
names = authors.keys()

plt.legend(handles=custom_lines,labels=names,loc='upper center', bbox_to_anchor=(0.9, 0.5),fontsize=7)

plt.xlabel('Files')
plt.ylabel('Weeks')
plt.show()
    



