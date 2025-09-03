from gurobipy import *

def solve_MIP():

	# Create a new model
	m = gp.Model()

	# Create variables
	x = m.addVar(vtype=GRB.CONTINUOUS, name="x")
	y = m.addVar(vtype=GRB.CONTINUOUS, name="y")

	# Set objective function
	#m.setObjective(2*x + 5*y, gp.GRB.MAXIMIZE)
	m.setObjective(9*x + 18*y, gp.GRB.MAXIMIZE)

	# Add constraints
	m.addConstr(7*x + 4*y <= 50)
	m.addConstr((1/1.1)*x + (1/0.7)*y <= 10)

	# Solve it!
	m.optimize()

	print(f"Optimal objective value: {m.objVal}")
	print(f"Solution values: x={x.X}, y={y.X}")

#solve_MIP()

def solve_MIP():

	"""Data"""
	products = range(7)
	resources = range(3)

	prices = [100, 120, 135, 90, 125, 110, 105]
	resource_consumptions = [[0, 3, 10],
							 [5, 10, 10],
							 [5, 3, 9],
							 [4, 6, 3],
							 [8, 2, 8],
							 [5, 2, 10],
							 [3, 2, 7]]
	resource_limitations = [100, 150, 200]

	"""Model"""
	eg1 = Model()
	x = []
	for i in products:
		x.append(eg1.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x'+str(i)))

	eg1.setObjective(quicksum(prices[i]*x[i] for i in products), GRB.MAXIMIZE)

	# add constraints and name them
	eg1.addConstrs((quicksum(resource_consumptions[i][j]*x[i] for i in products) <= resource_limitations[j] for j in resources), "resource_limitation")

	eg1.optimize()

	for var in eg1.getVars():
		print(var.varName, "=", round(var.x, 2))
	print("objective value =", round(eg1.objVal, 2))

	return eg1

solve_MIP()

import numpy as np

def solve_LR():

	# data
	d = np.array([[38, 137], [56, 201], [50, 152], [52, 107], [37, 150], [60, 173], [67, 194], [54, 166], [59, 154], [43, 137], [30, 38], [53, 193], [59, 154], [40, 175], [65, 247]])
	x, y = d[:,0].tolist(), d[:,1].tolist()
	n = len(d)

	m = Model()

	# Create variables
	alpha = m.addVar(vtype=GRB.CONTINUOUS, name="alpha")
	beta = m.addVar(vtype=GRB.CONTINUOUS, name="beta")
	
	# Set objective function
	m.setObjective(quicksum((y[i]-alpha-beta*x[i])**2 for i in range(n)), GRB.MINIMIZE)

	# Add constraints
	
	# Solve it!
	m.optimize()

	print(f"Optimal objective value: {m.objVal}")
	print(f"Solution values: alpha={alpha.X}, beta={beta.X}")

	X = np.hstack((np.ones((n,1)), np.array(x).reshape(-1,1)))
	y = np.array(y).reshape(-1,1)
	print(X.shape, y.shape, n)
	print(np.linalg.solve(X.T@X, X.T@y))

solve_LR()