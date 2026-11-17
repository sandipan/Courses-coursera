from sympy import *

x, y, z, r, s, t = symbols('x y z r s t')

f = lambda x: (2*x**2+3)*(4*x-6)
f = lambda t: (4-t**3)/(t**2+t+1)
f = lambda x: (1-exp(z))*(z+exp(z))
#print(diff(f(z), z).simplify())

#res = together(diff(f(t), t))
#num, den = fraction(res)
#res = simplify(num) / factor(den)
#print(res)

A, B, C = symbols('A B C')
f = lambda t: A*t / (B*t**2 + C*t**3)
#print(diff(f(t), t).simplify())
f = lambda r: A*exp(r) / (B + exp(r))
#print(diff(f(r), r).simplify())

f = lambda t: t*cos(t)*csc(t)
#print(diff(f(t), t).simplify())

f = lambda x: cos(x)/(1-sin(x))
#print(diff(f(x), x).simplify())

f = lambda x, y: 2*x*y / (x**2+y**2)
#print(f(x,y).subs(x, 1).subs(y, 2))
#print(diff(f(x,y), x).simplify(), diff(f(x,y), x).subs(x, 1).subs(y, 2))
#print(diff(f(x,y), y).simplify(), diff(f(x,y), y).subs(x, 1).subs(y, 2))

f = lambda s, t: sqrt(s**2 + t**2)
#print(diff(diff(f(s,t),s),t), diff(f(s,t), s, t))

f = lambda x, y: exp(x)*cos(y)
#print(diff(f(x,y),x,x)+diff(f(x,y),y,y))

f = lambda x, y, z: x*y**5*z**3 + atan(y*x**(3/2))
#print(diff(f(x,y,z),x,y,z))

f = lambda x, y: x**2/y
#print(Matrix([diff(f(x,y),x), diff(f(x,y),y)]).subs(x,3).subs(y,1))

def compute_dir_derivative(f, P, u):
	if u.norm() != 1:
		u = u / u.norm()
	Px, Py = P
	gradf = Matrix([diff(f(x,y),x), diff(f(x,y),y)]).subs(x, Px).subs(y, Py)
	return gradf.dot(u)

g= lambda x,y: exp(x)*sin(y)
P = (0,0)
u = Matrix([sqrt(3)/2, 1/2])
#print(compute_dir_derivative(g, P, u))

f= lambda x,y: x**2*y**3 + x**3*y**2
P = (-1,2)
u = Matrix([cos(pi/4), sin(pi/4)])
#print(compute_dir_derivative(f, P, u))

f= lambda x,y,z: z*exp(x*y)
#print(Matrix([diff(f(x,y,z),x), diff(f(x,y,z),y), diff(f(x,y,z),z)]).subs(x,-1).subs(y,0).subs(z,2))

f= lambda x,y: 400-x**2/100-y**2/1000
P = (100,300)
u = Matrix([-1/sqrt(2),1/sqrt(2)])
#print(compute_dir_derivative(f, P, u))
print(Matrix([diff(f(x,y),x), diff(f(x,y),y)]).subs(x, 100).subs(y, 300))

u = Matrix([-3/sqrt(109),10/sqrt(109)])
u = Matrix([3/sqrt(109),-10/sqrt(109)])
#u = Matrix([-10/sqrt(109),3/sqrt(109)])
print(compute_dir_derivative(f, P, u))
