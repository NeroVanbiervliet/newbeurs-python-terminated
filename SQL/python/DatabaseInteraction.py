#!/usr/bin/python
import MySQLdb
import _mysql_exceptions

class DatabaseInteraction:
	"""A class to interact with the oak beurs database (c) Nero"""
	
	# variables here declared are class variables, they are common for all objects and each object has a pointer to the same value!	
	userList = ['root','baerto','beurs']
	passwordList = ['lnrddvnc','baertdbpass','fromzerotoone']

	# constructor

	def __init__(self, dbUser = None):
		
		# variables declared in the constructor are property of the object
		self.dbName = 'oakTest'
		self.dbHost = 'localhost'

		if(dbUser is None): # default account is root TODO aanpassen
			# local var needed further in constructor
			dbUser = 'root'
			self.dbUser = dbUser
		else:
			self.dbUser = dbUser

		# get password
		if dbUser in self.userList:
			userIndex = self.userList.index(self.dbUser)
			self.dbPassword = self.passwordList[userIndex]
	
		else: # user is not known, set password = ""
			self.dbPassword = ""


	# functions

	# returns an array of all valid table names
	def getTableNames(self):
		
		query = "SHOW TABLES"	
		[columnNames, queryResult] = self.executeQuery(query)

		for row in queryResult:	
			print row[0]	

		return queryResult	

	# returns two arrays: [columnNames,dataRows]
	# a valid tableName is required, as can be obtained using the getTableNames() function
	def getAllTableEntries(self, tableName):

		query = "SELECT * FROM " + tableName
		return self.executeQuery(query)
		
	# executes a given query	
	def executeQuery(self, query):

		# open connection with database		
		conn = MySQLdb.connect(host=self.dbHost, user=self.dbUser, passwd=self.dbPassword, db=self.dbName)
		# get cursor object
		cur = conn.cursor() 

		# execute query
		cur.execute(query)

		# store result in local var
		columnNames = cur.description
		queryResult = cur.fetchall()

		# finish
		cur.close()
		conn.commit()
		conn.close()

		# return result
		return [columnNames,queryResult]


	# adds a stock to the stocks table
	# examples:
	# name = apple
	# ticker = AAPL
	# market = Nasdaq
	def addStock(self, name, ticker, market):
		
		query = ("INSERT INTO stocks(name, ticker, market) "
			"VALUES (\'%s\',\'%s\',\'%s\');") % (name,ticker,market)
		
		try:	
			self.executeQuery(query)
		except _mysql_exceptions.IntegrityError:
			print "OAK_ERROR: Ticker bestaat al in database"
			# exception herthrowen	TODO: goed dat programma failed door error? 		
			raise
	
	# returns a list containing all tickers present in the stocks table	
	def getTickerList(self):
		
		query = "SELECT ticker FROM stocks"
		[columnNames,queryResult] = self.executeQuery(query)
		
		# gegevens herschikken
		result = []		
		for ticker in queryResult:
			result.append(ticker[0])

		return result

	# returns stock info in a dictionary
	def getStockInfo(self, ticker):

		query = "SELECT * FROM stocks WHERE ticker=\'%s\'" % (ticker)
		[columnNames,queryResult] = self.executeQuery(query)

		# data in dictionary gieten
		result = {}		
		
		# columnames structure is -> (('id', 3, 1, 11, 11, 0, 0), ('name', 253, 5, 30, 30, 0, 0), ('ticker', 253, 4, 10, 10, 0, 1)
		for i in range(0,len(columnNames)):
			# add to dictionary, gaat er van uit dat ticker uniek is dus enkel eerste rij van queryResult wordt onderzocht
			result[columnNames[i][0]] = queryResult[0][i]

		return result

