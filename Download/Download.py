import urllib2
import csv
import sys
import os
import os.path
import numpy as np


def Download():

    stockList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')

    for i in range(len(stockList)):
        label = str(stockList[i])
        filename=label+'.txt'
        f=os.path.isfile('../data/stockPrices/' + filename)

        if f:
            os.remove('../data/stockPrices/' + filename)
            
        f = os.path.isfile('../data/stockPrices/' + filename)
        
        if f==False:
            
            url = str('http://ichart.finance.yahoo.com/table.csv?s='+ label)
            try:
                u = urllib2.urlopen(url)
                localFile = open('table.csv', 'w')
                localFile.write(u.read())
                localFile.close()
                
                os.rename('table.csv','../data/stockPrices/' + filename)

            except urllib2.HTTPError:
                print filename, 'not found'


Download()
