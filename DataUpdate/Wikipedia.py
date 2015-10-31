import urllib2
import json
import sys
import os
import numpy as np
import time
import datetime

# navigeer naar directory van deze file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# navigeer een naar boven
os.chdir('../')
sys.path.insert(0, 'SQL')
from DatabaseInteraction import DatabaseInteraction 

# navigeer naar map waar data staat en moet geupdate worden
os.chdir('data/wikiData/')

# start timer
startTime = time.time()

# get list of wikipedia articles to check
dbInt = DatabaseInteraction("backtest_real")
[columnNames, queryResult] = dbInt.executeQuery("SELECT STK.ticker, STC.value FROM stockCategory STC JOIN stock STK ON STC.stock = STK.id  WHERE criterium='wikipedia'")

# generate lists of tickers and lists of wikipedia articles
tickerList = []
articleList = []
for row in queryResult:
	tickerList.append(row[0])
	articleList.append(row[1])
	
# number of http requests to do in a batch
chunkSize = 50. 

# website root
webRoot = "http://stats.grok.se/json/en/"

print "---------------------------"
print "|starting Wikipedia update|"
print "---------------------------"
print str(len(articleList)) + " stocks to update"

# get current date
currentDate = datetime.datetime.now().date() 

# zet maximum datum die mag gedownload worden
# TODO voor het gemak voorlopig 20 dagen minder dan de huidige dag, dan is de data er zeker

maximumDate = currentDate - datetime.timedelta(days=20)

[maximumYear,maximumMonth,maximumDay] = str(maximumDate).split("-")
maximumYear = int(maximumYear)
maximumMonth = int(maximumMonth)
maximumDay = int(maximumDay)

# error list 
totalErrorList = []

# number of http requests
numHttpRequests = 0

# loop over different articles (=tickers)
for articleId in range(0,len(tickerList)):

	ticker = tickerList[articleId]

	dataList = []
	errorList = []

	# retrieving current state of the data of this stock
	query = "SELECT STC.value FROM stockCategory STC JOIN stock STK ON STK.id = STC.stock WHERE STK.ticker='%s' AND STC.criterium='wikipediaStatus'" % ticker
	[columnNames, queryResult] = dbInt.executeQuery(query)

	dataStatus = queryResult[0][0]

	# data that was already in file and that will be rewritten into file after appending new date
	oldData = []

	if dataStatus == "ok": # existing data is okay, just add new data
		# read all data of file into array
		localFile = open(ticker + ".txt", 'r')	
		localFile.readline() # eerste lijn skippen, die toont toch enkel formaat van data aan		
		oldData = localFile.readlines()
		oldData = [x.strip('\n') for x in oldData] # \n strippen van elke string
		localFile.close()

		# retrieve current last date available in file				
		mostRecentDate = oldData[0].split(",")[0]
		[minimumYear,minimumMonth,minimumDay] = mostRecentDate.split("-")
		minimumYear = int(minimumYear)
		minimumMonth = int(minimumMonth)
		minimumDay = int(minimumDay)

	else: # existing data is not okay, delete file and redownload everything			
		# lower date limit (wikipedia gaat niet verder terug in de tijd)
		minimumYear = 2007
		minimumMonth = 12
		minimumDay = 10		
	
	# construct year and month strings to iterate over
	datesToDo = []
	
	# alle data tussen min en max toevoegen aan datesToDo	
	minimumDate = datetime.date(minimumYear,minimumMonth,minimumDay)
	maximumDate = datetime.date(maximumYear,maximumMonth,maximumDay)
	
	delta = maximumDate - minimumDate

	for i in range(delta.days + 1):
		dateToAdd = str(minimumDate + datetime.timedelta(days=i))
		# bijknippen 
		dateToAdd = dateToAdd[0:4]+dateToAdd[5:7]
		if dateToAdd not in datesToDo:
			datesToDo.append(dateToAdd)

	# loop over different dates to do
	for yearMonth in datesToDo:
		
		print yearMonth

		url = webRoot + yearMonth + "/" + articleList[articleId] 

		# increase number of http requests
		numHttpRequests += 1

		if (numHttpRequests % chunkSize) == 0:		
			print 'sleep' 
			# na een aantal requests even slapen om server niet te overloaden zodat we geweigerd worden
			time.sleep(.25)

		try:
			site = urllib2.urlopen(url)
			rawJSONData = site.read()
			rawData = json.loads(rawJSONData)
			rawViewsData = rawData['daily_views']

			newData = []

			for key in rawViewsData.keys():
				newData.append(str(key) + "," + str(rawViewsData.get(key)))

			# sorteer alfabetisch zodat datums in juiste volgorde zijn
			newData.sort()			

		except urllib2.HTTPError:
			errorList.append(ticker + "," + articleList[articleId] + "," + str(yearMonth))

		except urllib2.URLError:
			print "OAK_ERROR: no internet connection?"
			errorList.append("OAK_ERROR: no internet connection?")
			break;

		except urllib2.BadStatusLine:
			print "OAK_ERROR: random error bij data halen van site"
			errorList.append("OAK_ERROR: random error bij data halen van site")
			break;
		
		if yearMonth == str(maximumYear)+str(maximumMonth): # we zitten in de laatste maand die moet gedaan worden
			
			maximumDate = "%s-%s-%s" % (maximumYear,maximumMonth,maximumDay)
			
			for dataItem in newData:
				# checken of het item niet na de maximumDate valt
				if dataItem <= maximumDate:
					dataList.insert(0,dataItem)

		elif yearMonth == str(minimumYear)+str(minimumMonth): # we zitten in de eerste maand die moet gedaan worden
			
			minimumDate = "%s-%s-%s" % (minimumYear,minimumMonth,minimumDay)

			for dataItem in newData:
				# checken of het item niet voor de miniumDate valt
				if dataItem >= str(minimumDate[0:6]):
					dataList.insert(0,dataItem)
		
		else: # normale maand waarvan alle items mogen toegevoegd worden		

			for dataItem in newData:
				dataList.insert(0,dataItem)		
		
			

	# na ophalen alle data wegschrijven naar file
	localFile = open(ticker + ".txt", 'w')
	localFile.write("Date, NumberOfViews\n")
	for dataItem in dataList: 
		localFile.write(dataItem + "\n")
	# reinstert old data
	for dataItem in oldData:
		localFile.write(dataItem + "\n")
	localFile.close()

	# add errors to totalErrorList
	totalErrorList.extend(errorList)
	
	# data is corrupt if an error occured
	if len(errorList) > 0:
		dbInt.editStockCategory(ticker, "wikipediaStatus", "corrupt")
	else: # data dik in orde
		dbInt.editStockCategory(ticker, "wikipediaStatus", "ok")
	

endTime = time.time()

# check if any errors occured
numOfErrors = len(errorList)
if(numOfErrors) > 0:

	# print errors to file
	os.chdir('../../DataUpdate')
	localFile = open("wiki.error", 'w')
	localFile.write("Ticker, ArticleName, YearAndMonth\n")

	for error in errorList: 
		localFile.write(error + "\n")
		
	localFile.close()

	print numOfErrors," errors occured"
	print "You can review them in the file",dname + "/wiki.error"

else: # geen errors

	# print to error file (empty)

	localFile = open("wiki.error", 'w')
	localFile.close()

	print "No errors occured."

print "Total http requests: ",numHttpRequests
print "Total process time : ",(endTime-startTime)," seconds"
