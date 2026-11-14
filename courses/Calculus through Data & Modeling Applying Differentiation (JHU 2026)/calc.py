from sympy import *

def L(x, a):
	return expand(f(a) + (x-a)*diff(f(x), x).subs(x, a))

def f(x):
	#return sin(x)
	#return sqrt(x+8)
	#return 2**x
	#return sqrt(x+1/2)
	return x**2 + 3*x - 1

def L(x, y, a, b):
	return expand(f(a, b) + (x-a)*diff(f(x,y), x).subs(x, a).subs(y, b)  + (y-b)*diff(f(x,y), y).subs(x, a).subs(y, b))

def f(x, y):
	#return x / (x+y)
	#return exp(x*y)*sin(y)
	return y*exp(x+y**2)

def L(x, y, z, a, b, c):
	return expand(f(a, b, c) + (x-a)*diff(f(x,y,z), x).subs(x, a).subs(y, b).subs(z, c)  + \
		                       (y-b)*diff(f(x,y,z), y).subs(x, a).subs(y, b).subs(z, c)) + \
	                           (z-c)*diff(f(x,y,z), z).subs(x, a).subs(y, b).subs(z, c)

def f(x, y, z):
	return sqrt(x**2 + y**2 + z**2)

#x = symbols('x')
#print(L(x, pi/6))
#print(L(x, 1))
#print(L(x, 0))
#print(L(x, 100))
#print(L(x, 100).subs(x, 100))
#print(10.0249**2)
#print(L(x, 2))
#print(L(x, 2).subs(x, 2.01))
#x, y = symbols('x y')
#print(L(x, y, 3, 2))
#print(L(x, y, 0, pi))
#print(4*6.02-2.99-14)
#print(L(x, y, -9, 3))
#print(L(x, y, -9, 3).subs(x, -8.98).subs(y, 2.97), f(-8.98, 2.97))
#x, y, z = symbols('x y z')
#print(L(x,y,z,2,1,2))

def critical_points(f, x):
	#print(diff(f(x), x))
	#return roots(diff(f(x), x), x)
	return solve(diff(f(x), x), x, dict=False)

def find_critical_points(f, x):
	points = critical_points(f, x)
	d2f = diff(f(x), x, x)
	#print(d2f)	
	for p in points:
		#p = float(p)
		sign = d2f.subs(x, p)
		#print(p, sign)
		if sign < 0:
			print(f'{p}:{f(p).evalf()}: max (concave)')
		elif sign > 0:
			print(f'{p}:{f(p).evalf()}: min (convex)')
		else:
			print(f'{p}:{f(p).evalf()}: not max/min, inflection point')

def inflection_points(f, x):
	return solve(diff(f(x), x, x), x, dict=False)
	
def plot(f, x):
	import numpy as np
	import matplotlib.pylab as plt
	f_n = lambdify(x, f, modules='numpy')
	x_val = np.linspace(-25,25,1000)
	y_val = f_n(x_val)
	#print(x)
	#print(y)
	plt.plot(x_val, y_val, 'r.-')
	plt.grid()
	plt.show()

#x = symbols('x')
#find_critical_points(lambda x: x**4-6*x**2+8*x, x)
#find_critical_points(lambda x: x**3-6*x**2+12*x+10, x)
#f = exp(x)/(x**2+1) 
#f = (x**2-4)/(x**2+4) 
#plot(f, x)
#f = lambda x: exp(x)/(x**2+1) 
#f = lambda x: exp(-x*x)
#f = lambda x: (x**2-4)/(x**2+4) 
#find_critical_points(f, x)
#print(inflection_points(f, x))

def partials(f, x, y):
	return diff(f(x,y), x), diff(f(x,y), y)

def DHessian(f, x, y):
	return diff(f(x,y), x, x)*diff(f(x,y), y, y) - (diff(f(x,y), x, y))**2

def critical_points(f, x, y):
	fx, fy = partials(f, x, y)
	return solve([fx, fy], [x,y], dict=True)

def find_critical_points(f, x, y):
	points = critical_points(f, x, y)
	print(points)
	D = DHessian(f, x, y)
	#print(D)	
	for p in points:
		#print(p)
		if not p[x].is_real or not p[y].is_real: continue
		sign = D.subs(x, p[x]).subs(y, p[y])
		#print(p, sign)
		if sign < 0:
			print(f'{p}:{f(p[x], p[y]).evalf()}: saddle point')
		elif sign > 0:
			if diff(f(x,y), x, x).subs(x, p[x]).subs(y, p[y]) > 0:
				print(f'{p}:{f(p[x], p[y]).evalf()}: min (convex)')
			else:
				print(f'{p}:{f(p[x], p[y]).evalf()}: max (concave)')
		else:
			print(f'{p}:{f(p[x], p[y]).evalf()}: not max/min/saddle point')

def f(x, y):
	#return y + x*sin(y)
	#return x*y + 1/x + 1/y
	return ln(2 + sin(x*y))
	#return x**3 - 12*x*y + 8*y**3
	#return x*y
	#return sin(x**2 + y**2)

#x, y = symbols('x y')
#fx, fy = partials(f, x, y)
#print(fx.subs(x,0).subs(y,0), fy.subs(x,0).subs(y,0))
#print(DHessian(f, x, y).subs(x,0).subs(y,0))
#find_critical_points(f, x, y)

def partials(f, x, y):
	return diff(f(x,y), x), diff(f(x,y), y)

def solve_lagrange_multipliers(f, g, x, y, lambda_):
	fx, fy = partials(f, x, y)
	gx, gy = partials(g, x, y)
	return solve([fx - lambda_*gx, fy - lambda_*gy, g(x,y)], [x,y,lambda_], dict=True)

def f(x,y):
	return x**2 + y**2
	#return x**2 + x*y + y**2 
	#return 2*x + 3*y
	#return x*y

P = 1
#print(P**2/16)

def g(x,y):
	return x*y-1
	#return x**2 + y**2 - 1
	#return x**2 + 4*y**2 - 1 #x**2 + 4*y**2 - 0.81
	#return 2*(x + y) - P
	
def find_constrained_solutions(f, g, x, y, lambda_):
	sol = solve_lagrange_multipliers(f, g, x, y, lambda_)
	for p in sol:
		if not p[x].is_real or not p[y].is_real: continue
		print(f'{p}:{f(p[x], p[y]).evalf()}')

x, y, lambda_ = symbols('x y lambda_')
#print(solve_lagrange_multipliers(f, g, x, y, lambda_))
find_constrained_solutions(f, g, x, y, lambda_)


def partials(f, x, y, z):
	return diff(f(x,y,z), x), diff(f(x,y,z), y), diff(f(x,y,z), z)

def solve_lagrange_multipliers(f, g, x, y, z, lambda_):
	fx, fy, fz = partials(f, x, y, z)
	gx, gy, gz = partials(g, x, y, z)
	return solve([fx - lambda_*gx, fy - lambda_*gy, fz - lambda_*gz, g(x,y,z)], [x,y,z,lambda_], dict=True)

def f(x,y,z):
	#return x-y+z
	#return x+y+z
	#return x*y*z
	return sqrt(x**2+y**2+z**2)

#print(2/sqrt(5**2+2**2+1**2), (2/sqrt(5**2+2**2+1**2)).evalf())

def g(x,y,z):
	#return x**2+y**2+z**2-3
	#return x*y*z-64
	#return x+y+z-30
	return 5*x+2*y-z+2
	
def find_constrained_solutions(f, g, x, y, z, lambda_):
	sol = solve_lagrange_multipliers(f, g, x, y, z, lambda_)
	for p in sol:
		if not p[x].is_real or not p[y].is_real or not p[z].is_real: continue
		print(f'{p}:{f(p[x], p[y], p[z]).evalf()}')

#x, y, z, lambda_ = symbols('x y z lambda_')
#print(solve_lagrange_multipliers(f, g, x, y, lambda_))
#find_constrained_solutions(f, g, x, y, z, lambda_)

def partials(f, x, y, z):
	return diff(f(x,y,z), x), diff(f(x,y,z), y), diff(f(x,y,z), z)

def solve_lagrange_multipliers(f, g1, g2, x, y, z, lambda1, lambda2):
	fx, fy, fz = partials(f, x, y, z)
	g1x, g1y, g1z = partials(g1, x, y, z)
	g2x, g2y, g2z = partials(g2, x, y, z)
	return solve([fx - lambda1*g1x - lambda2*g2x, fy - lambda1*g1y - lambda2*g2y, fz - lambda1*g1z- lambda2*g2z, g1(x,y,z), g2(x,y,z)], [x,y,z,lambda1, lambda2], dict=True)

def f(x,y,z):
	return x*y+y*z

def g1(x,y,z):
	return x*y-1
	
def g2(x,y,z):
	return y**2+z**2-1

def find_constrained_solutions(f, g1, g2, x, y, z, lambda1, lambda2):
	sol = solve_lagrange_multipliers(f, g1, g2, x, y, z, lambda1, lambda2)
	for p in sol:
		if not p[x].is_real or not p[y].is_real or not p[z].is_real: continue
		print(f'{p}:{f(p[x], p[y], p[z]).evalf()}')

#x, y, z, lambda1, lambda2 = symbols('x y z lambda1 lambda2')
#find_constrained_solutions(f, g1, g2, x, y, z, lambda1, lambda2)