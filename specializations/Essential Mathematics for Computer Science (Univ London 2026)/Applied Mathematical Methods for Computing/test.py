import numpy as np

print(np.sqrt(2**2+3**2+6**2))
print(180*np.acos(1/np.sqrt(17)/np.sqrt(10))/np.pi)

A, B = [[1,2,3],[4,5,6]], [[7,8],[9,10],[11,12]]
print(np.array(A)@np.array(B))

A, B = [[2,4],[6,8]], [[1,3],[5,7]]
print(np.array(A)@np.array(B))

A, B = [[2,0,1],[3,1,0]], [[1,4],[2,5],[3,6]]
print(np.array(A)@np.array(B))

Tg, Tn = [[0,1,0],[0,0,1]], [[2,0],[0,3]]
print(np.array(Tn)@np.array(Tg))


Tg, Tn = [[0,1,0],[0,0,1]], [[2,0],[0,3]]
print(np.array(Tn)@np.array(Tg))


a = np.pi/4
R = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
F = [[1,0],[0,-1]]
print(np.array(R).T@F@np.array(R))

a = np.pi/2
R = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
print(np.array(R)@np.array([[1],[0]]))

T = [[1,0,4],[0,1,-2],[0,0,1]]
print(np.array(T)@np.array([[2],[3],[1]]))


A = [[1,-3,5],[2,-1,-3],[3,0,4]]
b = [-9,19,-13]
print(np.linalg.solve(A, b))

T = [[1,0,3],[0,1,4],[0,0,1]]
print(np.array(T)@np.array([[0,2,2],[0,0,1],[1,1,1]]))


print(np.array([[3,0,0],[0,2,0],[0,0,1]])@np.array([[1,0,5],[0,1,4],[0,0,1]]))

from scipy.special import perm, comb, factorial

print(comb(11,5))
print(comb(6,3))
print((2**6)-comb(6,5)-comb(6,6), comb(6,0)+comb(6,1)+comb(6,2)+comb(6,3)+comb(6,4))
print((2**6)-comb(6,0)-comb(6,1)-comb(6,2), comb(6,3)+comb(6,4)+comb(6,5)+comb(6,6))
print(comb(15,3))

print('----')
print(comb(7,4)+comb(7,5)+comb(7,6)+comb(7,7))
print(2**7-comb(7,0)-comb(7,1)-comb(7,2), comb(7,3)+comb(7,4)+comb(7,5)+comb(7,6)+comb(7,7))
print(comb(10,4))
print(perm(10,3), comb(10,3)*factorial(3))
print(perm(8,4)*5)
print(1+perm(8,1)*2+perm(8,2)*3+perm(8,3)*4)
print(np.floor(149/2)+np.floor(149/3)-np.floor(149/6))

print(perm(4,2), comb(4,2)*factorial(2))

print('----')
print(np.mean([3,3,3,7,10,5]))
print(np.mean([4, 8, 6, 5, 3, 7, 2, 9]))
print(np.var([2, 4, 6, 8, 10], ddof=1), np.std([2, 4, 6, 8, 10], ddof=1))
n = 30
print(1-perm(365, n) / 365**n)
print(np.median([7, 3, 5, 9, 2, 8, 4]))
print(np.mean([45, 56, 78, 90, 65, 88, 70, 50, 92, 84, 72, 68, 81, 60, 75, 85, 87, 93, 77, 55]))
a = [15, 22, 27, 10, 19, 24, 18, 16, 12, 20]
print(np.max(a)-np.min(a), np.mean(a), np.median(a))
print(np.std([50, 60, 70, 80, 90]))
print(np.median([2, 3, 5, 2, 4, 3, 5]))

a = [10, 12, 11, 10, 17]
print(np.mean(a), np.median(a), np.var(a, ddof=0))

a = list(range(1,7))
print(np.var(a, ddof=0), np.std(a, ddof=0))


