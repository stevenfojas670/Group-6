import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import csv





# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

file = repo.split('/')[1]
fileInput1 = 'data2/file_'+ file + '.csv'
fileInput2 = 'data/file_'+ file + '.csv'


names = []
files = []
with open(fileInput2, newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        for i in range(int(row['Touches'])):
            files.append(row['Filename'])

#arr of dates 
dates = []
cols = []

with open(fileInput1, newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:

        date = row['date']
        date =date.split('-')
        #print(date)
        #ai generated/assisted (google ai)
        char = 'T'
        index = date[2].rfind(char)
        if index != -1:
            result = date[2][:index]
        else:
            result = date[2]
        #end of ai gen

        date[2] = result
        #date = [YYYY,MM,DD]
        dates.append(datetime.datetime(int(date[0]),int(date[1]),int(date[2])))
        name = row['Author']
        if name == 'Niall Scott':
            cols.append('red')
        elif name == 'Scott Alexander-Bown':
            cols.append('green')
        elif name == 'Artsem Kurantsou':
            cols.append('pink')
        elif name == 'Matthew Rollings':
            cols.append('teal')
        elif name == 'Slim Namouchi':
            cols.append('yellow')
        elif name == 'Fi5t':
            cols.append('orange')
        elif name == 'mat':
            cols.append('red')
        elif name == 'Daniel Kutik':
            cols.append('blue')
        elif name == 'Ivan Vlasov':
            cols.append('purple')
        elif name == 'altvnv':
            cols.append('lightskyblue')
        elif name == 'matthew':
            cols.append('brown')
        elif name == 'Frieder Bluemle':
            cols.append('maroon')
        elif name == 'Ali Waseem':
            cols.append('salmon')
        elif name == 'LeonKarabchevsky':
            cols.append('chocolate')
        elif name == 'BIOCATCH':
            cols.append('gold')
        elif name == 'vyas':
            cols.append('tan')
            
        elif name == 'aippisch':
            cols.append('greenyellow')
        elif name == 'leocadiotine':
            cols.append('honeydew')
        elif name == 'Andy Barber':
            cols.append('forestgreen')
        elif name == 'Mohammed Ezzat':
            cols.append('aquamarine')
        else:
            cols.append('darkviolet')

    csvfile.close()
    print (len(dates))
    fig, ax = plt.subplots()
    #ax.plot_date(files,dates)
    ax.scatter(x = files, y = dates, c = cols)
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('file'))
    ax.set_xticks(np.arange(0, 31, 2))

    ax.set_ylim(datetime.datetime(2015, 1, 1), None)
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%W'))
    ax.yaxis.set_major_locator(mdates.WeekdayLocator(interval=50))
    plt.ylabel('Year - That year week Number')

    plt.show()









