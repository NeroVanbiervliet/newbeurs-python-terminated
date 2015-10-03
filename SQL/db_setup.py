#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction
import time
print 'Test entries will be added to database'

dbObject = DatabaseInteraction('backtest_real')

# users
# NEED pass ipv hashing meegeven
# password = fromzerotoone
dbObject.addUser("nero","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbObject.addUser("michiel","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbObject.addUser("baerto","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")

# stocks
numIgnored=0
stockList = []
z = open('tickers.txt', 'r')
for line in z.readlines():
    line =line.replace("\n", "")
    line =line.replace("\"", "")
    line =line.replace("'", "")
    cols = line.split('\t')
	
    if len(cols)==3:   
    	stockList.append(cols)
    else:
		numIgnored += 1
		
z.close()
print 'numIgnored ',numIgnored

# NEED :20 weg doen
for i in range(len(stockList[:20])):
	
	if i % 500 == 0:
		print i
	# NEED addStock aanpassen, enkel markt bij categorie steken
	dbObject.addStock(stockList[i][1],stockList[i][0],stockList[i][2])

# methods
dbObject.addMethod("method1","MACD only buy param1: threshold param2: duration")
dbObject.addMethod("methodGoogleTrends","google trends uit paper params?")

# strategies
dbObject.addStrategy("MACD 3 6","method1","3 6")
dbObject.addStrategy("Google trends 0 5","methodGoogleTrends","0 5")
