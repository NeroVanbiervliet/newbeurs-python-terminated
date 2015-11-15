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
    parameters = argv[5].split(' ')
    ID = argv[6]

    print argv
    print
    
    print 'startDate:'
    print startDate.strftime("%B %d, %Y")
    print 'endDate:'
    print endDate.strftime("%B %d, %Y")
else:
    startDate = date(2010, 1, 1)
    endDate = date(2015, 7, 1)
    methodString = 'methodTA1'
    stockSelection = 'S%P500'
    parameters = [str(30),str(3),str(0.02)]
    
# TODO simulation description doorkrijgen
comment = 'Simulator Technical Analysis'

### ###

print comment

transactionCost = 0.0075*2.

# import correct method
exec('import ' + methodString + ' as method')

#If dates are wrong, stop program
if startDate > endDate:
    print 'start date is bigger than end date, not possible'
    print simDef.endGame()
    sys.exit()
    
# generate dateList to iterate over
dateList = simDef.genDateList(startDate,endDate)

# Inladen van alle tickers
tickerListAssembly = simDef.genTickerlist(stockSelection)

## Start simulation ##
tStart = time.time()
transactionList = []
transactionListMarket = []
transactionListRandom = []
stockCount = 0

for tickerList in tickerListAssembly:
    
    stockCount += len(tickerList)
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
        dummy = simDef.randomSim(date,stockDataDict)
        transactionListRandom += dummy
        
# Part 4: calculate gains from the period
[methodTotalGain, methodAvgGain, methodLogAvgGain, methodYearGain, methodYearLogGain] = simDef.calcGains(transactionList,transactionCost,dateList)
[randomTotalGain, randomAvgGain, randomLogAvgGain, randomYearGain, randomYearLogGain] = simDef.calcGains(transactionListRandom,0.,dateList)
[marketTotalGain, marketAvgGain, marketLogAvgGain, marketYearGain, marketYearLogGain] = simDef.calcGains(transactionListMarket,0.,dateList)
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
f.write('\n')
f.write('\n' + 'Average 10-day gain Method(%): ')
f.write(str(methodAvgGain*100.))
f.write('\n' + 'Average 10-day Log gain Method(%): ')
f.write(str(methodLogAvgGain*100.))
f.write('\n' + 'Total gain Method(%): ')
f.write(str(methodTotalGain*100.))
f.write('\n' + 'Yearly gain Method(%): ')
f.write(str(methodYearGain*100.))
f.write('\n' + 'Yearly Log gain Method(%): ')
f.write(str(methodYearLogGain*100.))
f.write('\n')
f.write('\n' + 'Average 10-day gain Random(%): ')
f.write(str(randomAvgGain*100.))
f.write('\n' + 'Average 10-day Log gain Random(%): ')
f.write(str(randomLogAvgGain*100.))
f.write('\n' + 'Total gain Random(%): ')
f.write(str(randomTotalGain*100.))
f.write('\n' + 'Yearly gain Random(%): ')
f.write(str(randomYearGain*100.))
f.write('\n' + 'Yearly Log gain Random(%): ')
f.write(str(randomYearLogGain*100.))
f.write('\n')
f.write('\n' + 'Average 10-day gain Market(%): ')
f.write(str(marketAvgGain*100.))
f.write('\n' + 'Average 10-day Log gain Market(%): ')
f.write(str(marketLogAvgGain*100.))
f.write('\n' + 'Total gain Market(%): ')
f.write(str(marketTotalGain*100.))
f.write('\n' + 'Yearly gain Market(%): ')
f.write(str(marketYearGain*100.))
f.write('\n' + 'Yearly Log gain Market(%): ')
f.write(str(marketYearLogGain*100.))
f.write('\n')
f.write('\n' + 'Amount of orders: ')
f.write(str(len(transactionList)))

f.write('\n' + 'Amount of orders Random: ')
f.write(str(len(transactionListRandom)))

f.write('\n' + 'Amount of orders Market: ')
f.write(str(len(transactionListMarket)))

f.write('\n' + 'Amount of stocks in selection: ')
f.write(str(stockCount))
f.close()

f = open('data/simLog/sim' + number + 'transactions' + '.txt','w+')
f.write('ticker,buyprice,buydat,duratione,type,score,sellprice,selldate')
for i in range(len(transactionList)):
    f.write('\n' + str(transactionList[i]))
f.close()


print 'total Simulation time: ',time.time()-tStart

simDef.endGame()
        
    
