#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction
import time

dbObject = DatabaseInteraction('backtest_real')
[columnNames,queryResult] = dbObject.getAllTableEntries("strategy")
for item in columnNames:
	print item[0]

for item in queryResult:
	print item
print '------------------------'
dbObject.getTableNames()

#dbObject.addMethod("fundamentalist","geen argumenten jongeuh")
#dbObject.addStock("apple","BLUB","Nasdaq")
#dbObject.addStock("oak","OAKK","EuroNext")
tickerList = dbObject.getAllTickers()
print str(tickerList)
stockInfo = dbObject.getStockInfo("OAK")
print str(stockInfo)

dbObject.addPidToSimulation(1,3)

#test om stocks in de server te steken

startTime = time.time()
for i in range(200,700):
	ticker = "h" + str(i)
	#dbObject.addStock(ticker,ticker,"brolmarkt")

endTime = time.time()
print endTime-startTime

[columnNames,queryResult] = dbObject.getTickerList("criterium='locatie' AND value='lieven zijn bureau'")
print str(columnNames)
print str(queryResult)