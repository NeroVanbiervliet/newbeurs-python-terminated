import numpy as np
from datetime import date, timedelta as td, datetime

def Value():
    word = 'debt'
    dataPath = 'googleTrends/' + word + '.txt'
    dummy = np.loadtxt(dataPath, delimiter=',', skiprows=1, usecols=(0,1), unpack=False,dtype = 'str')
    hits = []
    dates = []
    for i in range(len(dummy)):
        hits.append(int(dummy[i][1]))
        date_object = datetime.strptime(dummy[i][0][13:23], '%Y-%m-%d')
        dates.append(str(date_object + td(2))[:10])
        
    return hits[::-1],dates[::-1]

def Score(hits,dates):

    numberOfWeeks = 10
    scoreList = []
    dateList = []
    
    for i in range(len(hits)-numberOfWeeks):
        
        scoreValue = 0
        if hits[i] > np.mean(hits[i+1:i+numberOfWeeks+1]):
            scoreValue = 1
        if hits[i] < np.mean(hits[i+1:i+numberOfWeeks+1]):
            scoreValue = -1
        scoreList.append(scoreValue)
        dateList.append(dates[i])
        
    return scoreList,dateList

