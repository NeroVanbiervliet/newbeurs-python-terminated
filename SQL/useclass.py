#!/usr/bin/python
from DatabaseInteraction import DatabaseInteraction

dbObject = DatabaseInteraction()
dbObject.getAllTableEntries("users")
print '------------------------'
dbObject.getTableNames()

