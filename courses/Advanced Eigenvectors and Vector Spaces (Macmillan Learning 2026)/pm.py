
import numpy as np

def power_method(A, x=None, tol=1e-8, max_iter=1000):
    n = A.shape[0]
    if x is None:
        x = np.ones(n)
    x = x / np.linalg.norm(x)

    for _ in range(max_iter):
        y = A @ x
        x_new = y / np.linalg.norm(y)

        if np.linalg.norm(x_new - x) < tol or np.linalg.norm(x_new + x) < tol:
            break
        x = x_new

    #print('here', x_new)
    eigenvalue = x_new @ (A @ x_new)  # Rayleigh quotient
    return eigenvalue, x_new


def shifted_power_method(A, mu, tol=1e-8, max_iter=1000):
    n = A.shape[0]
    B = np.linalg.inv(A - mu * np.eye(n))
    eigenvalue_B, x = power_method(B, tol, max_iter)

    eigenvalue_A = mu + 1 / eigenvalue_B
    return eigenvalue_A, x
'''
A = np.array([[4., 1., 0.],
              [1., 3., 1.],
              [0., 1., 2.]])

# Power method: largest eigenvalue in magnitude
lam, v = power_method(A)
print("Power method:")
print("Eigenvalue:", lam)
print("Eigenvector:", v)

# Shifted power method: eigenvalue closest to mu
mu = 2.5
lam_s, v_s = shifted_power_method(A, mu)
print("\nShifted power method:")
print("Eigenvalue:", lam_s)
print("Eigenvector:", v_s)

# Verify using NumPy
print("\nNumPy eigenvalues:", np.linalg.eigvals(A))
'''

A = np.array([[1,3],[1,-1]])
#x0 =np.array([1,1])
#print(power_method(A))
print(np.linalg.eig(A))

#A = np.array([[1,3],[0,-1]])
#x0 =np.array([1,-1])
#print(power_method(A, x0, max_iter=102))
#print(np.linalg.eig(A))
#A = np.array([[1,1],[-2,-1]])
#print(np.linalg.eig(A))

#A = np.array([[1,2,1,-2],[1,-1,0,1],[1,0,1,-1],[0,-1,1,-1]])
#print(np.linalg.det(A))
'''
A = np.array([[3,-2,1],[0,3,0],[3,0,-1],[1,-2,2],[0,1,-2],[3,3,2]])
b = np.array([-2,-1,1,-1,-2,0])
print(np.linalg.matrix_rank(A))
#c = np.linalg.solve(A.T@A, A.T@b)
#print(c)
#print(A@c)

import sympy as sp

M = sp.Matrix([
    [3, -2, 1],
    [0, 3, 0],
    [3, 0, -1],
    [1, -2, 2],
    [0, 1, -2],
    [3, 3, 2]
])

v = sp.Matrix([-2, -1, 1, -1, -2, 0])

print("Rank of M:", M.rank())
print("Rank of augmented matrix:", M.row_join(v).rank())
print("Solution:", sp.linsolve((M, v)))
'''

A = np.array([[1,0,0,1],[1,1,0,0],[0,0,1,1],[0,1,1,0]])
print(np.linalg.matrix_rank(A))
