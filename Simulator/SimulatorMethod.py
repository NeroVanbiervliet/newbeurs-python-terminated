from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
from sys import argv
sys.path.insert(0, '../General')
from stockClass import Stock
sys.path.insert(0, '../Methods')


## Inputs
if len(argv) > 1:
    startDateList = argv[1].split('-')
    startDate = date(int(startDateList[0]),int(startDateList[1]),int(startDateList[2]))

    endDateList = argv[2].split('-')
    endDate = date(int(endDateList[0]),int(endDateList[1]),int(endDateList[2]))

    methodString = argv[3]
    stockSelection = argv[4]
    parameters = argv[5] 
    ID = argv[6]

    print 'startDate:'
    print startDate.strftime("%B %d, %Y")
    print 'endDate:'
    print endDate.strftime("%B %d, %Y")
else:
    startDate = date(2008, 1, 1)
    endDate = date(2010, 7, 1)
    methodString = 'methodGoogleTrends'
    stockSelection = 'S%P500'
    parameters = [0,5]
    
# TODO simulation description doorkrijgen
comment = 'Eerste test met Google Trends indicator op Dow Jones'

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
##TODO, moet nog via stockSelection
tickerLimit = 200
tickerListTotal = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
#tickerListTotal = ['^DJI']
tickerListAssembly = []
a = int(len(tickerListTotal)/tickerLimit) + 1
for i in range(a):
    tickerListAssembly.append(tickerListTotal[i*tickerLimit:i*tickerLimit+tickerLimit])
    
## Start simulation ##
tStart = time.time()
transactionList = []
buyMarketPrice = 0
sellMarketPrice = 0

for tickerList in tickerListAssembly:
    portfolio = []
    #money = 10000. 
    stockDataDict = method.generateData(tickerList)

    # Iterate all days
    for date in dateList:
        ## Part 1: buy signals
        buyList = []
        buyList = method.mainBuy(date,stockDataDict,tickerList,parameters)

        portfolio += buyList
        
        # Part 2: sell signals
        transactionListDummy,indices = method.mainSell(date,stockDataDict,tickerList,parameters,portfolio)
        for i in range(len(indices)):
            portfolio.pop(indices[i]-i)

        transactionList += transactionListDummy

        
    #Part 3: market growth
    for ticker in tickerList:
        if stockDataDict[ticker].status:
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

marketGain = (sellMarketPrice - buyMarketPrice)/max(buyMarketPrice,1)

# Part 4: calculate gains from the period
## TODO: voeg options, shorten etc toe
#totalBuyList = [[[ticker,price,date,duration]]]
gainList = []
amountOfOrders = 0
totalGain = 1.00
amountOfOrders = len(transactionList)
n = (int(amountOfOrders/len(dateList))+1)*6.
totalGainReal = np.ones(n)
#iterate all buy signals
for i in range(len(transactionList)):
    gain = (transactionList[i][5] - transactionList[i][1] - transactionCost)/transactionList[i][1]
    transactionList[i].append(gain)
    gainList.append(gain)
    totalGain = totalGain*(1+gain)
    totalGainReal[i%n] = totalGainReal[i%n]*(1+gain)
    
#transactionList = [[ticker,buyprice,buydate,duration,score,sellPrice,sellDate,gain]]

# Part 5: Make all plots

# Part 6: Make log file
if 'argv' in locals():
    number = ID

else:
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

        
    
