#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction
import time

startTime = time.time()

print 'Test entries will be added to database'

dbInt = DatabaseInteraction('backtest_real')

# users
# TODO pass ipv hashing meegeven
# password = fromzerotoone
dbInt.addUser("nero","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbInt.addUser("michiel","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbInt.addUser("baerto","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")

# stocks
numIgnored=0
stockList = []
z = open('tickers.txt', 'r')
for line in z.readlines():
    line =line.replace("\n", "")
    line =line.replace("\"", "")
    line =line.replace("'", "")
    cols = line.split('\t')
	
    if len(cols)==3: # aandeel heeft zowel naam,ticker als markt
    	stockList.append(cols)
    else:
		numIgnored += 1
		
z.close()
print 'numIgnored ',numIgnored

# NEED :20 weg doen
for i in range(len(stockList[:20])):
	
	if i % 500 == 0:
		print i

	name = stockList[i][1]
	ticker = stockList[i][0]
	market = stockList[i][2]

	dbInt.addStock(name,ticker)
	
	# markt in category steken
	# TODO inefficient, beter overloaden zodat je ook stockid kan meegeven
	dbInt.addStockToCategory(ticker,"market",market)

# methods
dbInt.addMethod("method1","MACD only buy param1: threshold param2: duration")
dbInt.addMethod("methodGoogleTrends","google trends uit paper params?")

# strategies
dbInt.addStrategy("MACD 3 6","method1","3 6")
dbInt.addStrategy("Google trends 0 5","methodGoogleTrends","0 5")

# data update scripts
dbInt.addDataSource("standardUpdate.py", "standard yahoo data")

endTime = time.time()
elapsedTime = (endTime-startTime)
print "total running time: " + str(elapsedTime) + " seconds"
