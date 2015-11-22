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
from mpl_toolkits.mplot3d import Axes3D

tickerList = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')

#ticker = 'AAPL'
ticker = tickerList[random.randint(0,len(tickerList)-1)]

stock = Stock(ticker)
Stock.generateStandard(stock)

MAVG = []
limit = 400
showLimit = 200
step1 = 1
step2 = 1

for i in range(0,limit,step1):
    dummy = []
    for j in range(1,limit+1,step2):
        dummy.append(np.mean(stock.closePrices[i:i+j]))
    
    MAVG.append(dummy)

MAVGInt1 = []
MAVGInt2 = []
errorList = []
for i in range(0,len(MAVG)):
    MAVGInt1.append(np.mean(MAVG[i][:100]))
    MAVGInt2.append(np.mean(MAVG[i][:50]))

for i in range(0,len(MAVG)):
    error = (MAVGInt2[i] - MAVGInt1[i])
    errorList.append(error)
    
errorAVG = []
for i in range(len(errorList)-100):
    errorAVG.append(sum(errorList[i:i+100]))
    
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
x1 = range(0,showLimit,step1)
ax1.plot(x1,MAVGInt1[:showLimit], color='b',label='Slow')
ax1.plot(x1,MAVGInt2[:showLimit], color='y',label='Fast')
ax2.plot(x1,errorAVG[:showLimit])
ax1.set_xlabel('time')
x2 = range(0,showLimit)
ax1.plot(x2,stock.closePrices[:showLimit],linewidth=3, color='r')

ax1.set_ylabel('MAVG', color='b')
ax2.set_ylabel('error', color='r')
##plt.plot(x1,MAVGInt1, color='b',label='Slow')
##plt.plot(x1,MAVGInt2, color='y',label='Fast')
##plt.plot(x1,errorList)
##plt.title(ticker)
##x2 = range(0,limit)
##plt.plot(x2,stock.closePrices[0:limit],linewidth=3, color='r')
ax1.legend()
plt.show()


##
##for i in range(0,len(MAVG)):
##
##    x1 = range(i*step1,limit,step2)
##    plt.plot(x1,MAVG[i][:len(x1)])
##
##
##plt.title(ticker)
##x2 = range(0,limit)
##plt.plot(x2,stock.closePrices[0:limit],linewidth=2, color='b')
##plt.show()

   
        
##X1 = []
##Y1 = []
##Z1 = []
##X2 = []
##Y2 = []
##Z2 = []
##
##for i in range(0,len(MAVG)):
##    for j in range(len(MAVG[i])):
##        X1.append(i*step1)
##        Y1.append(j*step2)
##        Z1.append(MAVG[i][j])
##
##for i in range(0,limit):
##    X2.append(i)
##    Y2.append(0)
##    Z2.append(stock.closePrices[i])
##
##fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')
###Xs, Ys = np.meshgrid(X1, Y1)
##
##ax.scatter(X1[::-1], Y1, Z1,c = 'b')
###ax.plot(X1, Y1, Z1,c = 'b')
##
###ax.scatter(X2, Y2, Z2,c = 'r')
##ax.plot(X2[::-1], Y2, Z2,c = 'r')
##
##
##plt.show()
