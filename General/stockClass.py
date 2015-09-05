import numpy as np
import os.path
import sys
sys.path.insert(0, '../Indicators/MACD')
import mainMACD as MACD
import matplotlib.pyplot as plt

class Stock:
   
    def __init__(self,ticker):
	# TODO add sql
        self.name = ticker
        self.dataPath = '../data/stockPrices/' + ticker + '.txt'
        self.market = 'lol'
        self.category = []
        self.MACD_parameters = [12,26,9]
        self.lengthLimit = 2000
        
##        #load price data from txt file
##        if os.path.isfile(self.dataPath):
##            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5,6), unpack=False)
##            
##            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
##            # Normal lists
##            # close price adjusted is used
##            self.openPrices = dummy[:,0][:self.lengthLimit]
##            self.highPrices = dummy[:,1][:self.lengthLimit]
##            self.lowPrices = dummy[:,2][:self.lengthLimit]
##            self.closePrices = dummy[:,5][:self.lengthLimit]
##            self.volume = dummy[:,4][:self.lengthLimit]
##            # Dictionaries
##            self.openPricesDict = dict(zip(self.dates, dummy[:,0][:self.lengthLimit]))
##            self.highPricesDict = dict(zip(self.dates, dummy[:,1][:self.lengthLimit]))
##            self.lowPricesDict = dict(zip(self.dates, dummy[:,2][:self.lengthLimit]))
##            self.closePricesDict = dict(zip(self.dates, dummy[:,5][:self.lengthLimit]))
##            self.volumeDict = dict(zip(self.dates, dummy[:,4][:self.lengthLimit]))
##        else:
##            print 'Data for ' + self.name + ' not available'

    def generateMACD(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5,6), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
            # Normal lists
            # close price adjusted is used
            self.closePrices = dummy[:,5][:self.lengthLimit]
            # Dictionaries
            self.closePricesDict = dict(zip(self.dates, dummy[:,5][:self.lengthLimit]))
            ## generate values for MACD
            self.MACDi = MACD.Value(self.closePrices,self.MACD_parameters[0],self.MACD_parameters[1])
            self.MACDiDict = dict(zip(self.dates[:len(self.MACDi)], self.MACDi))
            self.MACDScorei = MACD.Score(self.MACDi,self.closePrices,self.MACD_parameters[2])
            self.MACDScoreiDict = dict(zip(self.dates[:len(self.MACDScorei)], self.MACDScorei))
            self.MACDSignali = MACD.SignalLine(self.MACDi,self.MACD_parameters[2])
            self.MACDSignaliDict = dict(zip(self.dates[:len(self.MACDSignali)], self.MACDSignali))

        else:
            print 'Data for ' + self.name + ' not available'
        
