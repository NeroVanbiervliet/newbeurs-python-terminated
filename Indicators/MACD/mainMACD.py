import numpy as np
import random

def Value(closePrices,dates):
    output = [0,0]
    return output,dict(zip(dates[:len(output)], output))

def Score(closePrices,dates):
    MACDScore = []
    for i in range(len(closePrices)):
        if random.randint(0,10) == 1:
            MACDScore.append(2)
        else:
            MACDScore.append(0)
        
    return MACDScore,dict(zip(dates[:len(MACDScore)], MACDScore))
