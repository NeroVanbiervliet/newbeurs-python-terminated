# @params argv[1]=simulation id, argv[2]=pid
from sys import argv
from ..SQL.DatabaseInteraction import DatabaseInteraction

simulationId = argv[1]
pid = argv[2]

dbInt = DatabaseInteraction('backtest_real','webapp')

dbInt.addPidToSimulation(self, simulationId, pid)
