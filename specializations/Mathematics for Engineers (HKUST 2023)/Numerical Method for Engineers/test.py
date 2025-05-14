import numpy as np

def f(x):
	return x**2 - 5

def df(x):
	return 2*x

def bisection_method(x0, x1):
	for i in range(10):
		x2 = (x0 + x1) / 2
		if f(x0) * f(x2) < 0:
			x1 = x2
		elif f(x2) * f(x1) < 0:
			x0 = x2
		print(i, x2, x1 - x0)
	
def newtons_method(x0):
	x = x0
	for i in range(5):
		x = x - f(x) / df(x)
		print(i, x)
		
def secant_method(x0, x1):
	for i in range(5):
		x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
		x1, x0 = x2, x1
		print(i, x1)
		
#bisection_method(2, 3)
#newtons_method(2)
#secant_method(3, 2)

def power_method(A, x0):
	print(A, x0)
	x1 = x0
	for i in range(2):
		x0 = x1
		x1 = A @ x0 
	return x1.T@x0 / (x0.T@x0)
	
#print(power_method(np.array([[6,5],[4,5]]), np.array([[1], [1]])))

A = np.array([[3,5,2],[2,3,4],[6,6,6]])
P13 = np.array([[0,0,1],[0,1,0],[1,0,0]])
M1 = np.array([[1,0,0],[0,1,0],[-1/2,0,1]])
M2 = np.array([[1,0,0],[-1/3,1,0],[0,0,1]])
P23 = np.array([[1,0,0],[0,0,1],[0,1,0]])
M3 = np.array([[1,0,0],[0,1,0],[0,-1/2,1]])
U = np.array([[6,6,6],[0,2,-1],[0,0,5/2]])
PL = np.linalg.inv(M3@P23@M2@M1@P13)
print(np.linalg.inv(M1))
print(PL)
print(PL@U)

print(8 / (1- np.log10(9)))  # (0.9/1)^p <= 10^(-8)

print(0.9*0.01*(10/9)**0.2)
