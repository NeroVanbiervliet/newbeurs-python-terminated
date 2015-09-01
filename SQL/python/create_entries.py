#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

print 'Test entries will be added to database'

dbObject = DatabaseInteraction('backtest_real')


# users
# pass fromzerotoone
dbObject.addUser("beurs","$2a$12$rBOjgBqaorleheA2XuospuN65sO5XsUUHddygO4z8Hcd2eIA.vNPe")

# stocks
dbObject.addStock("apple","AAPL","Nasdaq")
dbObject.addStock("oak","OAK","Euronext")

# methods
dbObject.addMethod("fundamentalist","geen argumenten jongeuh")
dbObject.addMethod("indexvolger","geef als string de index mee die je wil volgen")

# strategies

dbObject.addStrategy("fundamentAgressief","fundamentalist","")
dbObject.addStrategy("bel20volger","indexvolger","bel20")

# simulation

# INSERT INTO simulation(name,description,owner,strategy,totalGain,totalReturn,status,progress) VALUES('denaam','descip0','1','1','3','4','running','40');


print 'Done'
