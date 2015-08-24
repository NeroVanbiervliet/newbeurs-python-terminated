import numpy as np
import random

def Value(closePrices):

    period1 = 12
    period2 = 26
    
    MACD = []
    EMA12 = EMA(closePrices,12)
    EMA26 = EMA(closePrices,26)

    for i in range(min(len(EMA12),len(EMA26))):
        MACD.append(EMA12[i]-EMA26[i])
    
    return MACD

def Score(MACD,closePrices):

    scoreList = []
    signal = SignalLine(MACD)
    
    for i in range(len(signal)):
        scoreList.append((MACD[i] - signal[i])/closePrices[i]*1000.)
        
    return scoreList

def SignalLine(MACD):

    period = 9
    signalLine = EMA(MACD,period)

    return signalLine

def EMA(list,period):

    result = []
    multiplier = 2./(period+1.)
    inverse = list[::-1]
    start = np.mean(inverse[:period])
    result.append(start)
    for i in range(len(inverse)-period):
        value = (inverse[i+period] - result[i])*multiplier + result[i]
        result.append(value)
    
    return result[::-1]
