import numpy as np

#print(np.linalg.inv([[3,-7,-2],[-3,5,1],[6,-4,0]]))

from scipy.linalg import lu

#A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
#p, l, u = lu(A)
#np.allclose(A - p @ l @ u, np.zeros((4, 4)))

#A = np.array([[3, -7, -2], [-3, 5, 1], [6, -4, 0]])
#_, l, u = lu(A)
#print(A)
#print(l)
#print(u)

from scipy.linalg import lu_factor, lu_solve
A = np.array([[3, -7, -2], [-3, 5, 1], [6, -4, 0]])
b = np.array([-3, 3, 2])
lu, piv = lu_factor(A)
x = lu_solve((lu, piv), b)
#print(A)
#print(lu)
#print(piv)
#print(x)

#I = np.eye(3)
#M1_1 = I.copy(); M1_1[1,0] = -1
#M2_1 = I.copy(); M2_1[2,0] = 2
#M3_1 = I.copy(); M3_1[2,1] = -5
#L = M1_1 @ M2_1 @ M3_1 # LU
#print(L)

#print(np.linalg.inv([[1,0,1],[0,1,1],[1,1,1]]))

def Gram_schmidt(basis):
	orth_basis = [basis[0]]
	for v in basis[1:]:
		u1 = v.copy()
		for u in orth_basis:
			u1 = u1 - (u1@u)*u / (u@u)
		orth_basis.append(u1)
	for i in range(len(orth_basis)):
		orth_basis[i] = orth_basis[i] / np.sqrt(orth_basis[i]@orth_basis[i])
	return orth_basis
	
#print(Gram_schmidt(np.array([[1,1,1], [0,1,1]])))
#print(Gram_schmidt(np.array([[1,1], [1,-1]])))
#print(Gram_schmidt(np.array([[1,1,-1], [0,1,-1]])))
#print(Gram_schmidt(np.array([[1,1], [1,0]])))

#A = np.hstack((np.ones(3).reshape(-1,1), np.arange(1,4).reshape(-1,1)))
#print(A)
#b = [1,1,3]
#print(np.linalg.inv(A.T@A)@(A.T@b))

#A = np.hstack((np.ones(3).reshape(-1,1), np.arange(3).reshape(-1,1)))
#print(A)
#b = [0,2,1]
#print(np.linalg.inv(A.T@A)@(A.T@b))

#print(np.linalg.eig([[1,-1],[-1,2]]))
#print(np.linalg.eig([[2,1,0],[1,2,1],[0,1,2]]))

A = [[0,1],[1,0]]
L, V = np.linalg.eig(A) 
print(L, V, A, V@np.diag(L)@V.T)
print(V@np.diag(L)**100@V.T)
s = 1/np.sqrt(2)
print(np.round(np.array([[s, -s], [s, s]])@np.array([[1, 0],[0, -1]])@np.array([[s, s], [-s, s]])))

print(np.linalg.eig(np.eye(2)))