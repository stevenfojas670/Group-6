import json
import requests
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.patches as mpatches

if not os.path.exists("data"):
 os.makedirs("data")

# parsing filenames for src extensions
# If file extension is not a src extension, then the function will return false
def parse_filenames(filename):
    src_extensiosn = ['.java', '.cpp', '.h', '.kt', '.kts', '.gradle', '.properties', '.mk', '.pro', '.xml', '.toml', '.yml', '.bat', '.sh']

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

def clean_files(author_map):

    # Map unique files to integers
    unique_files = set()

    for author in author_map.values():
        for date_entry in author.values():
            unique_files.update(date_entry['files'])
    
    unique_files_list = sorted(unique_files)

    file_to_id_map = {file: idx for idx, file in enumerate(unique_files_list, start=0)}

    all_dates = set()
    for author in author_map.values():
        all_dates.update(author.keys())

    date_objects = sorted(set(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in all_dates))

    earliest_date = min(date_objects)

    # Create mapping of dates to week numbers starting from "Week 0"
    date_to_week_map = {
        date.strftime("%Y-%m-%dT%H:%M:%SZ"): f"Week {(date - earliest_date).days // 7}"
        for date in date_objects
    }

    # Placing the mapped week numbers into the author_maps at the corresponding dates
    for author in author_map.keys():
        for date in author_map[author].keys():
            if date in date_to_week_map:
                author_map[author][date]['week'] = date_to_week_map[date]

    # print(author_map)

    to_json("author_data.json", author_map) # Creating json file so I can mess with it in jupyter notebook

    authors = list(author_map.keys())

    cmap = plt.colormaps.get_cmap('hsv')
    author_to_color = {author: idx for idx, author in enumerate(authors)}

    x = []
    y = []
    colors = []

    for author, contributions in author_map.items():
        color_idx = author_to_color[author]
        for date, details in contributions.items():
            week_number = details['week']
            for file in details['files']:
                x.append(file_to_id_map[file])
                y.append(int(week_number.split()[1]))  # Convert 'Week N' to integer N
                colors.append(color_idx)

    # Define tick marks on y-axis
    y_min, y_max = min(y), max(y)
    yticks = np.arange(y_min, y_max + 1, step=25)

    # Plot scatter plot with colormap
    plt.figure(figsize=(12, 12))
    plt.scatter(x, y, c=colors, cmap=cmap, s=40)
    plt.xlabel('Files')
    plt.ylabel('Weeks')
    plt.title('File commit history by weeks')
    plt.yticks(yticks)

    # Create legend with unique colors for authors
    legend_patches = [mpatches.Patch(color=cmap(author_to_color[author] / len(authors)), label=author) 
                    for author in authors]

    plt.legend(handles=legend_patches, title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.savefig('plotted_commit_history.png', dpi=300, bbox_inches='tight', pad_inches=0.2)

    plt.show()

    # Count contributions per author
    author_contributions = {author: len(contributions) for author, contributions in author_map.items()}

    contributions = pd.DataFrame(author_contributions.items(), columns=['Author', 'Contributions'])
    contributions.to_csv('author_contributions.csv', index=False)


def to_json(filename, jsonObj):
    with open(filename, "w") as outfile:
        json.dump(jsonObj, outfile, indent=4)

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

            all_authors = set()

            for commit_obj in jsonCommits:
                commit = commit_obj['commit']
                all_authors.add(commit['author']['name'])

            all_authors_df = pd.DataFrame(all_authors, columns=['Authors'])
            all_authors_df.to_csv('authors.csv', index=False)

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
                author_obj = commit['author'] # Gather author data
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    

                    if parse_filenames(filename=filename):

                        author_name = author_obj['name']
                        date = str(author_obj['date'])

                        if author_name not in author_map:
                            author_map[author_name] = { date: {
                                "files": [filename],
                                "week": None
                            }}
                        else:
                            if date not in author_map[author_name]:
                                author_map[author_name][date] = { 
                                    "files": [filename],
                                    "week": None
                                }
                            else:
                                author_map[author_name][date]['files'].append(filename)

                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
                    else:
                        break

                    
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    
    clean_files(author_map=author_map)

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
