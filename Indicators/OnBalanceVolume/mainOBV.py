import numpy as np

def Value(closePrices,volume):

    OBVList = []
    OBVValue = 0.
    dummy = closePrices[::-1]
    
    for i in range(1,len(dummy)):
        
        if dummy[i] > dummy[i-1]:
            OBVValue += volume[i]
            OBVList.append(OBVValue)

        elif dummy[i] < dummy[i-1]:
            OBVValue += -volume[i]
            OBVList.append(OBVValue)

        elif dummy[i] == dummy[i-1]:
            OBVValue += 0.
            OBVList.append(OBVValue)

    return OBVList[::-1]
            
            
def Score(OBVList,period1,period2):
    mini = min(OBVList)
    scoreList = []
    dummy = OBVList[::-1]
    for i in range(period2,len(dummy)):
        avg1 = np.mean(dummy[i-period1:i]) - mini
        avg2 = np.mean(dummy[i-period2:i]) - mini

        score = (avg1 - avg2)/avg2
        
        scoreList.append(score*100.)

        
    return scoreList[::-1]
