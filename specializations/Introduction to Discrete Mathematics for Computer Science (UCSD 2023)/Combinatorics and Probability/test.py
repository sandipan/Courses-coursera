for letter in {'e', 'u'}:
    for digit in {8, 2, 5}:
        print(letter, digit)
		
from itertools import product

for t in product({'e', 'u'}, {8, 2, 5}):
    print(*t, sep='')
	
print(26**5)

from itertools import product

#for number, password in enumerate(product('abcdefghijklmnopqrstuvwxyz', repeat=5)):
#	print(number, ''.join(password))

print(25**3, 25*24*23/6)
print(10**4*26**2)

from itertools import product

print(len([n for n in range(10000)
           if str(n).count('7') == 1]))
print(len([t for t in product(range(10), repeat=4)
           if t.count(7) == 1]))
		   
from itertools import permutations

for p in permutations('abc', 2):
    print(p)
	
from itertools import permutations

for p in permutations('abcde', 3):
    print(*p, sep='')
	
from itertools import permutations

for p in permutations('abc', 3):
    print(*p, sep='')
	
print(15*14*13)

from itertools import combinations
print(len(list(combinations(range(10),5))), 10*9*8*7*6/120)

n = 10 
count = 0

for i in range(n):
    for j in range(n):
        for k in range(n):
            if i < j and j < k:
                count += 1

print(count, n*(n-1)*(n-2)/6)

for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
                count += 1

print(count, n*(n-1)*(n-2)/6)#(16*n**3-18*n**2+20*n)/12)
n = 1000 
print(n*(n-1)*(n-2)/6)

#from math import comb
from scipy.special import comb
n = 7 #3
a, b = 3, -2
print([int(comb(n, k)*a**(n-k)*b**k) for k in range(n+1)])

print(comb(13,3)*comb(13,3))

print(comb(6,3)*5**6)
print(comb(10,4))

print(comb(24,4))

print(9*8*7*6)
import numpy as np
print(np.prod(range(4,4+9-1+1))/np.prod(range(1,9+1)))
print(comb(9+4-1, 9))

print(4**9)

print(comb(15+7-1, 7-1))

print(comb(15-7+7-1, 7-1))

s = [n*(n+1)/2 for n in range(1,11)]
print(sum(np.cumsum(s)))

print(sum([comb(12, k) for k in range(1, 7)]))

g = [comb(k, 2) for k in 2*np.arange(1,7)]
print(g, np.prod(g), np.prod(g) / np.prod(range(1,len(g)+1)))

print(comb(44,6))
print(comb(6,3)*comb(38,3))

for n in range(11):
	print([comb(n, k) / 2**n for k in range(n+1)])

n = 100
probs = [comb(n, k) / 2**n for k in range(n+1)]
print(sum(probs[40:60]))

n = 1000
probs = [comb(n, k) / 2**n for k in range(n+1)]
print(sum(probs[400:600]))

def prob_prob():
	import matplotlib.pylab as plt
	import seaborn as sns
	probs = np.zeros((16,16))
	for w in range(16):
		for b in range(16):
			if w+b and 30-w-b:
				probs[w,b] = 0.5*(w/(w+b)+(15-w)/(30-w-b))
			#plt.scatter(w, b, c=p)
	print(np.max(probs))
	ax = sns.heatmap(probs, annot=True, fmt=".3f")
	plt.show()
	
def monty_hall(strat='change', n=10000):
	count = 0
	all = set(range(3))
	for _ in range(n):
		car = np.random.choice(3, 1)[0]
		choice = np.random.choice(3, 1)[0]
		opened = list(all - set([car, choice]))[0]
		if strat == 'change':
			choice = list(all - set([choice, opened]))[0]
		count += (choice == car)
	return count / n
	
print(monty_hall('keep'))
print(monty_hall('change'))

def birthdays():
	n = 35
	#print(len(range(365-n+1, 365+1)))
	#print(1-np.prod(range(365-n+1, 365+1)) / 365**n)
	prob = 1
	for i in range(n):
		prob *= (365-i) / 365
		print(i, 1-prob)
	print(1-prob)

	N = 2000 #0
	counts = np.zeros(N)
	for k in range(N):
		bdays = np.random.choice(365, n)
		count = 0 # equal pairs	
		for i in range(n):
			for j in range(i+1, n):
				count += (bdays[i] == bdays[j])
		counts[k] = count
	print(np.mean(count))

	for k in range(n):
		print(k, comb(k, 2)/365) # exp # pairs
		

import re
N = 10000
n = 20
counts = np.zeros(N)
for i in range(N):
	out = ''.join(map(str, np.random.choice(2, n).tolist()))
	counts[i] = len(re.findall('10', out)) #HT
print(np.mean(counts))