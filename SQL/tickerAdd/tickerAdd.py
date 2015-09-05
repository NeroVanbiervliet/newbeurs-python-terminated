import numpy as np

#stockList = np.loadtxt('tickers.txt', delimiter=',', skiprows=0, usecols=(0,1,2), unpack=False,dtype = 'str')[:100]
stockList = []
z = open('tickers.txt', 'r')
for line in z.readlines():
    line =line.replace("\n", "")
    cols = line.split('\t')
    
    stockList.append(cols)
z.close()

