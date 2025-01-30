from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.patches as mpatches

def scatterplot(author_map):

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

    with open('author_data.json', "w") as outfile:
        json.dump(author_map, outfile, indent=4)

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