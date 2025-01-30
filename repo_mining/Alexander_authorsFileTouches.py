import json
import requests
import csv
import pandas as pd

import os

if not os.path.exists("data"):
 os.makedirs("data")

#Get the data from the csv
data = pd.read_csv('data/file_rootbeer.csv')

#drop the unneeded touches column
data = data.drop('touches', axis=1)

print(data.head())