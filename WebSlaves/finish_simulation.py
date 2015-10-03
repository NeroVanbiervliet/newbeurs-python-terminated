# @params argv[1]=simulation id, argv[2]=new status, argv[3]=gain, argv[4]=return
from sys import argv
# om import te kunnen doen moet package toegevoegd worden aan python path
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from SQL.DatabaseInteraction import DatabaseInteraction

simulationId = argv[1]
newStatus = argv[2]
totalGain = argv[3]
totalReturn = argv[4]

dbInt = DatabaseInteraction('backtest_real','webapp')
dbInt.finaliseSimulation(simulationId, newStatus,totalGain,totalReturn)
