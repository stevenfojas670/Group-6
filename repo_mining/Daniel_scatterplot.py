'''
Name: Daniel Levy, #8001542698, CS472, Lab #1
Description: This script handles the displaying of a repo's commit
history to the user. It retrieves an input file that plots which 
files were committed by what authors based on the timeframe of the 
project. 
Input: .csv file
Output: Scatterplot via matplotlib
'''
import pandas
import numpy as np 
import matplotlib.pyplot as plt 
import datetime
import random 
from cycler import cycler 
import seaborn 

# Opens the provided input file 
def openInputFile():
    return pandas.read_csv("commit_history.csv") 

# Calculates how many weeks old the project is 
def calculateProjectAge(firstCommit, lastCommit):
    oldestDate = firstCommit[0:10]
    latestDate = lastCommit[0:10]

    yearsApart = int(latestDate[0:4]) - int(oldestDate[0:4])

    return yearsApart*52

# Generates a 6 digit hex value to help
# with determining the colors
def generateRandomHexValue():
    digits = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
    hex = '#'

    for i in range(6):
        num = random.randint(0,15)
        if num >= 10:
            hex += digits[num]
        else:
            hex += str(num) 
    return hex    

# Create enumerations for all files/authors
# in a repo
def enumerateArrays(files,authors):
    eFiles, eAuthors = dict(), dict()

    for i in range(len(files)):
        eFiles[files[i]] = i
    
    for i in range(len(authors)):
        eAuthors[authors[i]] = i 

    return eFiles, eAuthors

# Sets up data to be graphed in scatterplot
def checkCommits(commits, eFiles, eAuthors,weeks):
    # Set up initial variables
    fileCommits = []
    weekCommitMade = []
    authors = []

    global initialWeeks 
    initialWeeks = weeks 
    currentDate = commits['Commit Date'][0]

    # Iterate through each commit 
    for c in commits.iterrows():
        # When the date has changed, we decrement the week count
        if currentDate != c[1]['Commit Date']:
            nextDate = c[1]['Commit Date']

            cDate = datetime.date(int(currentDate[0:4]),int(currentDate[5:7]),int(currentDate[8:10]))
            nDate = datetime.date(int(nextDate[0:4]),int(nextDate[5:7]),int(nextDate[8:10]))

            diff = cDate - nDate
            weeks -= (diff.days//7)
         
            currentDate = nextDate 

        # For every commit, keep track of the file name, which week it was made, 
        # and who the author was
        fileCommits.append(eFiles[c[1]['File Name']]) 
        weekCommitMade.append(weeks)
        authors.append(eAuthors[c[1]['Commit Author']])

    return fileCommits,weekCommitMade,authors 

# Sets up the coloring of the scatterplot based on
# the number of authors who committed in repo
def setUpScatterColor(authors):
    colors = []
    for i in range(len(authors)):
        colors.append(generateRandomHexValue())

    cycle = cycler(color=colors)
    plt.rc('axes',prop_cycle=cycle)

# Plots the scatter plot and displays to user
def plotScatter(numOfFiles,files,weeks,authors):
    for i in range(len(files)):
        plt.scatter(files[i],weeks[i])

    plt.xticks(range(0,numOfFiles,2))
    plt.yticks(range(0,initialWeeks,50))

    plt.xlabel("File")
    plt.ylabel("Weeks")

    plt.legend(authors)
    plt.title("Commit History")
    plt.show()

# Main function for script
def main():
    commits = openInputFile()

    weeks = calculateProjectAge(commits['Commit Date'].iloc[-1],commits['Commit Date'][0])

    # Get all unique files and authors from the current repo
    files = list(commits['File Name'].unique())
    authors = commits['Commit Author'].unique()

    enumeratedFiles, enumeratedAuthors = enumerateArrays(files,authors)

    fileCommits, weekCommitMade, commitAuthors = checkCommits(commits,enumeratedFiles,enumeratedAuthors,weeks)
    
    setUpScatterColor(authors)
    plotScatter(len(files),fileCommits,weekCommitMade,authors)

if __name__ == "__main__":
    main()
