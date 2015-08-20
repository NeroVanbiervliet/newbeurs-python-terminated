import numpy as np
import os.path
import sys
sys.path.insert(0, '../Indicators/MACD')
import mainMACD as MACD

class stock:

    def __init__(self,ticker):
        self.name = ticker
        self.dataPath = '../data/stockPrices/' + ticker + '.txt'
        self.market = 'lol'
        self.category = []
        
        #load price data from txt file
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')
            self.openPrices = dummy[:,0]
            self.highPrices = dummy[:,1]
            self.lowPrices = dummy[:,2]
            self.closePrices = dummy[:,3]
            self.volume = dummy[:,4]
        else:
            print 'Data for ' + self.name + ' not available'
            self.dates = []
            self.openPrices = []
            self.highPrices = []
            self.lowPrices = []
            self.closePrices = []
            self.volume = []

    def generateMACD(self):
        ## generate values for MACD
        self.MACDi = MACD.Value(self.closePrices,self.dates)
        self.MACD = self.MACDi[0]
        self.MACDScorei = MACD.Score(self.closePrices,self.dates)
        self.MACDScore = self.MACDScorei[0]
        
