# Jesse Ortega
# CS 472-1002, Spring 2025
# Lab 1: Git and GitHub

import json
import requests

from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
def drawPlot(lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # Key1: Commit Author's name, Value1/Key2: commit date, Value2: List of source files touched in commit
    authorTouchHistory = defaultdict(lambda: defaultdict(list))

    # Source file extensions selected based on the languages present in the repo 
    sourceFileExtensions = {'.cpp', '.h', '.java', '.kt'}

    # Set storing possible source files
    sourceFilenames = set()

    # Used to calculate the time difference between X commit and the repo's first commit
    oldestCommitDate = ''

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
                commitdate_str = shaDetails['commit']['author']['date']
                commitdate = datetime.strptime(commitdate_str, '%Y-%m-%dT%H:%M:%SZ')

                # Update the oldest found commit date
                oldestCommitDate = commitdate

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

    # Creating a mapping of a filename to an arbitrary, unique integer
    files = dict()
    for i, j in enumerate(sourceFilenames):
        files[j] = i

    # Holds the names of commit authors that have had a point plotted.
    authorPlotted = set()

    # Touch file count
    fileTouchCount = {key: 0 for key in sourceFilenames}

    # Load a list of colors
    # These will help make different plot points from different commit authors
    # distinguishable
    colors = list(mcolors.XKCD_COLORS)

    # Scatterplot configuration
    plt.figure(figsize=(15, 6))
    plt.title('File Touch History')
    plt.xlabel('File')
    plt.ylabel('Weeks')
    plt.grid(True)

    # Iterating through all the data, plotting points
    for i, author in enumerate(authorTouchHistory.keys()):
        for commitDate in authorTouchHistory[author]:
            for filename in authorTouchHistory[author][commitDate]:
                # If-else statement necessary to prevent duplicates from being listed
                # in the legend
                fileTouchCount[filename] += 1

                if author in authorPlotted:
                    plt.scatter(files[filename], ((commitDate - oldestCommitDate).days)/7, color=colors[i], s=50)
                else:
                    plt.scatter(files[filename], ((commitDate - oldestCommitDate).days)/7, color=colors[i], label=author, s=50)
                    authorPlotted.add(author)

    # Somewhat nicely prints the legend right of the scatterplot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True)
    plt.show()

    # too lazy to sort
    for key in fileTouchCount:
        print(f"{key} | {fileTouchCount[key]}")

# GitHub repo
repo = 'scottyab/rootbeer'

lstTokens = [""]

drawPlot(lstTokens, repo)
