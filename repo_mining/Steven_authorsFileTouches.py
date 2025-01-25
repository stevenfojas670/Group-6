import json
import requests
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

if not os.path.exists("data"):
 os.makedirs("data")

# parsing filenames for src extensions
# If file extension is not a src extension, then the function will return false
def parse_filenames(filename):
    src_extensiosn = ['.java', '.cpp', '.h', '.kt', '.kts', '.gradle', '.properties', '.mk', '.pro', '.xml', '.toml', '.yml', '.bat']

    if filename.startswith('.'):
        extension = '.' + filename.split('.')[-1]
    else:
        extension = '.' + filename.rsplit('.', 1)[-1]

    if extension in src_extensiosn:
        return True
    
    print('Not source file: ', extension)
    return False

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
    author_map = {} # Dict to store the author, commits and dates

    '''
        jsonCommits - List of all commits in the repo
        shaObject - Single commit within jsonCommits
        shaDetails - List of all files within a single commit
        filenameObj - Single file metadata from the shaDetails file object
    '''

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                commit = shaDetails['commit'] # Gathering commit data
                author = commit['author'] # Gather author data
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    if parse_filenames(filename=filename):

                        if author['name'] not in author_map:
                            author_map[author['name']] = {
                                "date": author['date'],
                                "files": [filename]
                            }
                        else:
                            author_map[author['name']]['date'] = author['date']
                            author_map[author['name']]['files'].append(filename)

                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
                    else:
                        break

                    
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    # plot_files(dictfiles=dictfiles, author_map=author_map)

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ['']

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
