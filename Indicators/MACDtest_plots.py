import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../General')
from stockClass import Stock

## Input ##
ticker = 'AAPL'
start = 200
end = 400

## generate graphs
stock = Stock(ticker)
stock.generateMACD()

plt.subplot(2,1,1)
plt.plot(stock.closePrices[start:end])

plt.subplot(2,1,2)
plt.plot(stock.MACDi[start:end])
plt.plot(stock.MACDScorei[start:end])
plt.plot(stock.MACDSignali[start:end])

plt.show()
