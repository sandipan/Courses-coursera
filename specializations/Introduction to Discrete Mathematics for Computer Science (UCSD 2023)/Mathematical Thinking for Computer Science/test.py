from itertools import permutations
import numpy as np
from time import time

def magic_square():
	for p in permutations(list(range(1,10))):
		p = np.reshape(p, (3,3))
		sums = np.sum(p, axis=0).tolist() + np.sum(p, axis=1).tolist() + [sum(p[i,i] for i in range(3)), sum(p[i,2-i] for i in range(3))] #sum(p[i,j] for i, j in zip([0,1,2], [2,1,0]))]
		if sums.count(sums[0]) == len(sums):
			print(p)
			break

def fast_magic_square():
	for p in permutations(list(range(1,10)), 4):
		p = np.reshape(p, (2,2))
		p1 = np.zeros((3,3), dtype=int)
		p1[:2,:2] = p
		p1[:2,2] = (15-np.sum(p, axis=1)).tolist()
		p1[2,:2] = (15-np.sum(p, axis=0)).tolist()
		p1[2,2] = 15-sum(p[i,i] for i in range(2))
		sums = np.sum(p1, axis=0).tolist() + np.sum(p1, axis=1).tolist() + [sum(p1[i,i] for i in range(3)), sum(p1[i,2-i] for i in range(3))]
		if len(np.unique(p1.ravel())) == len(p1.ravel()) and sums.count(sums[0]) == len(sums):
			print(p1)
			break
			
def faster_magic_square():
	for p in permutations(list(range(1,5))+list(range(6,10)), 3):
		p = np.reshape(list(p)+[5], (2,2))
		p1 = np.zeros((3,3), dtype=int)
		p1[:2,:2] = p
		p1[:2,2] = (15-np.sum(p, axis=1)).tolist()
		p1[2,:2] = (15-np.sum(p, axis=0)).tolist()
		p1[2,2] = 15-sum(p[i,i] for i in range(2))
		sums = np.sum(p1, axis=0).tolist() + np.sum(p1, axis=1).tolist() + [sum(p1[i,i] for i in range(3)), sum(p1[i,2-i] for i in range(3))]
		if len(np.unique(p1.ravel())) == len(p1.ravel()) and sums.count(sums[0]) == len(sums):
			print(p1)
			break

def faster2_magic_square():
	for p in permutations(list(range(1,5))+list(range(6,10)), 2):
		p = np.reshape(list(p)+[1,5], (2,2))
		p1 = np.zeros((3,3), dtype=int)
		p1[:2,:2] = p
		p1[:2,2] = (15-np.sum(p, axis=1)).tolist()
		p1[2,:2] = (15-np.sum(p, axis=0)).tolist()
		p1[2,2] = 15-sum(p[i,i] for i in range(2))
		sums = np.sum(p1, axis=0).tolist() + np.sum(p1, axis=1).tolist() + [sum(p1[i,i] for i in range(3)), sum(p1[i,2-i] for i in range(3))]
		if len(np.unique(p1.ravel())) == len(p1.ravel()) and sums.count(sums[0]) == len(sums):
			print(p1)
			break

'''
start = time()			
magic_square()
print('time: ', time() - start)
start = time()			
fast_magic_square()
print('time: ', time() - start)
start = time()			
faster_magic_square()
print('time: ', time() - start)
start = time()			
faster2_magic_square()
print('time: ', time() - start)
'''

#np.sqrt(27182)

import itertools as it

def is_solution(perm):
    for (i1, i2) in it.combinations(range(len(perm)), 2):
        if abs(i1 - i2) == abs(perm[i1] - perm[i2]):
            return False

    return True

'''
for perm in it.permutations(range(8)):
    if is_solution(perm):
        print(perm)
        exit()
'''
	
def can_be_extended_to_solution(perm):
    i = len(perm) - 1
    for j in range(i):
        if i - j == abs(perm[i] - perm[j]):
            return False
    return True

def extend(perm, n):
    if len(perm) == n:
        print(perm)
        exit()

    for k in range(n):
        if k not in perm:
            perm.append(k)

            if can_be_extended_to_solution(perm):
                extend(perm, n)

            perm.pop()

#extend(perm = [], n = 20)

import numpy as np

def print_grid(grid):
    i = 0
    while i < len(grid):
        print(grid[i:i+5])
        i += 5
    print('')

def num_diag(grid):
    return sum([1 for x in grid if x != 0])

def can_be_extended_to_solution_(grid_vec):
    m = len(grid_vec) - 1
    if m >= 25 or 25 - m < 16 - num_diag(grid_vec):
        return False
    i, j = m // 5, m % 5
    #print('here', (i,j))
    for u in range(i-1, i+2):
        for v in range(j-1, j+2):
            if not (u == i and v == j): 
                index = 5 * u + v
                if u >= 0 and u < 5 and v >= 0 and v < 5 and index >=0 and index < m:
                    prod = grid_vec[index]*grid_vec[m]
                    #print(u, v, i, j, grid_vec[m], prod)
                    if prod > 0:
                        #print('here1', u, v, index, prod)
                        if grid_vec[m] == 1 and ((u == i-1 and v == j+1) or (u == i+1 and v == j-1)):
                            return False
                        elif grid_vec[m] == -1 and ((u == i-1 and v == j-1) or (u == i+1 and v == j+1)):
                            return False
                    elif prod < 0:                        
                        if abs(u-i) + abs(v-j) <= 1: 
                            return False
    return True

import matplotlib.pylab as plt

def plot_sol(grid_vec):
	global id
	plt.figure(figsize=(10.35,10))
	plt.subplots_adjust(0,0,1,0.95,0,0)
	grid_vec_ = grid_vec.copy()
	if len(grid_vec_) < 25:
		grid_vec_ += [0]*(25-len(grid_vec_))
	for i in range(25):
		plt.subplot(5,5,i+1)
		plt.imshow(images[grid_vec_[i]])
		plt.xticks([]), plt.yticks([])
	plt.suptitle('Number of diagonals: {}'.format(num_diag(grid_vec_)), size=20)
	plt.savefig('out_{:05d}.png'.format(id))
	plt.close()
	id += 1
	
def extend_(grid_vec, n):
    global count
    if len(grid_vec) == 25:
        num_sol = num_diag(grid_vec)
        print(count)
        count += 1
        if num_sol == n:
            print_grid(grid_vec)
            plot_sol(grid_vec)
            exit()
        #elif num_sol >= 15:
        #    print(num_sol)
            #print_grid(grid_vec)
    for k in range(-1,2):
        grid_vec.append(k)
        #print('here', k, len(grid_vec))
        if can_be_extended_to_solution_(grid_vec):
            extend_(grid_vec, n)
            if count >= 700:
               plot_sol(grid_vec)
        grid_vec.pop()

count = 1
id = 1
images = {i:plt.imread(f'{i}.png') for i in range(-1,2)}
extend_(grid_vec = [], n = 16)
#extend_(grid_vec = [1,1,1,0,-1,\
#					0,0,1,0,-1,\
#					-1,-1,0,-1,-1,\
#					-1,0,1,0,0,\
#					-1], n = 16)
#print(can_be_extended_to_solution_([1,1,1,0,-1, 0,0,1,0,-1, -1,-1,0,-1,-1, -1,0,1,0,0, -1,0,1,1,1]))
#print(can_be_extended_to_solution_([1,1,1,0,-1, 0,0,1,0,-1, -1,-1,0,-1,-1, -1,0,1,0,0, -1]))

def change(amount):
  assert(amount >= 24)
  if amount == 24:
    return [5, 5, 7, 7]
  elif amount == 25:
    return [5, 5, 5, 5, 5]
  elif amount == 26:
    return [5, 7, 7, 7]
  elif amount == 27:
    return [5, 5, 5, 5, 7]
  elif amount == 28:
    return [7, 7, 7, 7]
  coins = change(amount - 5)
  coins.append(5)
  return coins  
  # complete this method
  
def find_x(l, u, count=1):
	m = (l + u) // 2
	a = input(f'Q{count}: x = {m}? ')
	if a == 'y':
		return m
	elif a == 'g':
		return find_x(m+1, u, count+1)
	elif a == 'l':
		return find_x(l, m-1, count+1)

#find_x(1, 2097151)

def left_digit():
	for n in range(1000, 10000):
		pow10 = int(np.log10(n))
		#print(n, pow10, 10**pow10*(n//10**pow10), n - 10**pow10*(n//10**pow10))
		if n == 57*(n - 10**pow10*(n//10**pow10)):
			print(n)
			break