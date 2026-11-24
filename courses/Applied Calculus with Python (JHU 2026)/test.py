import numpy as np

from sympy import *
from sympy.calculus.util import continuous_domain

x = symbols('x', real=True)

f = -4/5*x+ 7 #1 / (x**2 - 4)
domain = continuous_domain(f, x, S.Reals)
#print(domain)

A = np.array([[4, 1],[1.5, 1]])
b = np.array([9, 7])
#print(np.linalg.solve(A, b))

#A = np.array([[33, 1],[0, 1]])
#b = np.array([1350, 48])
#sol = np.linalg.solve(A, b)
#print(sol@[33,1], sol@[34,1])

k = symbols('k')
#print([s.evalf() for s in solve(2**(k*(-12))-8,k,domain=S.Reals)])

#print(Rational(2948 - 2530, 32-26))

t = symbols('t')
#print(diff(x**50, x))
#print(diff(1/(4*t)**3 + 16*t**2/(4*t)**3, t))
#print(diff(3*exp(x)+x, x).subs(x, 0))
# y - 3 = 4(x - 0)
r, a, b = symbols('r a b')
#print(diff(a*exp(r)/(b+exp(r)), r).simplify())


def Riemann_Sum(f, a = -1, b = 1, n = 4):
	x = symbols('x')
	dx = (b - a)/n 
	x_left = [a + i*dx for i in range (0, n)]
	x_right = [a + i*dx for i in range(1,n+1)]
	f_left = [f(x).subs(x,i) for i in x_left]
	f_right = [f(x).subs(x,i) for i in x_right]
	LHS = sum(f_left)*dx
	RHS = sum(f_right)*dx
	print(f'The left-hand sum is {LHS} and the right-hand sum is {RHS}')

f = lambda x: x**2  + 2*x + 1
#Riemann_Sum(f, n=1000)
#print(integrate(f(x), (x, -1, 1)))

f = lambda x: 4*x-3
Riemann_Sum(f, a=2,b=5,n=3)
print(integrate(f(x), (x, 2, 5)))

g = 9 - x**2
print(integrate(g, (x, 1, 4)), integrate(g, (x, 1, 3)), integrate(g, (x, 3, 4)))

def plot_g():
	import matplotlib.pylab as plt
	x = np.linspace(1,4,1000)
	g = 9 - x**2
	plt.plot(x, g, 'b.-')
	plt.fill_between(x, 0, g, where=(g >= 0), color='green', alpha=0.2)
	plt.fill_between(x, 0, g, where=(g < 0), color='red', alpha=0.2)
	plt.axhline(0, color='black', linewidth=0.8)
	plt.grid()
	plt.show()

#plot_g()

print(integrate(x**0.5+1/x, (x, 4, 9)))#.evalf())
