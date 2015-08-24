from os import listdir
from os.path import isfile, join

def getOccurrences(dir,numTabs):
	
	#tabstring generation
	tabString = ""
	for i in range(0,numTabs):
		tabString += "    " 	

	consoleOutput = ""
	
	totalNeed = 0
	totalTodo = 0	

	dirList = []
	fileList = []

	for item in listdir(dir):

		if isfile(join(dir,item)):
			fileList.append(item)
		else: # het is een dir
			dirList.append(item)

	# eerst dirs itereren
	for item in dirList:

		[currentNeed,currentTodo, currentConsoleOutput] = getOccurrences(join(dir,item),numTabs+1)
		
		if currentNeed>0 or currentTodo>0:
			totalNeed += currentNeed
			totalTodo += currentTodo
			consoleOutput += tabString + item + " " + str(currentNeed) + ' (' + str(currentTodo) + ')\n'
			consoleOutput += currentConsoleOutput
			consoleOutput += '\n' 

	# files itereren
	for item in fileList:

		f = open(join(dir,item))
		contents = f.read()
		f.close()

		currentNeed = contents.count('NE'+'ED')
		currentTodo = contents.count('TO'+'DO')

		totalNeed += currentNeed
		totalTodo += currentTodo

		if currentNeed>0 or currentTodo>0:
			consoleOutput += tabString + item + " " + str(currentNeed) + ' (' + str(currentTodo) + ')\n'
	

	return [totalNeed,totalTodo, consoleOutput]

[totalNeed,totalTodo, consoleOutput] = getOccurrences('.',1)
if totalNeed >0:
	print "Do not move to server, still NE"+"ED left!"
	
print "Total: " + str(totalNeed) + ' (' + str(totalTodo) + ')\n'
print "Breakdown:\n"
print consoleOutput




