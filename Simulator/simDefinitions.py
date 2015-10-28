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
                   duration = random.randint(4,10)
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
                duration = 10
                index = np.where(allDates==buyDate)[0][0]
                sellDate = allDates[index - duration]
                sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
                transactionList.append([ticker,buyPrice,buyDate,duration,'long','market',sellPrice,sellDate])

    return transactionList

def calcGains(transactionList,transactionCost,dateList):
    
    if len(transactionList) > 0:
        rawGainList = []
        rawDurationList = []
        tenDayGain = []
        tenDayLogGain = []
        for i in range(len(transactionList)):
            gainTemp = min(max((transactionList[i][6] - transactionList[i][1] - transactionCost)/transactionList[i][1],-0.5),0.5)
            
            if isinstance(gainTemp, (int, long, float, complex)) and (not np.isnan(gainTemp)):
                duration = transactionList[i][3]
                type = transactionList[i][4]
                if type == 'short':
                    gain = -gainTemp
                if type == 'long':
                    gain = gainTemp
                    
                rawGainList.append(gain)
                rawDurationList.append(duration)
                tenDayGain.append((1+gain)**(10./duration)-1)
                tenDayLogGain.append(np.log10((1+gain)**(10./duration)-1))

        amountOfDays = len(dateList)/365.*250.
        orderPerDays = len(transactionList)/(amountOfDays)
        avgDuration = np.mean(rawDurationList)
        n = int(orderPerDays*avgDuration)+1
        totalGainReal = np.ones(n)
        
        for i in range(len(rawGainList)):
            totalGainReal[i%n] = totalGainReal[i%n]*(1.+rawGainList[i])

        tenDayAvgGain = np.mean(tenDayGain)
        tenDayLogAvgGain = 10.**np.mean(tenDayLogGain)
        yearGain = (1. + tenDayAvgGain)**(250./10.)
        yearLogGain = (1. + tenDayLogAvgGain)**(250./10.)

        return [np.mean(totalGainReal)-1., tenDayAvgGain, tenDayLogAvgGain, yearGain-1., yearLogGain -1.]
    else:
        return [0,0,0,0,0]
    
def genDateList(startDate,endDate):

    delta = endDate - startDate 
    dateList = []
    for i in range(delta.days + 1):
        date = startDate + td(days=i)
        dateList.append(str(date))

    return dateList

def genTickerlist(stockSelection):
    dbInt = DatabaseInteraction('backtest_real')
    ## NEED: uncomment database dingen
    tickerLimit = 200
    #tickerListTotal = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
    tickerListTotal = dbInt.getTickerList(stockSelection)

    tickerListAssembly = []
    a = int(len(tickerListTotal)/tickerLimit) + 1
    for i in range(a):
        tickerListAssembly.append(tickerListTotal[i*tickerLimit:i*tickerLimit+tickerLimit])

    return tickerListAssembly
