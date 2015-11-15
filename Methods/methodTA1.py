import numpy as np
import sys
sys.path.insert(0, 'General')
from stockClass import Stock

def generateData(tickerList):
    stockDataDict = {}
    for ticker in tickerList:
            stockDataDict[ticker] = Stock(ticker)
            Stock.generateTechnicalAnalysis1(stockDataDict[ticker])
            
    return stockDataDict

def mainBuy(date,stockDataDict,tickerList,parameters):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: date = welke dag geanalyseerd moet worden
               parameters = [duration,limitscore voor MACD]
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """

    
    maxDuration = eval(parameters[0]) #30
    limitScoreMACD = eval(parameters[1]) #3
    
    buyList = []
    
    # Alle aandelen overlopen 
    for ticker in stockDataDict:
        #check if data is available for that date
        if stockDataDict[ticker].status:
            allDates2 = stockDataDict[ticker].dates2
            if date in allDates2:

                ## HIER Methode inserten
                # Voorwaarde om te kopen en toevoegen aan de buyList
                if stockDataDict[ticker].MACDScoreiDict[date] > limitScoreMACD and stockDataDict[ticker].AroonTimingDict[date] > 1:
                   score = [stockDataDict[ticker].MACDScoreiDict[date],stockDataDict[ticker].AroonTimingDict[date]]
                   price = stockDataDict[ticker].closePricesDict[date]
                   type = 'long'
                   buyList.append([ticker,price,date,maxDuration,type,score])

                if stockDataDict[ticker].MACDScoreiDict[date] < -limitScoreMACD and stockDataDict[ticker].AroonTimingDict[date] < -1:
                   score = [stockDataDict[ticker].MACDScoreiDict[date],stockDataDict[ticker].AroonTimingDict[date]]
                   price = stockDataDict[ticker].closePricesDict[date]
                   type = 'short'
                   buyList.append([ticker,price,date,maxDuration,type,score])

    return buyList

def mainSell(date,stockDataDict,tickerList,parameters,portfolio):

    transactionList = []
    indices = []

    limitSell = eval(parameters[2]) #0.02
    
    for i in range(len(portfolio)):
        ticker = portfolio[i][0]
        buyPrice = portfolio[i][1]
        buyDate = portfolio[i][2]
        maxDuration = portfolio[i][3]
        type = portfolio[i][4]
        score = portfolio[i][5]
        allDates2 = stockDataDict[ticker].dates2
        
        sell = False
        ##Selldate en sellprice hier
        if date in allDates2:
            ## Sell method hier
            index1 = np.where(allDates2==buyDate)[0][0]
            index2 = np.where(allDates2==date)[0][0]

            if type == 'long':
                if stockDataDict[ticker].AroonTimingDict[date] < 0:
                    sell = True
                if stockDataDict[ticker].MACDScoreiDict[date] < 0:
                    sell = True
                if (index1 - index2) > maxDuration:
                    sell = True
                if stockDataDict[ticker].closePrices[index2] < max(stockDataDict[ticker].closePrices[index2:index1+1])*(1-limitSell):
                    sell = True
                    
            if type == 'short':
                if stockDataDict[ticker].AroonTimingDict[date] > 0:
                    sell = True
                if stockDataDict[ticker].MACDScoreiDict[date] > 0:
                    sell = True
                if (index1 - index2) > maxDuration:
                    sell = True
                if stockDataDict[ticker].closePrices[index2] > min(stockDataDict[ticker].closePrices[index2:index1+1])*(1+limitSell):
                    sell = True
            
            if sell:
                sellDate = date
                sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
                transactionList.append([ticker,buyPrice,buyDate,maxDuration,type,score,sellPrice,sellDate])
                indices.append(i)
                   
    return transactionList,indices


### temporary ###

## ##Inladen van alle tickers
##tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
## ##run method
##buyList,stockDataDict = main('2015-08-18',{},tickerList)
