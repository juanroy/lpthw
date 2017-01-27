i = 0
numbers = []

while i < 6:
    print "At the top i is %d" % i
    numbers.append(i)

    i = i + 1
    print "Numbers now: ", numbers
    print "At the bottom i is %d" % i


print "The numbers: "

for num in numbers:
    print num


#---

numbers = []

def buclewhile(incr):
    print "At the top incr is %d" % incr
    numbers.append(incr)
    print "Numbers now: ", numbers

for i in range(0, 6):
    buclewhile(i)