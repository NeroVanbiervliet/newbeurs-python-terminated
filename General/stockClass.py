import numpy as np
import os.path
import sys
sys.path.insert(0, 'Indicators/MACD')
import mainMACD as MACD
sys.path.insert(0, 'Indicators/GoogleTrend')
import mainGoogleTrend as GoogleTrend
sys.path.insert(0, 'Indicators/Aroon')
import mainAroon as Aroon
sys.path.insert(0, 'Indicators/BaertIndicator')
import mainBaert as Baert
import matplotlib.pyplot as plt

class Stock:
   
    def __init__(self,ticker):
	# TODO add sql
        self.name = ticker
        self.dataPath = 'data/stockPrices/' + ticker + '.txt'
        self.market = 'lol'
        self.category = []
        self.MACD_parameters = [12,26,9]
        self.AroonParameters = [20]
        self.lengthLimit = 2000
        self.status = True
        
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
            #self.MACDSignali = MACD.SignalLine(self.MACDi,self.MACD_parameters[2])
            #self.MACDSignaliDict = dict(zip(self.dates[:len(self.MACDSignali)], self.MACDSignali))

        else:
            print 'Data for ' + self.name + ' not available'
            self.status = False

    def generatePID(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5,6), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
            # Normal lists
            # close price adjusted is used
            self.closePrices = dummy[:,5][:self.lengthLimit]
            # dictionary
            self.closePricesDict = dict(zip(self.dates, self.closePrices))	
            # dailyGain calculation
            self.closePricesArray = np.array(self.closePrices, dtype='f')			
            self.dailyGainArray = np.divide(self.closePricesArray[0:len(self.closePricesArray)-1],self.closePricesArray[1:len(self.closePricesArray)])
            # dictionary
            self.dailyGainDict = dict(zip(self.dates[0:len(self.closePricesArray)-1], self.dailyGainArray))
            self.dates = self.dates[0:len(self.closePricesArray)-1]
            
        else:
            print 'Data for ' + self.name + ' not available'
            self.status = False

    def generateGoogleTrend(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5,6), unpack=False)
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
        
    def generateTechnicalAnalysis1(self):
        if os.path.isfile(self.dataPath):
            dummy = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(1,2,3,4,5,6), unpack=False)
            self.dates = np.loadtxt(self.dataPath, delimiter=',', skiprows=1, usecols=(0,), unpack=False,dtype = 'str')[:self.lengthLimit]
            # Normal lists
            # close price adjusted is used
            self.closePrices = dummy[:,5][:self.lengthLimit]
            self.closePricesDict = dict(zip(self.dates, dummy[:,5][:self.lengthLimit]))
            ## Generate values for MACD
            MACDtemp = MACD.Value(self.closePrices,self.MACD_parameters[0],self.MACD_parameters[1])
            self.MACDScorei = MACD.Score(MACDtemp,self.closePrices,self.MACD_parameters[2])
            self.MACDScoreiDict = dict(zip(self.dates[:len(self.MACDScorei)], self.MACDScorei))
            ## Generate values for Aroon
            AroonUp,AroonDown = Aroon.Value(self.closePrices,self.AroonParameters[0])
            self.AroonTiming = Aroon.Timing(AroonUp,AroonDown)
            self.AroonTimingDict = dict(zip(self.dates[:len(self.AroonTiming)], self.AroonTiming))
            ## Generate Values for On Balance Volume

            self.dates2 = self.dates[:len(self.AroonTiming)][:len(self.MACDScorei)]
        else:
            print 'Data for ' + self.name + ' not available'
            self.status = False
