# @params argv[1]=simulation id, argv[2]=pid
from sys import argv
from ..SQL.DatabaseInteraction import DatabaseInteraction

simulationId = argv[1]
pid = argv[2]

# NEED veranderen dat webapp user is, of webslaves
dbInt = DatabaseInteraction('backtest_real')

dbInt.addPidToSimulation(self, simulationId, pid)
