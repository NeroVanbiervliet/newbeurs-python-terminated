import numpy as np

def Value(closePrices,period1):

    AroonUp = []
    AroonDown = []

    maxEntry = 9999
    minEntry = 9999

    for i in range(len(closePrices)-period1):
        j = len(closePrices)-period1-1-i
        
        if closePrices[j] > max(closePrices[j+1:j+1+period1]):
            maxValue = closePrices[j]
            maxEntry = j
        if closePrices[j] < min(closePrices[j+1:j+1+period1]):
            minValue = closePrices[j]
            minEntry = j
            
        AroonUpValue = (period1-(maxEntry-j))/float(period1)*100.
        AroonDownValue = (period1-(minEntry-j))/float(period1)*100.
        
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
