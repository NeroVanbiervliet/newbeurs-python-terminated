import numpy as np
import sys
sys.path.insert(0, '../General')
from stockClass import Stock


def main(date,stockDataDict,tickerList):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: date = welke dag geanalyseerd moet worden
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """
    
    buyList = []
    #buyList = [[ticker,price,date,duration,score]]
    firstTime = 0
    if stockDataDict == {}:
        # Alle data creeren voor de geselecteerde aandelen
        firstTime = 1
        for ticker in tickerList:
            stockDataDict[ticker] = Stock(ticker)
            Stock.generateMACD(stockDataDict[ticker])

    # Alle aandelen overlopen 
    for ticker in stockDataDict:
        #check if data is available for that date
        allDates = stockDataDict[ticker].dates
        if date in allDates and date in allDates[:len(stockDataDict[ticker].MACDScorei)]:
            # Voorwaarde om te kopen en toevoegen aan de buyList
            if stockDataDict[ticker].MACDScoreiDict[date] > 25:
               score = stockDataDict[ticker].MACDScoreiDict[date]
               price = stockDataDict[ticker].closePricesDict[date]
               #date = stockDataDict[ticker].dates[entry]
               duration = 6
               buyList.append([ticker,price,date,duration,score])

    ## to reduce the data package that has to be transferred       
    if firstTime == 1:
        return buyList,stockDataDict
    else:
        return buyList


### temporary ###

## ##Inladen van alle tickers
##tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
## ##run method
##buyList,stockDataDict = main('2015-08-18',{},tickerList)
