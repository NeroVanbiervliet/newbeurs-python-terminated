#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

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
tickerList = dbObject.getTickerList()
print str(tickerList)
stockInfo = dbObject.getStockInfo("OAK")
print str(stockInfo)

dbObject.addPidToSimulation(1,3)