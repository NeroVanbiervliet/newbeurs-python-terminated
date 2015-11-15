import numpy as np

def Value(closePrices,period1,period2):

    #period1 = 12
    #period2 = 26
    
    MACD = []
    EMA12 = EMA(closePrices,12)
    EMA26 = EMA(closePrices,26)

    for i in range(min(len(EMA12),len(EMA26))):
        MACD.append(EMA12[i]-EMA26[i])
    
    return MACD

def Score(MACD,closePrices,period3):

    scoreList = []
    signal = SignalLine(MACD,period3)
    
    score = 0
    diffPrev = 0
    cross = 0
    for i in range(len(signal)):
        j = (len(signal)-1) - i

        diff = MACD[j] - signal[j]

        if cross == 2:
            cross = 0
            score += diff
        
        if cross == 1:
            score += diff
            cross += 1

        if diff*diffPrev < 0:
            score = diff
            cross = 1
            
        if cross == 0:
            score = 0
        
        diffPrev = diff
        scoreList.append(score*8.)
        
    return scoreList[::-1]

def SignalLine(MACD,period3):

    #period3 = 9
    signalLine = EMA(MACD,period3)

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
