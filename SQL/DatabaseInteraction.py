#!/usr/bin/python
import MySQLdb
import _mysql_exceptions


class DatabaseInteraction:
    """A class to interact with the oak beurs database (c) Nero"""

    # variables here declared are class variables, they are common for all objects and each object has a pointer to the same value!
    userList = ['root','webapp','python']
    passwordList = ['crvfttngdsntwrk','frmzrtn5894rndm','twpntzvnsbtrdndr']

    # constructor

    def __init__(self, dbName, dbUser=None):

        # variables declared in the constructor are property of the object
        self.dbName = dbName
        self.dbHost = 'localhost'

        if (dbUser is None):  # default account is python
            # local var needed further in constructor
            dbUser = 'python'
            self.dbUser = dbUser
        else:
            self.dbUser = dbUser

        # get password
        if dbUser in self.userList:
            userIndex = self.userList.index(self.dbUser)
            self.dbPassword = self.passwordList[userIndex]

        else:  # user is not known, set password = ""
            self.dbPassword = ""

    # functions

    # returns the mandatory last print statement of every method
    def getTerminator(self):
        return "And Now His Watch is Ended"

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
    # sample structuur van dataRows:
    # ((1L, 'fundamentAgressief', 1L, 1, ''), (2L, 'bel20volger', 2L, 1, 'bel20'))
    # is dus list van lists, geen dictionaries
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
        return [columnNames, queryResult]

    # adds a stock to the stocks table
    # examples:
    # name = apple
    # ticker = AAPL
    # market = Nasdaq
    def addStock(self, name, ticker):

        query = ("INSERT INTO stock(name, ticker) "
                 "VALUES (\'%s\',\'%s\');") % (name, ticker)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe stock in de database mislukt. Ticker bestaat al in database"
            # exception herthrowen TODO eigen exception throwen met message hierboven?
            raise

    # adds a stock to a category
    def addStockToCategory(self,ticker,criterium,value):

        query = ("INSERT INTO stockCategory(stock,criterium,value) "
                 "VALUES ((SELECT id FROM stock WHERE ticker=\'%s\'),\'%s\',\'%s\');") % (ticker,criterium,value)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe stockCategory entry in de database mislukt. Mogelijk probleem: ticker bestaat niet in database"
            # exception herthrowen TODO eigen exception throwen met message hierboven?
            raise

    # returns a list containing all tickers present in the stocks table
    def getAllTickers(self):

        query = "SELECT ticker FROM stock"
        [columnNames, queryResult] = self.executeQuery(query)

        # gegevens herschikken
        result = []
        for ticker in queryResult:
            result.append(ticker[0])

        return result

    # returns a list of tickers
    # the stocks moeten aan de condition voldoen
    # de condition wordt beschreven aan de hand van entries in de stockCategory table
    def getTickerList(self,condition):

        # JOIN <=> INNER JOIN
        query = ("SELECT ticker FROM stock JOIN stockCategory ON stock.id = stockCategory.stock "
                 "WHERE %s;") % (condition)

        try:
            return self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Mogelijk probleem: geen idee"
            # exception herthrowen TODO eigen exception throwen met message hierboven?
            raise

    # returns stock info in a dictionary
    def getStockInfo(self, ticker):

        query = "SELECT * FROM stock WHERE ticker=\'%s\'" % (ticker)
        [columnNames, queryResult] = self.executeQuery(query)

        # data in dictionary gieten
        result = {}

        # columnames structure is -> (('id', 3, 1, 11, 11, 0, 0), ('name', 253, 5, 30, 30, 0, 0), ('ticker', 253, 4, 10, 10, 0, 1)
        for i in range(0, len(columnNames)):
            # add to dictionary, gaat er van uit dat ticker uniek is dus enkel eerste rij van queryResult wordt onderzocht
            result[columnNames[i][0]] = queryResult[0][i]

        return result

    # adds a method to the database
    # @param name de naam van de methode, zelfde als directorynaam van methode!
    # @param description beschrijving van de methode, inclusief de argumenten die mee moeten gegeven worden bij uitvoeren van script!
    def addMethod(self, name, description):

        query = ("INSERT INTO method(name, description) "
                 "VALUES (\'%s\',\'%s\');") % (name, description)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe stock in de database mislukt. Methodenaam bestaat al in database"
            # exception herthrowen TODO eigen exception throwen met message hierboven
            raise

    # returns method info in a dictionary
    def getMethodInfo(self, name):

        query = "SELECT * FROM method WHERE name=\'%s\'" % (name)
        [columnNames, queryResult] = self.executeQuery(query)

        # data in dictionary gieten
        result = {}

        # columnames structure is -> (('id', 3, 1, 11, 11, 0, 0), ('name', 253, 5, 30, 30, 0, 0), ('ticker', 253, 4, 10, 10, 0, 1)
        for i in range(0, len(columnNames)):
            # add to dictionary, gaat er van uit dat ticker uniek is dus enkel eerste rij van queryResult wordt onderzocht
            result[columnNames[i][0]] = queryResult[0][i]

        return result

    # adds a user to the database
    # only use this in development! a hashed password is required, but this must be generate by a JSP script using bcrypt
    # users must be added in the web application, not in python
    def addUser(self, userName, passwordHashed):

		# TODO hashing hier doen, passwoord als argument meegeven

        query = ("INSERT INTO user(name, passwordHashed) "
                 "VALUES (\'%s\',\'%s\');") % (userName, passwordHashed)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe user in de database mislukt. UserName bestaat al in database"
            # exception herthrowen TODO eigen exception throwen met message hierboven
            raise



    # adds a strategy to the database
    # TODO also add entry in strategyEditHistory
    def addStrategy(self, strategyName, methodName, parameters):

        # method info ophalen om id te vinden uit name
        # TODO exception voor als method niet voorkomt in db
        methodInfo = self.getMethodInfo(methodName)

        query = ("INSERT INTO strategy(name, method, parameters) "
                 "VALUES (\'%s\',\'%s\',\'%s\');") % (strategyName, methodInfo.get('id'), parameters)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe strategy in de database mislukt. StrategyName bestaat al in database"
            # exception herthrowen TODO eigen exception throwen met message hierboven
            raise

    # adds given PID to a simulation record
    def addPidToSimulation(self, simulationId, simulationPid):

        query = ("UPDATE simulation "
                 "SET pid='%s' "
                 "WHERE id=%s;") % (simulationPid,simulationId)

        try:
            self.executeQuery(query)
        except _mysql_exceptions:
            print "OAK_ERROR: PID toevoegen aan simulation in de database mislukt. Waarschijnlijk bestaat het sim id niet in de db"
            # exception herthrowen TODO eigen exception throwen met message hierboven
            raise

    #
    def finaliseSimulation(self,simulationId,status,totalGain,totalReturn):

	# checken of de status niet al stopped is
	# TODO kan netter met een executeQuery en een WHERE id = ...
        
		[columnNames, dataRows] = self.getAllTableEntries("simulation")
		for dataRow in dataRows:
			# juiste rij gevonden, int() nodig omdat simulationId komt van bash script en dat is dan een string, geen int!  
			if dataRow[0] == int(simulationId):            
				if dataRow[9] == "stopped":
					status = "stopped"
				break

		query = ("UPDATE simulation "
				"SET status='%s', totalGain='%s', totalReturn='%s', timestampEnd=NOW()"
				"WHERE id='%s';") % (status,totalGain,totalReturn,simulationId)

		try:
			self.executeQuery(query)
		except _mysql_exceptions:
			print "OAK_ERROR: status updaten van de simulation in de database mislukt. Waarschijnlijk bestaat het sim id niet in de db"
			# exception herthrowen TODO eigen exception throwen met message hierboven
			raise

    # adds a data source
    def addDataSource(self, scriptFile, description):

        query = ("INSERT INTO dataStatus(script,description) "
                 "VALUES (\'%s\',\'%s\');") % (scriptFile,description)

        try:
            self.executeQuery(query)
        except _mysql_exceptions.IntegrityError:
            print "OAK_ERROR: Creatie van nieuwe user in de database mislukt. UserName bestaat al in database"
            # exception herthrowen TODO eigen exception throwen met andere message dan hierboven
            raise
