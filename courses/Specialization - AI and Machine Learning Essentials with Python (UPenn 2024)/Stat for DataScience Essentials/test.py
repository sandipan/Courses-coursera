import numpy as np

def simulate_sampling(n, N):
	times = 0
	for iter in range(10000):
		if n//2 in np.random.choice(N, n):
			times += 1
	print(times / 10000)		

def simulate_sampling2(N):
	times = 0
	for iter in range(10000):
		if not 1 in np.random.choice(N, 1):
			if 1 in np.random.choice(N-1, 1):
				times += 1
	print(times / 10000)		

#simulate_sampling(20, 100)
#simulate_sampling(2, 6)
#simulate_sampling(1, 6)
#simulate_sampling2(6)
#print(5/36, 1/6)
#X = np.arange(1,7)
#print(np.mean(X), np.var(X))

from sympy import symbols, integrate

#x = symbols('x')
#print(integrate(1/9*(4-x**2), x))
#print(integrate(1/9*(4-x**2), (x, -1, 2)))
#print(integrate(1/9*(4-x**2), (x, -1, x)))
#print(integrate(1/9*(4-x**2)*x, x))
#print(integrate(1/9*(4-x**2)*x, (x, -1, 2)))
#print(integrate(1/9*(4-x**2)*x**2, (x, -1, 2)))
#print(integrate(1/9*(4-x**2)*x**2, (x, -1, 2)) - (integrate(1/9*(4-x**2)*x, (x, -1, 2)))**2)
#print(integrate(1/9*(4-x**2)*(x-1/4)**2, (x, -1, 2)), 43/80)

from scipy.stats import norm
#print(norm.ppf(.95))
#print(norm.ppf(.95, loc=85, scale=5))
#print(85+5*norm.ppf(.95))
#print(norm.ppf(.95, loc=1, scale=1/(8*np.sqrt(2))))
#print(norm.ppf(.95, loc=64, scale=np.sqrt(32)))
#print(1 - norm.cdf(3500, loc=100*30, scale=10*15))

def compute_mean_var(x, p):
	m = sum(p*x)
	v = sum(p*x**2) - m**2
	return m, v

#x = np.arange(3)
#p = np.array([1/4,1/2,1/4])
#print(compute_mean_var(x, p))

def clt():
	n = 10**3
	x = np.arange(1,4)
	p = np.array([0.21, 0.54, 0.25])
	xbar, xvar = compute_mean_var(x, p)
	print(xbar, xvar)
	print(norm.ppf(.005, loc=xbar, scale=np.sqrt(xvar)/np.sqrt(n)), norm.ppf(.995, loc=xbar, scale=np.sqrt(xvar)/np.sqrt(n)))
	#, xbar - norm.ppf(.99, loc=xbar, scale=np.sqrt(xvar)/np.sqrt(n)), xbar + norm.ppf(.99, loc=xbar, scale=np.sqrt(xvar)/np.sqrt(n))

n = 100
phat = 0.12
print(phat - norm.ppf(.975)*np.sqrt(phat*(1-phat))/np.sqrt(n-1), phat + norm.ppf(.975)*np.sqrt(phat*(1-phat))/np.sqrt(n-1))

n = 200
phat = 0.18
print(np.sqrt(phat*(1-phat)/(n-1)))

n1, n2 = 100, 200
p1, p2 = 0.12, 0.18
v1, v2 = p1*(1-p1)/(n1-1), p2*(1-p2)/(n2-1) #p1*(1-p1), p2*(1-p2) 
#print(v1, v2, v1 + v2, np.sqrt(v1 + v2))
print(v1 + v2, np.sqrt(v1 + v2))

def plot_F():
	import matplotlib.pylab as plt
	x = np.linspace(-5, 5, 100)
	f = (4 - x**2) / 9
	f[x < -1] = 0
	f[x > 2] = 0
	F = -x**3 / 27 + 4*x/9 + 11/27
	F[x < -1] = 0
	F[x > 2] = 1
	plt.plot(x, f, label='f(x)')
	plt.plot(x, F, label='F(x)')
	plt.legend()
	plt.grid()
	plt.xlabel('x')
	plt.ylabel(r'pdf and cdf $(-\frac{x^3}{27} + \frac{4x}{9} + \frac{11}{27})$')
	plt.show()
