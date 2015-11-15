import numpy as np

def Value(closePrices,period1):

    AroonUp = []
    AroonDown = []

    maxEntry = 9999
    minEntry = 9999

    for i in range(len(stockClose)-period1):
        j = len(stockClose)-period1-1-i
        
        if stockClose[j] > max(stockClose[j+1:j+1+period1]):
            maxValue = stockClose[j]
            maxEntry = j
        if stockClose[j] < min(stockClose[j+1:j+1+period1]):
            minValue = stockClose[j]
            minEntry = j
            
        AroonUpValue = (period-(maxEntry-j))/float(period1)*100.
        AroonDownValue = (period-(minEntry-j))/float(period1)*100.
        
        AroonUp.append(max(AroonUpValue,0))
        AroonDown.append(max(AroonDownValue,0))
    
    
    return AroonUp[::-1],AroonDown[::-1]


def Timing(AroonUp,AroonDown):
    
    score = 0
    timing = []
    for i in range(1,len(AroonUp)):
        j = len(AroonUp)-1-i
        score = 0
        if AroonUp[j] > 80 and AroonDown[j] < 30:
            score = 1
        if AroonDown[j] > 80 and AroonUp[j] < 30:
            score = -1
        if AroonUp[j+1] < 40 and AroonUp[j] > 90:
            score = 2
        if AroonDown[j+1] < 40 and AroonDown[j] > 90:
            score = -2
            
        timing.append(score)
    
    return timing[::-1]
