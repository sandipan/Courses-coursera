import numpy as np

A = np.array([[2,1,5],[1,2,1],[2,1,3]])
print(np.linalg.det(A))
b = np.array([20,10,15])
print(np.linalg.solve(A, b))


A = np.array([[7,5,3],[3,2,5],[1,2,1]])
print(np.linalg.det(A))
b = np.array([120,70,20])
print(np.linalg.solve(A, b))


A = np.array([[1,2,-1],[1,0,1],[0,1,0]])
print(np.linalg.inv(A))


A = np.array([[5,2,3],[-1,-3,2],[0,1,-1]])
B = np.array([[1,0,-4],[2,1,0],[8,-1,0]])
print(np.linalg.det(A)*np.linalg.det(B))

A = np.array([[2,0,0],[1,2,1],[-1,0,1]])
print(np.linalg.eig(A))

