import matplotlib.pyplot as plt

name = 'sim64'
lol = []
f = open('../data/simLog/' + name + 'transactions.txt','r')
for line in f:
    lol.append(line)
f.close()

transactions = []
for i in lol[1:]:
    transactions.append(eval(i.replace("\n", "")))

gainList = []
scoreList = []
for i in range(len(transactions)):
    gain = (transactions[i][5] - transactions[i][1])/transactions[i][1]
    score = transactions[i][4]

    gainList.append(gain)
    scoreList.append(score)

plt.scatter(scoreList,gainList)
plt.show()
