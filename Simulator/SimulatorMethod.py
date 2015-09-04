from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
sys.path.insert(0, '../General')
from stockClass import Stock
sys.path.insert(0, '../Methods')

## Inputs
startDate = date(2010, 1, 4)
endDate = date(2015, 7, 10)
methodString = 'method1'
stockSelection = 'S%P500'
buyParameters = [3,6]
sellParameters = [-0.1,0.1,-0.1]

comment = 'Test met werkende MACD, MACDScore >' + str(buyParameters[0]) + \
', duration ' + str(buyParameters[1]) + ', lowerlimit sell: ' + str(sellParameters[0]) + \
', upperlimit sell: ' + str(sellParameters[1])

print comment
transactionCost = 0.0075*2.
# import correct method
exec('import ' + methodString + ' as method')

if startDate > endDate:
    print 'start date is bigger than end date, not possible'

# generate dateList to iterate over
delta = endDate - startDate 
dateList = []
for i in range(delta.days + 1):
    date = startDate + td(days=i)
    dateList.append(str(date))

# Inladen van alle tickers
tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
##todo, moet nog via stockSelection

## Start simulation ##
tStart = time.time()

# Part 1: Gather all the buy signals
totalBuyList = []
stockDataDict = {}
for date in dateList:
    buyList = []
    if stockDataDict == {}:
        buyList,stockDataDict = method.mainBuy(date,{},tickerList,buyParameters)
    else:
        buyList = method.mainBuy(date,stockDataDict,tickerList,buyParameters)
        
    totalBuyList.append(buyList)

# Part 2: Gather sell signals and complete transactionlist
#TODO
transactionList = method.mainSellSim(stockDataDict,totalBuyList,sellParameters)
#transactionList = [[ticker,buyprice,buydate,duration,score,sellPrice,sellDate]]

# Part 3: calculate gains from the period
#totalBuyList = [[[ticker,price,date,duration]]]
gainList = []
amountOfOrders = 0
totalGain = 1.00
amountOfOrders = len(transactionList)
n = (int(amountOfOrders/len(dateList))+1)*buyParameters[1]
totalGainReal = np.ones(n)
#iterate all buy signals
for i in range(len(transactionList)):
    gain = (transactionList[i][5] - transactionList[i][1] - transactionCost)/transactionList[i][1]
    transactionList[i].append(gain)
    gainList.append(gain)
    totalGain = totalGain*(1+gain)
    totalGainReal[i%n] = totalGainReal[i%n]*(1+gain)
    
#transactionList = [[ticker,buyprice,buydate,duration,score,sellPrice,sellDate,gain]]

# Part 4: Check market growth
buyMarketPrice = 0
sellMarketPrice = 0
for ticker in tickerList:
    allDates = stockDataDict[ticker].dates
    beginDate = startDate
    count = 0
    while (not (str(beginDate) in allDates)) and count < 4:
        beginDate += td(1)
        count += 1
           
    stopDate = endDate
    count = 0
    while (not (str(stopDate) in allDates)) and count < 4:
        stopDate += td(-1)
        count += 1
        
    if str(stopDate) in allDates and str(beginDate) in allDates:
        buyMarketPrice += stockDataDict[ticker].closePricesDict[str(beginDate)]
        sellMarketPrice += stockDataDict[ticker].closePricesDict[str(stopDate)]

marketGain = (sellMarketPrice - buyMarketPrice)/buyMarketPrice
# Part 5: Make all plots

# Part 6: Make log file
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
f.write('\n' + 'Comment: ')
f.write(comment)
f.write('\n' + 'Start date: ')
f.write(str(startDate))
f.write('\n' + 'End date: ')
f.write(str(endDate))
f.write('\n' + 'Stock Selection: ')
f.write(str(stockSelection))
f.write('\n' + 'Average gain (%): ')
f.write(str(np.mean(gainList)*100.))
f.write('\n' + 'Total gain (%): ')
f.write(str((totalGain-1)*100.))
f.write('\n' + 'Total gain Real (%): ')
f.write(str((np.mean(totalGainReal)-1)*100.))
f.write('\n' + 'Market gain (%): ')
f.write(str(marketGain*100.))
f.write('\n' + 'Amount of orders: ')
f.write(str(amountOfOrders))
f.close()

f = open('../data/simLog/sim' + number + 'transactions' + '.txt','w+')
f.write('ticker,buyprice,buydate,duration,score,sellprice,selldate')
for i in range(len(transactionList)):
    f.write('\n' + str(transactionList[i]))
f.close()

print 'avg gain:' ,np.mean(gainList)
print 'total gain:' ,totalGain-1,np.mean(totalGainReal)-1
print 'market gain:' ,marketGain
print 'total Simulation time: ',time.time()-tStart
print 'And Now His Watch is Ended' 
