import json
import requests
from collections import defaultdict
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
def countfiles(lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    authoredFileName = defaultdict(lambda: defaultdict(list))
    srcFiles = set()

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

                authorName = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if not 'test' in filename:
                        if 'src' in filename:
                            if filename.endswith('java') or filename.endswith('.cpp') or filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.kt'):
                                authoredFileName[authorName][date].append(filename)
                                srcFiles.add(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    counter = 0
    for filename in srcFiles:
        counter += 1

    for author in authoredFileName:
        print(author)
        for commitDate in authoredFileName[author]:
            print(f"--{commitDate}")
            for filename in authoredFileName[author][commitDate]:
                print(f"----{filename}")
    print("Source file count = " + str(counter))

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

countfiles(lstTokens, repo)
