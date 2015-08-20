import numpy as np
import sys
sys.path.insert(0, '../General')
from stockClass import stock

## Inputs are arguments, or stock slection

def method1(entry,stockDataDict):
    """ Dit is methode 1 die aandelen koopt en verkoopt onder bepaalde voorwaardes
        Input: entry = hoeveel dagen terug in de tijd
        Output: buyList = zegt welke aandelen gekocht worden en voor hoe lang
        """
    
    buyList = []
    #buyList = [[name,price,date,duration]]

    # Inladen van alle tickers
    tickerList = np.loadtxt('../data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')

    if stockDataDict == {}:
        # Alle data creeren voor de geselecteerde aandelen
        for ticker in tickerList[:100]:
            stockDataDict[ticker] = stock(ticker)
            stock.generateMACD(stockDataDict[ticker])

    # Alle aandelen overlopen 
    for ticker in stockDataDict:
        # Voorwaarde om te kopen en toevoegen aan de buyList
        if stockDataDict[ticker].MACDScorei[entry] > 0:
           name = stockDataDict[ticker].name
           price = stockDataDict[ticker].closePrices[entry]
           date = stockDataDict[ticker].dates[entry]
           duration = 6
           buyList.append([name,price,date,duration])

    return buyList,stockDataDict
## Outputs are stocks that have to be bought with some details why, how long etc

buyList,stockDataDict = method1(0,{})
