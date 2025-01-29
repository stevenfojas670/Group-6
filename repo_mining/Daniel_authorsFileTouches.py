'''
Name: Daniel Levy, #8001542698, CS472, Lab #1
Description: This script will go through each commit from a GitHub repo
and store the author/date the commit was made on. This is the same script
as `CollectFiles.py` (Dr. Businge said I could reuse this script for this file),
but now I will be parsing the commit data from GitHub's API instead of just
retrieving the file name.
Input: .csv file containing all files that needs to be checked
Output: .csv file containing a log of all commits for a GitHub repo 
'''
import pandas 
import requests
import json
import csv 

outFiles = list(list())

# GitHub Tokens
lstTokens = []

# Reads an input file
def readInputFile(repo):
    return pandas.read_csv("data/"+repos[repo]) 

# GitHub Authentication function
# Retrieved from `CollectFiles.py`
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

# GitHub Checker Function
# Retrived from `CollectFiles.py`
def checkCommits(files, lsttokens,repo): 
    ipage = 1  
    ct = 0 

    try:
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)
           
            if len(jsonCommits) == 0:
                break
            
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                # To get the commit history, I will use the same GitHub API that gave us the source
                # files and extract the data I need from the commits via the JSON
                for filenameObj in filesjson:
                    fileName = filenameObj['filename']
                    
                    # Now instead of just getting the file name, we will also get the
                    # associated commit we are looking at 
                    commit = shaObject['commit']
                    
                    # If the file we are checking is apart of our input file, then that 
                    # means we need to retrieve the author/date for this particular commit 
                    if filenameObj['filename'] in files:
                        outFiles.append([fileName,commit['author']['name'],commit['author']['date']])
                        print(f"Found commit from {commit['author']['name']} on {commit['author']['date']}")
            ipage += 1      
    except:
        print("Error receiving data")
        exit(0)

# Creates an output file to be used with `scatterplot.py`
def createOutputFile():
    df = pandas.DataFrame(outFiles)
    df.columns = ["File Name", "Commit Author", "Commit Date"]
    df.to_csv('commit_history.csv',index=False)

# Main function for script
def main():
    repo = 'scottyab/rootbeer' # Set repo we are checking commit history for

    srcFiles = readInputFile(repo)
    checkCommits(set(srcFiles["Filename"]),lstTokens,repo)
    
    createOutputFile()

if __name__ == "__main__":
    main()
