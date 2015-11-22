import numpy as np

sys.path.insert(0, 'Indicators/MACD')
import mainMACD as MACD
sys.path.insert(0, 'Indicators/Aroon')
import mainAroon as Aroon
sys.path.insert(0, 'Indicators/OnBalanceVolume')
import mainOBV as OBV


def mainBaert(closePrices,volume):

    buy = False

    AroonUp,AroonDown = Aroon.Value(closePrices,25)
    

    return buy,duration


def sellBaert(closePrices,volume):

    sell = False

    return sell
