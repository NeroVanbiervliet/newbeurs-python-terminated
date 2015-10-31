import numpy as np
import sys
sys.path.insert(0, 'General')
from stockClass import Stock

def generateData(tickerList):
    stockDataDict = {}
    for ticker in tickerList:
            stockDataDict[ticker] = Stock(ticker)
            Stock.generatePID(stockDataDict[ticker])
            
    return stockDataDict

def mainBuy(date,stockDataDict,tickerList,buyParameters):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: date = welke dag geanalyseerd moet worden
               
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """

    limitScore = buyParameters[0]
    duration = buyParameters[1]
    
    buyList = []
    
    # Alle aandelen overlopen 
    for ticker in stockDataDict:
        #check if data is available for that date
        if stockDataDict[ticker].status:
            allDates = stockDataDict[ticker].dates
            if date in allDates and date in stockDataDict[ticker].datesTrendScore:
                
                ## HIER Methode inserten
                # Voorwaarde om te kopen en toevoegen aan de buyList
                if stockDataDict[ticker].dailyGainDict[date] > 1.06: # 6 procent verschil met vorige dag
                   score = stockDataDict[ticker].dailyGainDict[date]
                   price = stockDataDict[ticker].closePricesDict[date]
                   #date = stockDataDict[ticker].dates[entry]
                   type = 'long'
                   buyList.append([ticker,price,date,duration,type,score])

    return buyList

def mainSell(date,stockDataDict,tickerList,sellParameters,portfolio):

    transactionList = []
    indices = []
    
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
                transactionList.append([ticker,buyPrice,buyDate,duration,type,portfolio[i][4],sellPrice,sellDate])
                indices.append(i)
                   
    return transactionList,indices

##### temporary ###

## ##Inladen van alle tickers
##tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
## ##run method
##buyList,stockDataDict = main('2015-08-18',{},tickerList)
