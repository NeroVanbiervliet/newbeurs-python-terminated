import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname('../')
os.chdir(dname)

import numpy as np
import urllib2
import sys
sys.path.insert(0, 'General')
from stockClass import Stock
import time
from yahoo_finance import Share

def endGame():
    print 'And Now His Watch is Ended'

tStart = time.time()

# TODO: tickerlist van database
tickerList = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')

count = 0
for ticker in tickerList:
    count += 1
    stock = Stock(ticker)

    if count%50 == 0:
        tElapsed = time.time()-tStart
        print 'Avg time per stock:', tElapsed/float(count)
        print 'Time remaining:', (len(tickerList)-count)*tElapsed/float(count)
        
    if os.path.isfile(stock.dataPath):
        
        dummy = Share(ticker)
        close = dummy.get_price()
        open = dummy.get_open()
        volume = dummy.get_volume()
        high = dummy.get_days_high()
        low = dummy.get_days_low()
        date = dummy.get_trade_datetime()[:10]

    else:
        url = str('http://ichart.finance.yahoo.com/table.csv?s='+ ticker)
        try:
            u = urllib2.urlopen(url)
            localFile = open('table.csv', 'w')
            localFile.write(u.read())
            localFile.close()
            
            os.rename('table.csv',stock.dataPath)

        except urllib2.HTTPError:
            print stock.dataPath, 'not found'

print 'total download time: ',time.time()-tStart
endGame()
