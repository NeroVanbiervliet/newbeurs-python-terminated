#Move script to other directory
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir('../')

#Import required packages
import numpy as np

import sys
sys.path.insert(0, 'General')
from stockClass import Stock
import matplotlib.pyplot as plt


daysInPast = 2000


#tickerList = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
tickerList = ['^DJI']
results = []

for ticker in tickerList:
    stock = Stock(ticker)
    stock.generateTrend()
    
    if stock.status:
        j = min(daysInPast,len(stock.closePrices)-1)
        stop = False
        while j > 0 and not stop: # all start dates iterate
            
            p0 = stock.closePrices[j]
            found1 = False
            i = 0
            while not found1 and j-i > 0: # search for trend
                pt = stock.closePrices[j-i]
                found2 = False

                if (pt - p0)/p0 > 0.1: #uptrend found
                    index = j-i
                    k  = 0
                    high = 0.
                    found1 = True
                    while j-i-k > 0 and not found2:
                        
                        if high < stock.closePrices[j-i-k]:
                            high = stock.closePrices[j-i-k]
                            index = j-i-k
                            value = high
                        
                        if (stock.closePrices[j-i-k] - high)/high < -0.05:
                            found2 = True
                        
                        k += 1
                        if j-i-k == 0:
                            stop = True
                        
                if (pt - p0)/p0 < -0.05: #downtrend found
                    index = j-i
                    k  = 0
                    low = 999999999.
                    found1 = True
                    while j-i-k > 0 and not found2:
                        
                        if low > stock.closePrices[j-i-k]:
                            low = stock.closePrices[j-i-k]
                            index = j-i-k
                            value = low
                        
                        if (stock.closePrices[j-i-k] - low)/low > 0.1:
                            found2 = True
                    
                        k += 1
                        if j-i-k == 0:
                            stop = True
                            
                i += 1
                
            if found1 and found2:
                gain1 = (value - p0)/p0
                gain2 = (value - pt)/pt
                results.append([j,index,j-i-index,gain1,gain2])

            j = index

 # onfly if one stock selected
plt.plot(stock.closePrices[:daysInPast])
dots1x = []
dots1y = []
for i in range(len(results)):
    dots1x.append(results[i][1])
    dots1y.append(stock.closePrices[results[i][1]])
    
plt.scatter(dots1x,dots1y)

plt.show()

            
L1 = []
L2 = []
gains = []

for i in range(len(results)):
    a = results[i][0]-results[i][1]
    L1.append(a)
    L2.append(results[i][2])
    gains.append(results[i][3])


[aSorted,bSorted,cSorted] = [list(x) for x in zip(*sorted(zip(gains,L1,L2), key=lambda pair: pair[0]))]

print 'Lowest'
print 'Gain, Duration, LOL'
for i in range(5):
    print aSorted[i],bSorted[i],cSorted[i]
    
print
print 'Highest'
print 'Gain, Duration, LOL'
for i in range(5):
    print aSorted[-(i+1)],bSorted[-(i+1)],cSorted[-(i+1)]
    

