import numpy as np
import sys
sys.path.insert(0, '../General')
from stockClass import Stock

def generateData(tickerList):
    stockDataDict = {}
    for ticker in tickerList:
            stockDataDict[ticker] = Stock(ticker)
            Stock.generateMACD(stockDataDict[ticker])
            
    return stockDataDict

def mainBuy(date,stockDataDict,tickerList,buyParameters):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: date = welke dag geanalyseerd moet worden
               parameters = [limitscore voor MACD,duration]
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """

    limitScore = buyParameters[0]
    duration = buyParameters[1]
    
    buyList = []
    
    # Alle aandelen overlopen 
    for ticker in stockDataDict:
        #check if data is available for that date
        allDates = stockDataDict[ticker].dates
        if date in allDates and date in allDates[:len(stockDataDict[ticker].MACDScorei)]:

            ## HIER Methode inserten
            # Voorwaarde om te kopen en toevoegen aan de buyList
            if stockDataDict[ticker].MACDScoreiDict[date] > limitScore:
               score = stockDataDict[ticker].MACDScoreiDict[date]
               price = stockDataDict[ticker].closePricesDict[date]
               #date = stockDataDict[ticker].dates[entry]
               buyList.append([ticker,price,date,duration,score])

    return buyList

def mainSell(date,stockDataDict,tickerList,sellParameters,portfolio):

    transactionList = []
    indices = []
    #TODO: voeg een sell definitie toe die in real life wordt gebruikt
    for i in range(len(portfolio)):
        ticker = portfolio[i][0]
        buyPrice = portfolio[i][1]
        buyDate = portfolio[i][2]
        duration = portfolio[i][3]
        allDates = stockDataDict[ticker].dates
        
        ##Selldate en sellprice hier
        if date in allDates:
            index1 = np.where(allDates==buyDate)[0][0]
            index2 = np.where(allDates==date)[0][0]
            if (index1 - index2) >= duration:
                sellDate = date
                sellPrice = stockDataDict[ticker].closePricesDict[sellDate]
                transactionList.append([ticker,buyPrice,buyDate,duration,portfolio[i][4],sellPrice,sellDate])
                indices.append(i)
                   
    return transactionList,indices

def mainSellSim(stockDataDict,buyList,parameters):
    
    transactionList = []
    lowerLimit = parameters[0]
    upperLimit = parameters[1]
    midLimit = parameters[2]
    
    for i in range(len(buyList)):
        for j in range(len(buyList[i])):
            ticker = buyList[i][j][0]
            buyPrice = buyList[i][j][1]
            buyDate = buyList[i][j][2]
            duration = buyList[i][j][3]
            allDates = stockDataDict[ticker].dates

            ##Selldate en sellprice hier
            
            index = np.where(allDates==buyDate)[0][0]
            notSold = True
            for k in range(1,duration):
                date = allDates[index - k]
                yesterday = allDates[index - k + 1]
                # Als er bepaalde boven en onder limieten bereikt zijn, verkopen
                if ((stockDataDict[ticker].closePricesDict[date] - buyPrice)/buyPrice < lowerLimit \
                    or (stockDataDict[ticker].closePricesDict[date] - buyPrice)/buyPrice > upperLimit) and notSold :
                    sellDate = date
                    notSold = False
                    
                # Als het aandeel daalt met midlimit, verkopen
                if ((stockDataDict[ticker].closePricesDict[date] - stockDataDict[ticker].closePricesDict[yesterday])/ \
                    stockDataDict[ticker].closePricesDict[yesterday]) < midLimit and notSold:
                    sellDate = date
                    notSold = False
                    
            if notSold:
                sellDate = allDates[index - duration]
                
            sellPrice = stockDataDict[ticker].closePricesDict[sellDate]

            ##
            
            transactionList.append([ticker,buyPrice,buyDate,duration,buyList[i][j][4],sellPrice,sellDate])

    return transactionList

### temporary ###

## ##Inladen van alle tickers
##tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
## ##run method
##buyList,stockDataDict = main('2015-08-18',{},tickerList)
