#Move script to other directory
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.chdir('../')

import random
import sys
sys.path.insert(0, 'General')
from stockClass import Stock

import numpy as np
import matplotlib.pyplot as plt

tickerList = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')

#ticker = 'AAPL'
ticker = tickerList[random.randint(0,len(tickerList)-1)]
stock = Stock(ticker)
Stock.generateStandard(stock)

entry = 50
period = 20

WAVG1 = []
WAVG2 = []
WAVG3 = []

for i in range(entry,min(len(stock.closePrices),200)):

    num1,den1,num2,den2,num3,den3 = 0.,0.,0.,0.,0.,0.
       
    for j in range(period):

        num1 += stock.volume[i+j]*stock.closePrices[i+j]
        den1 += stock.volume[i+j]
        num2 += 1/stock.volume[i+j]*stock.closePrices[i+j]
        den2 += 1/stock.volume[i+j]
        num3 += stock.closePrices[i+j]
        den3 += 1.
    
    WAVG1.append(num1/den1)
    WAVG2.append(num2/den2)
    WAVG3.append(num3/den3)



x1 = range(entry,min(len(stock.closePrices),200))
plt.plot(x1,WAVG1, color='b',label='Weighted')
plt.plot(x1,WAVG2, color='g',label='Inverse Weighted')
plt.plot(x1,WAVG3, color='y',label='Normal')
plt.title(ticker)
x2 = range(0,min(len(stock.closePrices),200))
plt.plot(x2,stock.closePrices[:len(x2)],linewidth=2, color='r')
plt.legend()
plt.show()
