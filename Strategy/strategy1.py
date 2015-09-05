import sys
sys.path.insert(0, '../General')
from stockClass import Stock
sys.path.insert(0, '../Methods')
import method1 as method

def generateData(tickerList):

    stockDataDict = method.generateData(tickerList)

    return stockDataDict

def mainBuy(date,stockDataDict,tickerList):

    buyParameters = [3,6]
    
    buyList = method.mainBuy(date,stockDataDict,tickerList,buyParameters)

    return buyList

def mainSell(date,stockDataDict,tickerList,portfolio):
    
    sellParameters = []
    
    transactionList,indices = method.mainSell(date,stockDataDict,tickerList,sellParameters,portfolio)

    return transactionList,indices


