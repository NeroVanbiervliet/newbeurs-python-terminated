#Import required packages
from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
import random
import sys
sys.path.insert(0, 'SQL')
from DatabaseInteraction import DatabaseInteraction 

def endGame():
    print 'And Now His Watch is Ended'

def randomSim(date,stockDataDict):
    
    transactionList = []
    for ticker in stockDataDict:
        #check if data is available for that date
        if stockDataDict[ticker].status:
            allDates = stockDataDict[ticker].dates
            if date in allDates:
                if random.randint(0,30) == 1: 
                   buyPrice = stockDataDict[ticker].closePricesDict[date]
                   buyDate = date
                   duration = random.randint(5,10)
                   index = np.where(allDates==buyDate)[0][0]
                   sellDate = allDates[index - duration]
                   sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
                   transactionList.append([ticker,buyPrice,buyDate,duration,'long','random',sellPrice,sellDate])

    return transactionList

def marketSim(date,stockDataDict):

    transactionList = []
    for ticker in stockDataDict:
        #check if data is available for that date
        if stockDataDict[ticker].status:
            allDates = stockDataDict[ticker].dates
            if date in allDates:
                 
                buyPrice = stockDataDict[ticker].closePricesDict[date]
                buyDate = date
                duration = 1
                index = np.where(allDates==buyDate)[0][0]
                sellDate = allDates[index - duration]
                sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
                transactionList.append([ticker,buyPrice,buyDate,duration,'long','market',sellPrice,sellDate])

    return transactionList

def calcGains(transactionList,transactionCost,dateList):

    rawGainList = []
    rawDurationList = []
    for i in range(len(transactionList)):
        gain = (transactionList[i][6] - transactionList[i][1] - transactionCost)/transactionList[i][1]
        duration = transactionList[i][3]
        type = transactionList[i][4]
        if type == 'short':
            gain = -gain
        rawGainList.append(gain)
        rawDurationList.append(duration)

    amountOfDays = len(dateList)/365.*250.
    orderPerDays = len(transactionList)/(amountOfDays)
    avgDuration = np.mean(rawDurationList)
    n = int(orderPerDays*avgDuration)+1
    totalGainReal = np.ones(n)
    for i in range(len(rawGainList)):
        totalGainReal[i%n] = totalGainReal[i%n]*(1+gain)

    avgGain = np.mean(rawGainList)
    yearGain = (1 + avgGain)**(amountOfDays/avgDuration)

    return [np.mean(totalGainReal)-1 , avgGain, yearGain]
    
def genDateList(startDate,endDate):

    delta = endDate - startDate 
    dateList = []
    for i in range(delta.days + 1):
        date = startDate + td(days=i)
        dateList.append(str(date))

    return dateList

def genTickerlist(stockSelection):
    dbInt = DatabaseInteraction('backtest_real')

    # TODO: via stockSelection
    tickerLimit = 200
    #tickerListTotal = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
    tickerListTotal = dbInt.getTickerList(stockSelection)

    tickerListAssembly = []
    a = int(len(tickerListTotal)/tickerLimit) + 1
    for i in range(a):
        tickerListAssembly.append(tickerListTotal[i*tickerLimit:i*tickerLimit+tickerLimit])

    return tickerListAssembly
