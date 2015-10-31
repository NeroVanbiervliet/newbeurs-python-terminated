import numpy as np
import urllib2
import sys
sys.path.insert(0, 'General')
from stockClass import Stock
import time
from yahoo_finance import Share
import os

def writeInFile(dataPath,value):
    f = open(dataPath, "r")
    contents = f.readlines()
    f.close()

    contents.insert(1, value + '\n')

    f = open(dataPath, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

def standardUpdateDef(tickerList,ID):
    
    count = 0
    for ticker in tickerList:
        count += 1
        stock = Stock(ticker)
  
        if os.path.isfile(stock.dataPath):
            
##            dummy = Share(ticker)
##            close = dummy.get_price()
##            openValue = dummy.get_open()
##            volume = dummy.get_volume()
##            high = dummy.get_days_high()
##            low = dummy.get_days_low()
##            date = dummy.get_trade_datetime()[:10]
##
##            value = str(date) + ',' + str(openValue)+ ',' + str(high)+ ',' + str(low)+ \
##            ',' + str(close)+ ',' + str(volume)+ ',' + str(close)
##
##            writeInFile(stock.dataPath,value)

            lol = 'hier gebeurt echt niks'

        else:
            url = str('http://ichart.finance.yahoo.com/table.csv?s='+ ticker)
            try:
##                with open(stock.dataPath,'wb') as f:
##                    f.write(urllib2.urlopen(url).read())
##                    f.close()
                    
                u = urllib2.urlopen(url)
                localFile = open(ticker + '.csv', 'w')
                localFile.write(u.read())
                localFile.close()
                
                os.rename(ticker + '.csv',stock.dataPath)

            except urllib2.HTTPError:
                print stock.dataPath, 'not found'


