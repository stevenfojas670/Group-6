import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# use the csv created in data
file_path = 'repo_mining\data\CTfile_rootbeer.csv'
data = pd.read_csv(file_path)

x = data.iloc[:, 0].values
# getting the labels
y = data.iloc[:, 1].values
# Plot...
plt.scatter(x, y, c=y, s=25) # s is a size of marker 

plt.xlabel("Files")

# Set y-axis label
plt.ylabel("Touches")

# Set the x-axis limits
plt.gca().set_aspect('equal')

plt.show()