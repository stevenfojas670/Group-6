# Jesse Ortega
# CS 472-1002, Spring 2025
# Lab 1: Git and GitHub

import json
import requests
import csv
from collections import defaultdict


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

# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def touchHistory(lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # Key1: Commit Author's name, Value1/Key2: commit date, Value2: List of source files touched in commit
    authorTouchHistory = defaultdict(lambda: defaultdict(list))

    # Source file extensions selected based on the languages present in the repo 
    sourceFileExtensions = {'.cpp', '.h', '.java', '.kt'}

    # Set storing possible source files
    sourceFilenames = set()

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

                # Store the commit's author
                author = shaDetails['commit']['author']['name']

                # Store the commit's creation date
                commitdate = shaDetails['commit']['author']['date']


                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    dotpos = filename.rfind('.')
                    
                    # If a touched file has a whitelisted file extension, record its name and commit date
                    # Additionally, record the source file name to reference later.
                    if dotpos > -1:
                        if filename[dotpos:] in sourceFileExtensions:
                            authorTouchHistory[author][commitdate].append(filename)
                            sourceFilenames.add(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    # Print source file names
    print("Source Filenames:")
    for filename in sourceFilenames:
            print(f"\t{filename}")

    print("\n--\n")

    for author in authorTouchHistory:
        print(author)
        for commitDate in authorTouchHistory[author]:
            print(f"\t{commitDate}")
            for filename in authorTouchHistory[author][commitDate]:
                print(f"\t\t{filename}")


# GitHub repo
repo = 'scottyab/rootbeer'

lstTokens = [""]

touchHistory(lstTokens, repo)