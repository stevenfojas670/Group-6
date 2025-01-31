import json
import requests
from collections import defaultdict
import csv
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.lines import Line2D

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
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

                authorName = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                commitDate = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')  # Convert string to datetime

                # Get the week number (ISO format)
                week_number = commitDate.isocalendar()[1]

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if not 'test' in filename and 'src' in filename and filename.endswith(('java', 'cpp', 'c', 'h', 'kt')):
                        authoredFileName[authorName][week_number].append(filename)
                        srcFiles.add(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return authoredFileName, srcFiles

# Generate the scatter plot
def generate_scatter_plot(authoredFileName, srcFiles):
    # Set up colors for each author
    authors = list(authoredFileName.keys())
    colors = cm.get_cmap("tab20", len(authors))  # 20 unique colors
    author_color_map = {authors[i]: colors(i) for i in range(len(authors))}

    # Create a file index map
    file_index_map = {file: idx for idx, file in enumerate(srcFiles)}

    # Set up the plot
    plt.figure(figsize=(10, 6))

    # Generate the scatter plot
    for author, weeks in authoredFileName.items():
        for week, files in weeks.items():
            # Plot each file for that author and week
            for file in files:
                file_idx = file_index_map[file]
                plt.scatter(week, file_idx, color=author_color_map[author], label=author if week == 1 else "")

    # Create the legend with custom color-key for authors
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=author_color_map[author], markersize=10, label=author) for author in authors]
    plt.legend(handles=legend_elements, title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Labels and title
    plt.xlabel("Weeks")
    plt.ylabel("Files (Indexed)")
    plt.title("Weeks vs Files (Shaded by Author)")
    plt.xticks(np.arange(1, max([week for weeks in authoredFileName.values() for week in weeks])+1, 1))  # Weeks on x-axis
    plt.yticks(np.arange(len(srcFiles)), [f'file_{i+1}' for i in range(len(srcFiles))])  # Files on y-axis, using indices

    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    # GitHub repo
    repo = 'scottyab/rootbeer'
    lstTokens = [""]  # Replace with your tokens

    # Get the file data from GitHub
    authoredFileName, srcFiles = countfiles(lstTokens, repo)

    # Generate and display the scatter plot
    generate_scatter_plot(authoredFileName, srcFiles)

if __name__ == "__main__":
    main()
