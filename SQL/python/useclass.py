#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

dbObject = DatabaseInteraction()
[columnNames,queryResult] = dbObject.getAllTableEntries("users")
for item in columnNames:
	print item[0]

for item in queryResult:
	print item
print '------------------------'
dbObject.getTableNames()

#dbObject.addStock("apple","BLUB","Nasdaq")
tickerList = dbObject.getTickerList()
print str(tickerList)
stockInfo = dbObject.getStockInfo("AAPL")
print str(stockInfo)
