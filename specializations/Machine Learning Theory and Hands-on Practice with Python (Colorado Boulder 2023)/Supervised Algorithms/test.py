import numpy as np

def log(x):
	return 0 if x <= 0 else np.log(x)

def entropy(X, y):
	p = sum(y>0) / len(y)
	return -p*log(p) -(1-p)*log(1-p)

def compute_info_gain(X, sp, y):
	H = entropy(X, y)
	n1, n2 = sum(X <= sp), sum(X > sp)
	H1 = entropy(X[X <= sp], y[X <= sp])
	H2 = entropy(X[X > sp], y[X > sp])
	return H - (n1 / (n1+n2) * H1 + n2 / (n1+n2) * H2)

def gini(X, y):
	p = sum(y>0) / len(y)
	return 2*p*(1-p) #1-p**2 -(1-p)**2
	
def compute_gini(X, sp, y):
	n1, n2 = sum(X <= sp), sum(X > sp)
	G1 = gini(X[X <= sp], y[X <= sp])
	print('G1', G1)
	G2 = gini(X[X > sp], y[X > sp])
	return (n1 / (n1+n2) * G1 + n2 / (n1+n2) * G2)
	
X = np.array([1]*3+[2]*4+[3]*2+[4]*5+[5]*2)
y = np.array([+1]*3+[+1]*2+[-1]*2+[+1]*2+[+1]+[-1]*4+[-1]*2)

for sp in np.linspace(1.5,4.5,4):
	print(sp) 
	print(compute_info_gain(X, sp, y))

print()

for sp in np.linspace(1.5,4.5,4):
	print(sp) 
	print(compute_gini(X, sp, y))