from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
sys.path.insert(0, '../General')
from stockClass import stock
sys.path.insert(0, '../Methods')

## Inputs
startDate = date(2015, 7, 10)
endDate = date(2014, 7, 10)
method = 'method1'

# import correct method
exec('import ' + method + ' as method')

# generate dateList to iterate over
delta = startDate - endDate 
dateList = []
for i in range(delta.days + 1):
    date = startDate + td(days=i)
    dateList.append(str(date))

# Inladen van alle tickers
tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')[:100]

## Start simulation ##
tStart = time.time()

# Part 1: gather all the buy signals
totalBuyList = []
counter = 0
for date in dateList:
    buyList = []
    counter += 1
    if counter == 1:
        buyList,stockDataDict = method.main(date,{},tickerList)
    else:
        buyList = method.main(date,stockDataDict,tickerList)
        
    totalBuyList.append(buyList)

# Part 2: calculate gains from the period
#totalBuyList = [[[ticker,price,date,duration]]]
gainList = []
#iterate all buy signals
for i in range(len(totalBuyList)):
    for j in range(len(totalBuyList[i])):
        ticker = totalBuyList[i][j][0]
        buyPrice = totalBuyList[i][j][1]
        buyDate = totalBuyList[i][j][2]
        duration = totalBuyList[i][j][3]
        dates = stockDataDict[ticker].dates
        index = np.where(dates==buyDate)[0][0]
        sellDate = dates[index+duration]
        sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
        totalBuyList[i][j].append(sellPrice)
        totalBuyList[i][j].append(sellDate)
        gain = (sellPrice - buyPrice)/buyPrice
        gainList.append(gain)
        
#totalBuyList = [[[ticker,price,date,duration,sellPrice,sellDate]]]

print np.mean(gain)
print 'total Simulation time: ',time.time()-tStart
print 'And Now His Watch Has Ended' 
