import numpy as np
import os.path
import sys
sys.path.insert(0, 'Indicators/MACD')
import mainMACD as MACD
sys.path.insert(0, 'Indicators/GoogleTrend')
import mainGoogleTrend as GoogleTrend
import matplotlib.pyplot as plt

class Stock:
   
    def __init__(self,ticker):
	# TODO add sql
        self.name = ticker
        self.dataPath = 'data/stockPrices/' + ticker + '.txt'
        self.market = 'lol'
        self.category = []
        self.MACD_parameters = [12,26,9]
        self.lengthLimit = 5000
        self.status = True
        
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
            self.status = False

    def generateGoogleTrend(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(6,), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
            # Normal lists
            # close price adjusted is used
            self.closePrices = dummy[:,5][:self.lengthLimit]
            # Dictionaries
            self.closePricesDict = dict(zip(self.dates, dummy[:,5][:self.lengthLimit]))
            ## generate values for MACD
            self.hits,self.datesTrend = GoogleTrend.Value()
            self.hitsDict = dict(zip(self.datesTrend, self.hits))
            self.GTScore,self.datesTrendScore = GoogleTrend.Score(self.hits,self.datesTrend)
            self.GTScoreDict = dict(zip(self.datesTrendScore, self.GTScore))

        else:
            print 'Data for ' + self.name + ' not available'
            self.status = False
        
    def generateTrend(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(6,), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
            # Normal lists
            # close price adjusted is used
            self.closePrices = dummy[:self.lengthLimit]
            # Dictionaries
            self.closePricesDict = dict(zip(self.dates, dummy[:self.lengthLimit]))
        else:
            print 'Data for ' + self.name + ' not available'
            self.status = False
        
