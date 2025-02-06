#imported code from CollectFiles.py
import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

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
def countfiles(dictfiles, lsttokens, repo,dates,names):
    ipage = 1  # url page counter
    ct = 0  # token counter

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
                    if '.cpp' in filename or '.java' in filename or '.kts' in filename or '.h' in filename or 'Cmake' in filename:
                        commitfile = shaDetails['commit']
                        name = commitfile['author']['name']
                        date = commitfile['author']['date']
                        #login = {'name': 'Niall Scott', 
                        #         'email': 'riverniall@gmail.com', 
                        #         'date': '2024-10-04T07:42:57Z'}
                        names.append(name)
                        dates.append(date)
                        #dictfiles[filename] = name
                        print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["insert token"]

dictfiles = dict()
dates = []
names = []
countfiles(dictfiles, lstTokens, repo,dates,names)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/authors_' + file + '.csv'
rows = ["Author", "date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
i = 0
for git,name in dictfiles.items():
    rows = [name,dates[i]]
    i += 1
    writer.writerow(rows)
    #if bigcount is None or count > bigcount:
    #    bigcount = count
    #    bigfilename = filename
fileCSV.close()
#print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
print("these are all the authors of the source files")