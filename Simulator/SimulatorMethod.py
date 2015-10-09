#Move script to other directory
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.chdir('../')

#Import required packages
from datetime import date, timedelta as td, datetime
import numpy as np
import time
import sys
from sys import argv
sys.path.insert(0, 'Simulator')
import simDefinitions as simDef
sys.path.insert(0, 'General')
from stockClass import Stock
sys.path.insert(0, 'Methods')



### Inputs ###
if len(argv) > 1:
    
    startDateList = argv[1].split('-')
    startDate = date(int(startDateList[0]),int(startDateList[1]),int(startDateList[2]))

    endDateList = argv[2].split('-')
    endDate = date(int(endDateList[0]),int(endDateList[1]),int(endDateList[2]))

    methodString = argv[3]
    stockSelection = argv[4]
    parameters = argv[5] 
    ID = argv[6]

    print argv
    print
    
    print 'startDate:'
    print startDate.strftime("%B %d, %Y")
    print 'endDate:'
    print endDate.strftime("%B %d, %Y")
else:
    startDate = date(2008, 1, 1)
    endDate = date(2010, 7, 1)
    methodString = 'method1'
    stockSelection = 'S%P500'
    parameters = [0,5]
    
# TODO simulation description doorkrijgen
comment = 'Simulator renewed'

### ###

print comment

transactionCost = 0.0075*2.

# import correct method
exec('import ' + methodString + ' as method')

#If dates are wrong, stop program
if startDate > endDate:
    print 'start date is bigger than end date, not possible'
    print simDef.endGame()
    sys.exit
    
# generate dateList to iterate over
dateList = simDef.genDateList(startDate,endDate)

# Inladen van alle tickers
tickerListAssembly = simDef.genTickerlist(stockSelection)

## Start simulation ##
tStart = time.time()
transactionList = []
transactionListMarket = []
transactionListRandom = []

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

        # Part 3: Market growth & Random method
        dummy = simDef.marketSim(date,stockDataDict)
        transactionListMarket += dummy
        dummt = simDef.randomSim(date,stockDataDict)
        transactionListRandom += dummy
        
# Part 4: calculate gains from the period
[methodTotalGain, methodAvgGain, methodYearGain] = simDef.calcGains(transactionList,transactionCost,dateList)
[randomTotalGain, randomAvgGain, randomYearGain] = simDef.calcGains(transactionListRandom,0.,dateList)
[marketTotalGain, marketAvgGain, marketYearGain] = simDef.calcGains(transactionListMarket,0.,dateList)
# Part 5: Make all plots

# Part 6: Make log file
if len(argv) > 1:
    number = ID

else:
    f = open('data/simLog/simNumber.txt','r')
    number  = f.read()
    f.close()
    f = open('data/simLog/simNumber.txt','w+')
    f.write(str(int(number)+1))
    f.close()

f = open('data/simLog/sim' + number + '.txt','w+')
f.write('Method: ')
f.write(methodString)
f.write('Parameters: ')
f.write(str(parameters))
f.write('\n' + 'Comment: ')
f.write(comment)
f.write('\n' + 'Start date: ')
f.write(str(startDate))
f.write('\n' + 'End date: ')
f.write(str(endDate))
f.write('\n' + 'Stock Selection: ')
f.write(str(stockSelection))

f.write('\n' + 'Average gain Method(%): ')
f.write(str(methodAvgGain*100.))
f.write('\n' + 'Total gain Real Method(%): ')
f.write(str(methodTotalGain*100.))
f.write('\n' + 'Yearly gain Real Method(%): ')
f.write(str(methodYearGain*100.))

f.write('\n' + 'Average gain Random(%): ')
f.write(str(randomAvgGain*100.))
f.write('\n' + 'Total gain Real Random(%): ')
f.write(str(randomTotalGain*100.))
f.write('\n' + 'Yearly gain Real Random(%): ')
f.write(str(randomYearGain*100.))

f.write('\n' + 'Average gain Market(%): ')
f.write(str(marketAvgGain*100.))
f.write('\n' + 'Total gain Real Market(%): ')
f.write(str(marketTotalGain*100.))
f.write('\n' + 'Yearly gain Real Market(%): ')
f.write(str(marketYearGain*100.))

f.write('\n' + 'Amount of orders: ')
f.write(str(len(transactionList)))
f.close()

f = open('data/simLog/sim' + number + 'transactions' + '.txt','w+')
f.write('ticker,buyprice,buydat,duratione,type,score,sellprice,selldate')
for i in range(len(transactionList)):
    f.write('\n' + str(transactionList[i]))
f.close()


print 'total Simulation time: ',time.time()-tStart

simDef.endGame()
        
    
