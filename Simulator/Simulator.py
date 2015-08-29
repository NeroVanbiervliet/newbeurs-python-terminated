from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
sys.path.insert(0, '../General')
from stockClass import Stock
sys.path.insert(0, '../Methods')

## Inputs
startDate = date(2014, 7, 10)
endDate = date(2015, 7, 10)
methodString = 'method1'
stockSelection = 'S%P500'
comment = 'Test met werkende MACD, MACDScore > 25, duration 6 dagen'

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
counter = 0
for date in dateList:
    buyList = []
    counter += 1
    if counter == 1:
        buyList,stockDataDict = method.mainBuy(date,{},tickerList)
    else:
        buyList = method.mainBuy(date,stockDataDict,tickerList)
        
    totalBuyList.append(buyList)

# Part 2: Gather sell signals
#TODO
transactionList = method.mainSell(stockDataDict,totalBuyList)
#transactionList = [[[ticker,buyprice,buydate,duration,score,sellPrice,sellDate]]]

# Part 3: calculate gains from the period
#totalBuyList = [[[ticker,price,date,duration]]]
gainList = []
amountOfOrders = 0
#iterate all buy signals
for i in range(len(transactionList)):

    gain = (transactionList[i][5] - transactionList[i][1] - transactionCost)/transactionList[i][1]
        
    gainList.append(gain)
        
# Part 4: Make all plots

# Part 5: Make log file
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
f.write('\n' + 'Amount of orders: ')
f.write(str(amountOfOrders))
f.close()

f = open('../data/simLog/sim' + number + 'transactions' + '.txt','w+')
f.write('ticker,buyprice,buydate,duration,score,sellprice,selldate')
for i in range(len(totalBuyList)):
    for j in range(len(totalBuyList[i])):
        f.write('\n' + str(totalBuyList[i][j]))

#todo: voeg nog andere info toe, zoals op welke markt de simulatie is gedaan, transactiekosten, hoeveel de markt zelf is gestegen etc..

print np.mean(gainList)
print 'total Simulation time: ',time.time()-tStart
print 'And Now His Watch is Ended' 
