import os
#navigeer naar directory van deze file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.chdir('../')

import numpy as np
import urllib2
import sys
sys.path.insert(0, 'General')
from stockClass import Stock
import time
import os
import re
from datetime import date

def standardUpdateDef(tickerList):
    
    for ticker in tickerList:
        sleep(0.5)
        stock = Stock(ticker)
  
        if os.path.isfile(stock.dataPath):
            dailyUpdate(ticker,stock)
        else:
            fullPriceUpdate(ticker,stock)

def writeInFile(dataPath,value):
    f = open(dataPath, "r")
    contents = f.readlines()
    f.close()

    contents.insert(1, value + '\n')

    f = open(dataPath, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

def downloadActualData(ticker):

    url = 'http://finance.yahoo.com/q/hp?s=' + ticker + '+Historical+Prices'
    
    a = urllib2.urlopen(url)
    b =a.read()
    pattern = '<span class="time_rtq_ticker"><span id="yfs_l84_' + ticker.lower() + '">(.*?)</span></span> '
    m = re.search(pattern,b)
    value = m.group(1)

    return value

def dailyUpdate(ticker,stock):
    if os.path.isfile(stock.dataPath):
        f = open(stock.dataPath,'r')
        a = f.readlines()
        dateFile = a[1][0:10]
        f.close()

        if not dateFile == str(date.today()):

            url = 'http://finance.yahoo.com/q/hp?s=' + ticker + '+Historical+Prices'
            a = urllib2.urlopen(url)
            b =a.read()

            pattern = '</th></tr><tr>' + \
                      '<td class="yfnc_tabledata1" nowrap align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td>' + \
                      '<td class="yfnc_tabledata1" align="right">(.*?)</td></tr>'
            
            m = re.search(pattern,b)

            if m:
                dateTemp = time.strptime(m.group(1),"%b %d, %Y")
                dateValue = time.strftime("%Y-%m-%d",dateTemp)
                openPrice = m.group(2)
                highPrice = m.group(3)
                lowPrice = m.group(4)
                closePrice = m.group(5)
                volume = m.group(6).replace(',','')
                adjClose = m.group(7)
                
                value = str(dateValue) + ',' + \
                        str(openPrice) + ',' + \
                        str(highPrice) + ',' + \
                        str(lowPrice) + ',' + \
                        str(closePrice) + ',' + \
                        str(volume) + ',' + \
                        str(adjClose)

                if not dateFile == dateValue:
                    writeInFile(stock.dataPath,value)
        
    
def fullPriceUpdate(ticker,stock):
    
    if os.path.isfile(stock.dataPath):
        os.remove(stock.dataPath)
        
    url = str('http://ichart.finance.yahoo.com/table.csv?s='+ ticker)
    try:     
        u = urllib2.urlopen(url)
        localFile = open(ticker + '.csv', 'w')
        localFile.write(u.read())
        localFile.close()
        
        os.rename(ticker + '.csv',stock.dataPath)

    except urllib2.HTTPError:
        print stock.dataPath, 'not found online'




