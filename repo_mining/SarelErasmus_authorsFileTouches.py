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
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    source_file_extensions = ['.cpp','.java','.h','.sh','.xml','.png']

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
                date = shaDetails['commit']['committer']['date']
                dictfiles[date] = []
                authorName = shaDetails['commit']['committer']['name']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    for ext in source_file_extensions:
                        if(filename.endswith(ext)):
                            if(ext == '.xml' and filename.startswith('.')):
                                break
                            if(filename.startswith('rootbeerlib')):
                                break

                            dictfiles.get(date).append([authorName,filename])
                            print(filename)
                            break
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
lstTokens = ["3"]
# lstTokens = ["fd02a694b606c4120b8ca7bbe7ce29229376ee",
#                 "16ce529bdb32263fb90a392d38b5f53c7ecb6b",
#                 "8cea5715051869e98044f38b60fe897b350d4a"]


dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/authors_' + file + '.csv'
rows = ["Date", "Filename", "Author"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)


bigcount = None
bigfilename = None
for date, authorList in dictfiles.items():
    for name, fileName in authorList:
        rows = [date,fileName,name]
        writer.writerow(rows)
    
fileCSV.close()