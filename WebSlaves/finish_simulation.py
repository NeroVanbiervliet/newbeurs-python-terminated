# @params argv[1]=simulation id, argv[2]=new status, argv[3]=return, argv[4]=gain
from sys import argv
from ..SQL.DatabaseInteraction import DatabaseInteraction

simulationId = argv[1]
newStatus = argv[2]

# NEED veranderen dat webapp user is, of webslaves
dbInt = DatabaseInteraction('backtest_real')

# NEED functie schrijven in databaseinteraction class
# NEED enkel failed als hij niet al stopped is! (checken eerst)
# NEED return en gain ook meegeven
dbInt.finaliseSimulation(self, simulationId, newStatus)
