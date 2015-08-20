import numpy as np
import random

def Value(closePrices,dates):
    
    return [0,0]

def Score(closePrices,dates):
    MACDScore = []
    for i in range(len(closePrices)):
        if random.randint(0,10) == 1:
            MACDScore.append(2)
        else:
            MACDScore.append(0)
        
    return MACDScore
