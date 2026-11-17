def newton_raphson(f, df, x0, tol=1e-8, max_iter=100):
    x = x0
    for _ in range(max_iter):
        if abs(df(x)) < 1e-12:
            raise ZeroDivisionError("Derivative is zero.")
        x_new = x - f(x)/df(x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise RuntimeError("Newton-Raphson did not converge.")

import numpy as np

# Example: f(x) = x² - 2
f = lambda x: x**2 - (2+2/np.exp(1)**2)*x + 1
df = lambda x: 2*x - (2+2/np.exp(1)**2)

#root = newton_raphson(f, df, x0=1)
#print("Root:", root)

#from sympy import *
#x = symbols('x')
#print(nsolve(ln(2*x)-ln((x-1)**2)-2, x, 0.5))

#print(np.array([9,5,4])-np.array([6,9,3]))
#print(np.array([2,5,0])-3*np.array([3,2,3]))
#print(np.linalg.norm([-5*np.sqrt(5),4,-2*np.sqrt(7)]))
#print(np.dot(np.array([4,4,3]), np.array([6,7,8])-np.array([5,5,1])))

from sympy import *
k = symbols('k')
v = Matrix([3,k,7])
u = Matrix([1,4,3])
#print(u.dot(v))
#print(solve(u.dot(v)-0, k))
#print(np.dot([3,-6,7], [1,4,3]))

#print(0.5*np.linalg.norm(np.cross(np.array([0,1,7])-np.array([1,1,3]), np.array([1,2,5])-np.array([1,1,3]))))
A = ((Matrix([0,1,7])-Matrix([1,1,3])).cross(Matrix([1,2,5])-Matrix([1,1,3]))).norm()/2
#print(A, A.evalf())


v = np.cross(np.array([1,3,-2]), np.array([2,1,-3]))
#print(v / np.linalg.norm(v))
u, v, w = symbols('u v w')
u = Matrix([1,3,-2])
v = Matrix([2,1,-3])
w = u.cross(v)
#print(w / w.norm())

u = Matrix([1,0,4])
v = Matrix([0,1,2])
v_unit = v / v.norm()
#print((u.dot(v_unit))*v_unit)

#print(np.abs(np.dot(np.array([3,0,-1]), np.cross(np.array([0,2,4]), np.array([-2,3,0])))))

#print(cos(105*pi/180))

x = symbols('x')
x = pi/3
#print((2*cos(pi/2*x)).evalf(), (2*cos(pi/2*(x+4))).evalf(), \
#    (2*cos(pi/2*(x-4))).evalf(), (2*cos(pi/2*(x+2*4))).evalf(), (2*cos(pi/2*(x-2*4))).evalf())


t = symbols('t')
P = Matrix([3,6,0])
Q = Matrix([-2,3,1])
v = P - Q
#print(Q + t*v)

B = Matrix([8,8,1])
C = Matrix([-8,8,14])
#print((1-t)*B + t*C)

P = Matrix([3,-1,2])
n = Matrix([6,-2,4])
#print(P + t*n)

P = Matrix([-7,12,4])
v = Matrix([3,-2,-4])
#print(P + t*v)

A, B, C = [0,-2,10], [8,8,1], [-8,8,14]
AB = Matrix(B) - Matrix(A)
AC = Matrix(C) - Matrix(A)
n = AB.cross(AC)
D = -n.dot(A)
#print(n, D)

L1 = Matrix([2*t, 1-3*t, 2*t-3])
L2 = Matrix([4*t, 2*t+1, -3*t-3]) # intersects at [0,0,0]
#n = (L1.subs(t, 1)).cross(L2.subs(t, 1)).evalf()
#n = Matrix([2,-2,-1]).cross(Matrix([4,3,-6])).evalf()
P = Matrix([0,1,-3])
n = Matrix([2,-3,2]).cross(Matrix([4,2,-3]))
D = -P.dot(n)
#print(n, D)

n1, n2 = Matrix([5, -2*sqrt(11), 10]), Matrix([2*sqrt(11), 6, -8])
#print((n1.dot(n2)) / (n1.norm()*n2.norm()))

Q = Matrix([1,0,2])
n = Matrix([-4, 8, 9])
D = -n.dot(Q)
P = Matrix([3,-2,5])
#print((P.dot(n)+D)/n.norm())

import matplotlib.pylab as plt
x = np.array(np.linspace(-1,np.exp(1)-1,200).tolist() + np.linspace(np.exp(1)-1,4,200).tolist())
#plt.plot(x, 1/(1-np.log(x+1)), 'r.-')
#plt.axvline(x=np.exp(1)-1, color='b')
#plt.grid()
#plt.show()

x = symbols('x')
#print(solve(x*x+4*x-21, x))

#print(tan(-75*pi/180))
#print(solve((sec(x)+csc(x))*(sin(x)+cos(x))-cot(x)-1, x))

A, B, C = Matrix([4+sqrt(5),3*sqrt(5),4]), Matrix([2*sqrt(5),2*sqrt(5),2-2*sqrt(5)]), Matrix([sqrt(5),2*sqrt(5),2])
#print((A-B).norm().evalf(), (B-C).norm(), (C-A).norm())

t = symbols('t')
AB = B-A
#print(A + t*AB)
#print(B + t*AB)
AC, BC = C - A, C - B
#print(AC.dot(BC) / (AC.norm()*BC.norm()))

n = AC.cross(BC)
D = -n.dot(A)
#print(n, D)




