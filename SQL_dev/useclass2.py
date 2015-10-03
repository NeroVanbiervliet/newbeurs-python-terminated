#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

dbObject = DatabaseInteraction('backtest_real','webapp')
dbObject.finaliseSimulation(26,"done","0.2","0.3")

