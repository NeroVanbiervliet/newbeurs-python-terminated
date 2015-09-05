# @params argv[1]=simulation id, argv[2]=pid
from sys import argv
# om import te kunnen doen moet package toegevoegd worden aan python path
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from SQL.DatabaseInteraction import DatabaseInteraction

simulationId = argv[1]
pid = argv[2]

dbInt = DatabaseInteraction('backtest_real','webapp')

dbInt.addPidToSimulation(simulationId, pid)
