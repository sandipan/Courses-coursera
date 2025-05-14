import numpy as np

def grad(x):
	x1, y1 = x
	return np.array([2*x1-6,2*y1])

def gradient_descent(x0, grad, alpha):
	x = x0
	for i in range(10):
		x -= alpha*grad(x)
		print(i, x)

#gradient_descent(np.array([0.,1.]), grad, alpha=0.1)

def f(x):
	return x**2 - 2

def df(x):
	return 2*x

def newtons_method(x0):
	x = x0
	for i in range(5):
		x = x - f(x) / df(x)
		print(i, x)
		
#newtons_method(2)
#newtons_method(3)
#newtons_method(4)
newtons_method(-0.1)
