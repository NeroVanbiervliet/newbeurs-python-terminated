import numpy as np
import os.path
import sys
sys.path.insert(0, '../Indicators/MACD')
import mainMACD as MACD

class Stock:
   
    def __init__(self,ticker):
	# TODO add sql
        self.name = ticker
        self.dataPath = '../data/stockPrices/' + ticker + '.txt'
        self.market = 'lol'
        self.category = []
        
        #load price data from txt file
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')
            # Normal lists
            self.lengthLimit = 4000
            self.openPrices = dummy[:,0][:self.lengthLimit]
            self.highPrices = dummy[:,1][:self.lengthLimit]
            self.lowPrices = dummy[:,2][:self.lengthLimit]
            self.closePrices = dummy[:,3][:self.lengthLimit]
            self.volume = dummy[:,4][:self.lengthLimit]
            # Dictionaries
            self.openPricesDict = dict(zip(self.dates, dummy[:,0][:self.lengthLimit]))
            self.highPricesDict = dict(zip(self.dates, dummy[:,1][:self.lengthLimit]))
            self.lowPricesDict = dict(zip(self.dates, dummy[:,2][:self.lengthLimit]))
            self.closePricesDict = dict(zip(self.dates, dummy[:,3][:self.lengthLimit]))
            self.volumeDict = dict(zip(self.dates, dummy[:,4][:self.lengthLimit]))
        else:
            print 'Data for ' + self.name + ' not available'

    def generateMACD(self):
        ## generate values for MACD
        self.MACDi = MACD.Value(self.closePrices)
        self.MACDiDict = dict(zip(self.dates[:len(self.MACDi)], self.MACDi))
        self.MACDScorei = MACD.Score(self.MACDi,self.closePrices)
        self.MACDScoreiDict = dict(zip(self.dates[:len(self.MACDScorei)], self.MACDScorei))
        self.MACDSignali = MACD.SignalLine(self.MACDi)
        self.MACDSignaliDict = dict(zip(self.dates[:len(self.MACDSignali)], self.MACDSignali))
