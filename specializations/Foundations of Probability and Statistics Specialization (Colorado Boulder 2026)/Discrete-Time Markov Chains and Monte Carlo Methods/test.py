import numpy as np

P = np.array([[0.5,0.2,0.3],[0.1,0.5,0.4],[0.2,0.2,0.6]])
P3 = P@P@P
#print(P3)

P = np.array([[0.5,0.2,0.3],[0,1,0],[0.2,0.2,0.6]])
P3 = P@P@P
#print(P3)
#print(P3[2,1], 1 - P3[2,1])

P2 = P@P
#print(P3[2,2] / (1 - P2[2,1])) # P(X4=N, X3!=S, X2!=S | X1=N) / P(X3!=S, X2!=S | X1=N)
                               # P(Y4=N | Y1=N) / (1 - P(Y3=S | Y1=N))

P = np.array([[0.1,0.4,0.5],[0.3,0.2,0.5],[0.6,0,0.4]])
Ps = P.copy()
for _ in range(100):
	Ps = Ps@P

#print(Ps)
#print(np.linalg.eig(P))

#print(16/21)


P = np.array([[0.8,0.2,0,0,0],[0,0.7,0.3,0,0],[0.4,0,0.2,0,0.4],[0,0,0.1,0,0.9],[0,0,0,0.5,0.5]])
Ps = P.copy()
for _ in range(1000):
	Ps = Ps@P
#print(Ps)


P = np.array([[2/3,1/3,0,0],[2/9,5/9,2/9,0],[0,4/9,4/9,1/9],[0,0,2/3,1/3]])
Ps = P.copy()
for _ in range(100):
	Ps = Ps@P
#print(Ps)


P = np.array([[0.1,0.4,0.5],[0.3,0.2,0.5],[0.6,0,0.4]])
Ps = P.copy()
for _ in range(100):
	Ps = Ps@P
#print(Ps)

eigvals, eigvecs = np.linalg.eig(P.T) # P^T pi = 1.pi <=> pi P = pi.1^T
#print(eigvals)
# Eigenvectors corresponding to eigenvalue 1
v = eigvecs[:, np.isclose(eigvals, 1)]
# Normalize each eigenvector
pi = v / v.sum(axis=0)
#print(np.real_if_close(pi))

import sympy as sp
#P = sp.Matrix([[0.9,-0.4,-0.5],[-0.3,0.8,-0.5],[0.6,0,-0.6],[1,1,1]]).T 
P = sp.Matrix([[0.1,0.4,0.5],[0.3,0.2,0.5],[0.6,0,0.4]])  # transition matrix
P = P.applyfunc(lambda x: sp.Rational(str(x)))
P = (P.T - sp.eye(3))
P[2, :] = sp.ones(1, 3)
x = sp.Matrix([0,0,1]) # 0,
#print(P.LUsolve(x))

P = sp.Matrix([[0.1,0.4,0.5],[0.3,0.2,0.5],[0.6,0,0.4]])  # transition matrix
pi = sp.symbols('p1:4')
eqs = list(sp.Matrix(1, 3, pi)*P - sp.Matrix(1, 3, pi))
eqs.append(sum(pi) - 1)
#print(sp.solve(eqs, pi))

#P = sp.Matrix([[0,0.1,0.2],[0.1,0.3,0.4],[0.4,0.2,0.3]])  # transition matrix: hit state 1 starting from X0=3, drop first row/col of P
#P = (sp.eye(3) - P)
#print(P.evalf(2))
#x = sp.Matrix([1,1,1])
#print(P.LUsolve(x))
P = sp.Matrix([[0.1,0.4],[0.3,0.2]])  # transition matrix: hit state 2 starting from X0=0, drop row/col 2 of P
#P = P.applyfunc(lambda x: sp.Rational(str(x)))
P = (sp.eye(2) - P)
x = sp.Matrix([1,1])
#print(P.LUsolve(x))


#P = sp.Matrix([[0.5,0,0.5,0],[0.7,0,0.1,0.2],[0.2,0.1,0.3,0.4],[0.1,0.4,0.2,0.3]])  # transition matrix: return to state 1 starting from X0=1
#P[:,0] = np.zeros(4)
#P = (sp.eye(4) - P)
#print(P.evalf(1))
#x = sp.Matrix([1,1,1,1])
#print(P.LUsolve(x))
P = sp.Matrix([[0.1,0.4,0.5],[0.3,0.2,0.5],[0.6,0,0.4]])  # transition matrix: hit state 0 starting from X0=0
P[:,0] = np.zeros(3)
#P = P.applyfunc(lambda x: sp.Rational(str(x)))
P = (sp.eye(3) - P)
x = sp.Matrix([1,1,1])
#print(P.LUsolve(x))

#print(1 / (4/(9*3)))


#---

'''
# w021
# P
# 0.1 0.4 0.5
# 0.3 0.2 0.5
# 0.6  0  0.4
#w021 = 0.1*w021 + 0.4*0 + 0.5*w221
#w221 = 1 + 0.6*w021 + 0*0 + 0.4*w221
A = np.array([[0.9, -0.5],[-0.6, 0.6]])
b = [0,1]
print(np.linalg.solve(A, b))

P = np.array([[0.1, 0.4, 0.5],
              [0.3, 0.2, 0.5],
              [0.6, 0.0, 0.4]])
N = 100000
total = 0
for _ in range(N):
    s = 0
    count = 0
    while s != 1:
        s = np.random.choice(3, p=P[s])
        if s == 2:
            count += 1
    total += count
print(total / N)
'''

# p2 # starts at 2 and visits 0
# P
# 0.1 0.3 0.4 0.2
# 0.3 0.2 0.4 0.1
# 0.4 0.1 0.3 0.2
#  0  0.7 0.2 0.1
#p1 = 0.3*1 + 0.2*p1 + 0.4*p2 + 0.2*0
#p2 = 0.4*1 + 0.1*p1 + 0.3*p2 + 0.2*0 # p3 = 0
A = np.array([[0.8, -0.4],[-0.1, 0.7]])
b = [0.3, 0.4]
#print(np.linalg.solve(A, b))

P = np.array([[0.1, 0.3, 0.4, 0.2],
              [0.3, 0.2, 0.4, 0.1],
              [0.4, 0.1, 0.3, 0.2],
              [0, 0.7, 0.2, 0.1]])
N = 100000
count = 0
for _ in range(N):
	s = 2
	while True:
		s = np.random.choice(4, p=P[s])
		if s == 0 or s == 3:
			if s == 0:
				count += 1
			break
#print(count / N)


#eigvals, eigvecs = np.linalg.eig(P.T) # P^T pi = 1.pi <=> pi P = pi.1^T
#v = eigvecs[:, np.isclose(eigvals, 1)]
#pi = v / v.sum(axis=0)
#print(pi)

'''
x = sp.symbols('x')
P = sp.Matrix([[1/2,1/2],[x,1-x]])
# Eigenvalues and eigenvectors of P.T
eigs = P.T.eigenvects()
# Extract eigenvector corresponding to eigenvalue 1
v = next(e[2][0] for e in eigs if sp.simplify(e[0] - 1) == 0)
# Normalize eigenvector
pi = v / sum(v)
#print("Eigenvalues:", P.T.eigenvals())
#print("Stationary distribution:", pi.applyfunc(sp.simplify))

xval = (sp.solve(2*x/(2*x+1) - 1/3, x))[0]
#print(xval)

P = sp.Matrix([[sp.Rational(1,2), sp.Rational(1,2)],
               [x, 1-x]]).subs(x, xval)
#print(P.applyfunc(lambda x: sp.Rational(str(x))))
Ps = P.copy()
for _ in range(100):
    Ps = (Ps @ P).applyfunc(sp.simplify)
#print(Ps)




# P(T=n+3) = (1/6)**3 P(T>n) # E[T] = 216
T = []
for i in range(1000):
	t = 0
	while True:
		s = np.random.choice(list(range(1,7)), 3)   
		#print(s)
		s = ''.join(map(str, s))
		t += 1
		if s == '123':
			T.append(t)
			break
#print(np.mean(T))

#import matplotlib.pylab as plt
#plt.hist(T)
#plt.show()


P = sp.Matrix([[0,1/2,1/2,0],[1/2,0,0,1/2],[1,0,0,0],[0,1,0,0]])
P = P.applyfunc(lambda x: sp.Rational(str(x)))
eigs = P.T.eigenvects()
v = next(e[2][0] for e in eigs if sp.simplify(e[0] - 1) == 0)
pi = v / sum(v)
#print(list(pi))
#print(list(pi.applyfunc(lambda x: 1/x)))

P = np.array([[0,1/2,1/2,0],[1/2,0,0,1/2],[1,0,0,0],[0,1,0,0]])
T = []
for i in range(10000):
	s = 0
	t = 0
	while True:
		s = np.random.choice(list(range(4)), p=P[s,:])   
		t += 1
		if s == 0:
			T.append(t)
			break
#print(np.mean(T))
#plt.hist(T)
#plt.show()
'''

# f(x) = 5/32 x^4
# F(x) = 1/32 x^5
# Finv(x) = 2 x^(1/5)

# f_U(u) = 1
# x = 2 u^(1/5)
# f_x(x) = f_U(u) |du / dx| = f_U(u) (5 u^(4/5) / 2)  = f_U(u) (5 (x/2)^4) / 2) = 1. (5 / 32 x^4)

# 6x(1-x) / 1 <= c 
# 6 - 12x = 0 = > x = 1/2
# -12. max
# 6x(1-x) / 1 <= 3/2

from sympy import symbols, S, exp, Interval
from sympy.calculus.util import maximum
x = symbols('x')
# Define a quadratic function: f(x) = -x^2 + 4x + 5
f = 6*x*(1-x) / 1
#f = 60*(x**2)*(1-x)**3  
# Find the maximum value over all Real numbers
max_val = maximum(f, x, domain=Interval(0, 1))
#print(f"Maximum value: {max_val}")


import sympy as sp

x, r = sp.symbols('x r')

f = 625/6*x**3*exp(-3*x) / (r*exp(-r*x))

'''
# First-order partial derivatives
fx = sp.diff(f, x)
fr = sp.diff(f, r)

# Solve for critical points
critical_points = sp.solve([fx, fr], [x, r])

print(critical_points)

# Evaluate function at critical points
for point in critical_points:
    print(f.subs({x: point[0], r: point[1]}))
'''

r = 1
f = 625/6*x**3*exp(-3*x) / (r*exp(-r*x))
#max_val = maximum(f, x, S.Reals)
#print(f"Maximum value: {max_val}")


import numpy as np

states = [1, 2]
actions = ['L', 'R', 'U', 'D']

V = {s: 0.0 for s in states}
gamma = 0.9

# Random walk policy
pi = {(s, a): 1/4 for s in states for a in actions}

# Rewards
r = {
    (1, 'L'): -1, (1, 'R'): 5,
    (2, 'L'): 0,  (2, 'R'): -1
}

for s in states:
    r[s, 'U'] = r[s, 'D'] = -1

# Transition probabilities
p = {(s, a, s1): 0 for s in states
     for a in actions for s1 in states}

p[1, 'R', 2] = p[2, 'L', 1] = 1
p[1, 'L', 1] = p[2, 'R', 2] = 1

for s in states:
    p[s, 'U', s] = p[s, 'D', s] = 1

# Iterative policy evaluation
for _ in range(1000):
    V_new = {}

    for s in states:
        V_new[s] = sum(
            pi[s, a] * (
                r[s, a] +
                gamma * sum(p[s, a, s1] * V[s1]
                            for s1 in states)
            )
            for a in actions
        )

    V = V_new
    #print(V)

print(V)
print("Value at state 2:", round(V[2], 1))
