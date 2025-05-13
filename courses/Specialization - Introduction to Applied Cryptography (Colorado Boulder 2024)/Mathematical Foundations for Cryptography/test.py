def gcd_ext(a, b):
	b0 = b
	x0, y0 = 1, 0
	x1, y1 = 0, 1
	while b:
		q = a // b
		x0, x1 = x1, x0 - q * x1
		y0, y1 = y1, y0 - q * y1
		a, b = b, a % b
	#if x0 < 0:
	#	x0 += b0
	return a, x0, y0

def compute_exp_mod(x, n, m):
	pmod, p = {}, 1
	y = x
	while p < n:
		pmod[p] = y
		p *= 2
		y = (y * y) % m
	print(pmod)
	r = 1
	for p in sorted(pmod.keys())[::-1]:
		if n >= p:
			n -= p
			r = (r * pmod[p]) % m
	return r
	
def primes(n):
	S = list(range(2,n+1))
	for e in sorted(S):
		me = 2*e
		while me <= n:
			if me in S:
				S.remove(me)
			me += e
	return S
		
def Euler_totient(n):
	P = factorize(n)
	print(P)
	e = 1
	for p in P:
		e *= p**P[p]*(1-1/p)
	return int(e)

import numpy as np

def sieve_Eratosthenes(n):
	P = np.ones(n+1, dtype=int)
	P[0:2] = 0
	for e in range(2, n+1):
		P[range(2*e, n+1, e)] = 0
	return [i for i in range(n+1) if P[i]]	
	
def factorize(n, P=None):
	#P = primes(n // 2) #int(np.sqrt(n)) #
	if P is None:
		P = sieve_Eratosthenes(n) #int(np.sqrt(n)) #
	#print(n, P)
	i = 0
	#f = {}
	f = set([])
	while n > 1:
		#print(n, i, P[i])
		if n % P[i] == 0:
			n //= P[i]
			#f[P[i]] = f.get(P[i], 0) + 1
			f.add(P[i])
		else:
			i += 1
	return f

def Euler_totient_prime_factors(n, P):
	f = factorize(n, P)
	print(n, f)
	#e = n #1
	#for p in f:
	#	e *= (1-1/p) #p**f[p]*(1-1/p)
	return int(n*np.prod([(1-1/p) for p in f])) #int(e)

def Euler_totients_prime_factors(a, N):
	P = sieve_Eratosthenes(N)
	return [Euler_totient_prime_factors(n, P) for n in a]
	
def Euler_totient_def(n):
	#phi = 0
	#for i in range(1, n):
	#	if gcd(i, n) == 1:
	#		phi += 1
	return sum([gcd(i, n) == 1 for i in range(1, n)]) #phi

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a
		
def Euler_totients_def(a):
	return [Euler_totient_def(n) for n in a]

import math

def bin_rev(d):
	b = []
	while d:
		b.append(d % 2)
		d //= 2
	return b

def mult_exp_mod(a, d, m):
	k = int(math.log2(d))
	r = a % m
	a_pow = [r]
	for i in range(k):
		a_pow.append(a_pow[-1]**2 % m)
	print(a_pow)
	b = bin_rev(d)
	res = 1
	for i in range(len(b)):
		if b[i]:
			res = (res * a_pow[i]) % m
	return res
	
print(mult_exp_mod(47, 69, 143))
print(mult_exp_mod(4, 13, 497))

#print(bin(69))



'''
from time import time	
n = 1234571
start = time()
print(Euler_totient_prime_factors(n, sieve_Eratosthenes(n)))
print(time() - start)
start = time()
print(Euler_totient_def(n))
print(time() - start)


a = [12345, 123456, 1234561, 1234563, 1234567, 1234569, 1234571]
start = time()
print(Euler_totients_prime_factors(a, max(a)))
print(time() - start)
start = time()
print(Euler_totients_def(a))
print(time() - start)
'''

def mult_inverse(a, b):
    """
    Modular multiplicative inverse.
    """
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1    

#from functools import reduce
#from operator import mul    
from math import prod
	
def CRT_residue(a, m):
	# assert len(a) == len(m)
	n = len(a)
	P = prod(m) #reduce(mul, m)
	M = [P // m[i] for i in range(n)]
	N = [gcd_ext(M[i], m[i])[1] for i in range(n)]
	return sum([a[i]*M[i]*N[i] for i in range(n)]) % P
	
def Garner(a, m):
	M, s = 1, 0
	for i in range(len(m)):
		s += a[i] * M
		M *= m[i]
		#print(s, M)
	return s
	
def RSA_encrypt(m, e, n):
	return (m**e) % n
	
def RSA_decrypt(c, d, n):
	return (c**d) % n
	

'''	
print(gcd_ext(819, 990))
print(gcd_ext(527, 612))
print(gcd_ext(91, 343))
print(gcd_ext(930, 992))
print(gcd_ext(16, 47))
print(gcd_ext(219, 220))
print(compute_exp_mod(47, 69, 143))
print(compute_exp_mod(15, 15, 14))
print(factorize(4*27*7*11))
print(Euler_totient(3**4))
print(Euler_totient(2717))
for a in [93, 16, 5, 174]:
	print((a**2)%221)
print(1/(300*np.log(10)), 1/700)
m, e, d, n = 15, 7, 103, 143
c = RSA_encrypt(m, e, n)
print(c, RSA_decrypt(c, d, n))
'''
#print(sieve_Eratosthenes(100))
#m = [2147483743, 2147483713, 2147483693, 2147483659, 2147483647, 2147483629]
#a = [1246736738, 748761, 1829651881, 2008266397, 748030137, 1460049539]
#print(CRT_residue(a, m))
#print(Garner(a, m))
#print(np.sqrt(99115))
#print(factorize(112), factorize(922))
#print(factorize(99115), factorize(13115))
#print(primes(99115//5+1))
#n1, n2 = 12345, 82734
#print(n1 % 7, n1 % 8, n1 % 9)
#print(n2 % 7, n2 % 8, n2 % 9)
#print((n1 + n2) % 7, (n1 + n2) % 8, (n1 + n2) % 9)
#print((n1 * n2) % 7, (n1 * n2) % 8, (n1 * n2) % 9)
#print((16*72 + 28*63 + 20*56) % 504)
#print(primes(462))
#print((16**4) % 143)
#print((42**4) % 143)
#print((113**2) % 143)
#print((42**2) % 143)
#print((46**2) % 143)
#print((114 * 16 * 2) % 143)