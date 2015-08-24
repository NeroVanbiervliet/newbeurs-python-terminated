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
methodString = 'method1'
stockSelection = 'S%P500'

# import correct method
exec('import ' + methodString + ' as method')

# generate dateList to iterate over
delta = startDate - endDate 
dateList = []
for i in range(delta.days + 1):
    date = startDate + td(days=i)
    dateList.append(str(date))

# Inladen van alle tickers
tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
##todo, moet nog via stockSelection

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
amountOfOrders = 0
#iterate all buy signals
for i in range(len(totalBuyList)):
    for j in range(len(totalBuyList[i])):
        amountOfOrders += 1
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

# Part 3: Make all plots

# Part 4: Make log file
f = open('../data/simLog/simNumber.txt','r')
number  = f.read()
f.close()
f = open('../data/simLog/simNumber.txt','w+')
f.write(str(int(number)+1))
f.close()

market = 'S%P500'
f = open('../data/simLog/sim' + number + '.txt','w+')
f.write('Method: ')
f.write(methodString)
f.write('\n' + 'Start date: ')
f.write(str(startDate))
f.write('\n' + 'End date: ')
f.write(str(endDate))
f.write('\n' + 'Stock Selection: ')
f.write(str(stockSelection))
f.write('\n' + 'Average gain (%): ')
f.write(str(np.mean(gain*100.)))
f.write('\n' + 'Amount of orders: ')
f.write(str(amountOfOrders))
f.close()

#todo: voeg nog andere info toe, zoals op welke markt de simulatie is gedaan etc..

print np.mean(gain)
print 'total Simulation time: ',time.time()-tStart
print 'And Now His Watch Has Ended' 
