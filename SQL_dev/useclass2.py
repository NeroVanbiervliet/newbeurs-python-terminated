#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

dbObject = DatabaseInteraction('backtest_real','webapp')
result = dbObject.getTickerList('{market=ASX,location=thuis}');
for ticker in result:
    print ticker



