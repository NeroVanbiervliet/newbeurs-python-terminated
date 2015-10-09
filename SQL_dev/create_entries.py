#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

print 'Test entries will be added to database'

dbObject = DatabaseInteraction('backtest_real')


# users
dbObject.addUser("nero","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbObject.addUser("michiel","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")
dbObject.addUser("baerto","$2a$12$/MugNnVIjdLd1TnshSyK2eXp.jM3lGM1GipTdFNTuwTHvFimPgCbu")

# stocks
dbObject.addStock("apple","AAPL","Nasdaq")
dbObject.addStock("oak","OAK","Euronext")

# stockCategory
dbObject.addStockToCategory("OAK","locatie","lieven zijn bureau")
dbObject.addStockToCategory("AAPL","locatie","amerika")

# methods
dbObject.addMethod("fundamentalist","geen argumenten jongeuh")
dbObject.addMethod("indexvolger","geef als string de index mee die je wil volgen")

# strategies

dbObject.addStrategy("fundamentAgressief","fundamentalist","")
dbObject.addStrategy("bel20volger","indexvolger","bel20")

# add data sources
dbObject.addDataSource("yahoo.py","prices of all stocks")
dbObject.addDataSource("wikipedia.py","number of views")

# simulation

# INSERT INTO simulation(name,description,owner,strategy,totalGain,totalReturn,status,progress) VALUES('denaam','descip0','1','1','3','4','running','40');

print 'Done'
