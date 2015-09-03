import numpy as np
import sys
sys.path.insert(0, '../General')
from stockClass import Stock


def mainBuy(date,stockDataDict,tickerList,parameters):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: date = welke dag geanalyseerd moet worden
               parameters = [limitscore voor MACD,duration]
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """

    limitScore = parameters[0]
    duration = parameters[1]
    
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

            ## HIER Methode inserten
            # Voorwaarde om te kopen en toevoegen aan de buyList
            if stockDataDict[ticker].MACDScoreiDict[date] > limitScore:
               score = stockDataDict[ticker].MACDScoreiDict[date]
               price = stockDataDict[ticker].closePricesDict[date]
               #date = stockDataDict[ticker].dates[entry]
               buyList.append([ticker,price,date,duration,score])


    
    ## to reduce the data package that has to be transferred       
    if firstTime == 1:
        return buyList,stockDataDict
    else:
        return buyList


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
