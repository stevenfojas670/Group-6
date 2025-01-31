import json
import requests
import csv
import os
from datetime import datetime

if not os.path.exists("data"):
 os.makedirs("data")

info=[]

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    #get the initial date the project begun
    projectStart = getStartDate(lstTokens)[:10]
    projectStart = datetime.strptime(projectStart, "%Y-%m-%d")

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    #check if fileName is source file (.cpp or .java or .ks or .kst)
                    if (filename.find(".cpp")>0 or filename.find(".java")>0 or filename.find(".h")>0 or filename.find(".kt")>0 or filename.find(".c")>0 or filename.find(".xml")>0):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1

                        #retrieve name of author and date information from source files
                        commitJson = shaDetails['commit']
                        authorObj = commitJson['author']
                        name = authorObj['name']
                        theDate = authorObj['date']
                        date = authorObj['date'][:10]
                        date = datetime.strptime(date, "%Y-%m-%d")
                        #print(date)
                        #iretrieved the initial date the project was created and use this date to calculate the number of weeks has passed 
                        #from that point to the commit
                        #cast to int to not worried about decimal weeks
                        weeks = int((date - projectStart).days)
                        weeks =int(weeks/7)

                        #print(filename)
                        #print(name + " " + date+'\n')

                        #Format of my tuple is [author, fileName, date, weeksFromStart]
                        myTuple=(name, filename, theDate, weeks)
                        info.append(myTuple)

                        #lineString.append(name +" "+ filename +" "+ date)

            ipage += 1 #duda
                
    except:
        print("Error receiving data")
        exit(0)

#getting the start date of the project
def getStartDate(lsttokens):
    url='https://api.github.com/repos/scottyab/rootbeer'
    json, ct = github_auth(url, lsttokens, 0)
    return json['created_at']

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits


dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

#for myTuple in info:
#    print(myTuple)
#    print("\n")

#print('Total number of files: ' + str(len(dictfiles)))

#file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + 'myAuthorFileTouches' + '.csv'

#Format of my tuple is [author, fileName, date, weeksFromStart]
#rows = ["Filename", "Touches"]
rows = ["author", "fileName", "date", "weeksFromStart"]

fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None

for myTuples in info:
    rows = [myTuples[0], myTuples[1], myTuples[2], myTuples[3]]
    writer.writerow(rows)

#for filename, count in dictfiles.items():
#    rows = [filename, count]
#    writer.writerow(rows)
#    if bigcount is None or count > bigcount:
#        bigcount = count
#        bigfilename = filename


fileCSV.close()
#print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')