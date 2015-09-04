import sys
sys.path.insert(0, '../General')
from stockClass import Stock
sys.path.insert(0, '../Methods')
import method1 as method

def mainBuy(date,stockDataDict,tickerList):

    buyParameters = [3,6]
    
    if stockDataDict == {}:
        buyList,stockDataDict = method.mainBuy(date,{},tickerList,buyParameters)
    else:
        buyList = method.mainBuy(date,stockDataDict,tickerList,buyParameters)

    return buyList,stockDataDict

def mainSell():
    
    sellParameters = [-0.1,0.1,-0.1]

    return 'lol'

def mainSellSim(stockDataDict,totalBuyList):

    sellParameters = [-0.1,0.1,-0.1]

    transactionList = method.mainSellSim(stockDataDict,totalBuyList,sellParameters)

    return transactionList
