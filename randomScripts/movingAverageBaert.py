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
limit = 200
entry = 50
move = 100

for i in range(0,min(len(stock.closePrices)-entry-move,200)):
    dummy = []
    for j in range(1,limit+1-entry):
        dummy.append(np.mean(stock.closePrices[move+entry+i:move+entry+i+j]))

    
    MAVG.append(dummy)

for i in range(0,len(MAVG),5):
    x1 = range(entry+i,limit)
    plt.plot(x1,MAVG[i][:len(x1)])


plt.title(ticker)
x2 = range(0,limit)
plt.plot(x2,stock.closePrices[move:move+limit],linewidth=2, color='r')
plt.show()

##X = []
##Y = []
##Z = []
##for i in range(len(MAVG)):
##    for j in range(len(MAVG[i])):
##        X.append(i)
##        Y.append(j)
##        Z.append(MAVG[i][j])
##
##fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')
##X, Y = np.meshgrid(X, Y)
##
##ax.plot_surface(X, Y, Z)
##plt.show()
