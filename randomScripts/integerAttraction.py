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
#ticker = tickerList[random.randint(0,len(tickerList)-1)]
stock = Stock(ticker)
Stock.generateStandard(stock)

