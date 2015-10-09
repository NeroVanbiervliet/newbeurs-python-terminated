import time

tStart = time.time()
n = 100000000

lol = 0
for i in range(n):
    lol += i

print 'Time:',time.time() - tStart
print 'And Now His Watch is Ended'
