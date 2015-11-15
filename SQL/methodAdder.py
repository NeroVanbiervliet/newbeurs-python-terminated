from DatabaseInteraction import DatabaseInteraction

dbInt = DatabaseInteraction('backtest_real')
dbInt.addMethod("methodTA1","MACD, Aroon, OBV and RSI combined")
dbInt.addStrategy("Technical Analysis 1","methodTA1",[6,3])
