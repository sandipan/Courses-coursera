import gurobipy as gp

def solve_MIP():

	# Solve the following MIP:
	#  maximize
	#        x +   y + 2 z
	#  subject to
	#        x + 2 y + 3 z <= 4
	#        x +   y       >= 1
	#        x, y, z binary

	# Create a new model
	m = gp.Model()

	# Create variables
	x = m.addVar(vtype='B', name="x")
	y = m.addVar(vtype='B', name="y")
	z = m.addVar(vtype='B', name="z")

	# Set objective function
	m.setObjective(x + y + 2 * z, gp.GRB.MAXIMIZE)

	# Add constraints
	m.addConstr(x + 2 * y + 3 * z <= 4)
	m.addConstr(x + y >= 1)

	# Solve it!
	m.optimize()

	print(f"Optimal objective value: {m.objVal}")
	print(f"Solution values: x={x.X}, y={y.X}, z={z.X}")

#solve_MIP()

from gurobipy import *

def linear_example(limitations_list):

	"""Data"""
	products = range(2)
	resources = range(3)

	prices = [700, 900]
	resource_consumptions = [[3, 5],
							  [1, 2],
							  [50, 20]]
	resource_limitations = limitations_list

	"""Model"""
	eg1 = Model()
	x = []
	for i in products:
		x.append(eg1.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x'+str(i)))

	eg1.setObjective(quicksum(prices[i]*x[i] for i in products), GRB.MAXIMIZE)

	# add constraints and name them
	eg1.addConstrs((quicksum(resource_consumptions[j][i]*x[i] for i in products) <= resource_limitations[j] for j in resources), "resource_limitation")

	eg1.optimize()

	for var in eg1.getVars():
		print(var.varName, "=", round(var.x, 2))
	print("objective value =", round(eg1.objVal, 2))

	return eg1

limitations_list = [3600, 1600, 48000]
origin_model1 = linear_example(limitations_list)

# use Pi to get the shadow price of each constraint
print(f"shadow price of the wood constraint is {origin_model1.Pi[0]}")
print(f"shadow price of the labor constraint is {origin_model1.Pi[1]}")
print(f"shadow price of the machine constraint is {origin_model1.Pi[2]}")


def solve_MIP():

	m = gp.Model()

	# Create variables
	x1 = m.addVar(vtype=GRB.CONTINUOUS, name="x1")
	x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2")
	x3 = m.addVar(vtype=GRB.CONTINUOUS, name="x3")

	# Set objective function
	m.setObjective(4*x1 - 2*x2 +  x3, gp.GRB.MAXIMIZE)

	# Add constraints
	m.addConstr(2*x1 + x2 <= 10)
	m.addConstr(x2 + x3 >= -3)
	m.addConstr(x1 + 3*x2 - 3*x3 == 14)

	# Solve it!
	m.optimize()

	print(f"Optimal objective value: {m.objVal}")
	print(f"Solution values: x1={x1.X}, x2={x2.X}, x3={x3.X}")
	print(f"schadow price: {m.Pi[0]}, {m.Pi[1]}, {m.Pi[2]}")
	print(f"constraints: {10-2*x1.X-x2.X}, {-3-x2.X-x3.X}, {14-x1.X-3*x2.X+3*x3.X}")

#solve_MIP()

def network_flow():
	m = gp.Model()

	# Create variables
	xOA = m.addVar(vtype=GRB.CONTINUOUS, name="xOA")
	xOB = m.addVar(vtype=GRB.CONTINUOUS, name="xOB")
	xOC = m.addVar(vtype=GRB.CONTINUOUS, name="xOC")
	xAB = m.addVar(vtype=GRB.CONTINUOUS, name="xAB")
	xBC = m.addVar(vtype=GRB.CONTINUOUS, name="xBC")
	xAD = m.addVar(vtype=GRB.CONTINUOUS, name="xAD")
	xBD = m.addVar(vtype=GRB.CONTINUOUS, name="xBD")
	xBE = m.addVar(vtype=GRB.CONTINUOUS, name="xBE")
	xCE = m.addVar(vtype=GRB.CONTINUOUS, name="xCE")
	xDE = m.addVar(vtype=GRB.CONTINUOUS, name="xDE")
	xDT = m.addVar(vtype=GRB.CONTINUOUS, name="xDT")
	xET = m.addVar(vtype=GRB.CONTINUOUS, name="xET")
	xTO = m.addVar(vtype=GRB.CONTINUOUS, name="xTO")

	# Set objective function
	#m.setObjective(-xTO, gp.GRB.MINIMIZE)
	m.setObjective(xTO, gp.GRB.MAXIMIZE)

	# Add constraints
	m.addConstr(xOA - xAB - xAD == 0)
	m.addConstr(xOB + xAB - xBC - xBD - xBE == 0)
	m.addConstr(xOC + xBC - xCE == 0)
	m.addConstr(xAD + xBD - xDE - xDT == 0)
	m.addConstr(xBE + xCE + xDE - xET == 0)
	m.addConstr(xTO - xOA - xOB - xOC == 0)
	m.addConstr(xDT + xET - xTO == 0)
	m.addConstr(xOA <= 2)
	m.addConstr(xOB <= 5)
	m.addConstr(xOC <= 4)
	m.addConstr(xAD <= 7)
	m.addConstr(xAB <= 2)
	m.addConstr(xBC <= 1)
	m.addConstr(xBD <= 4)
	m.addConstr(xBE <= 3)
	m.addConstr(xCE <= 4)
	m.addConstr(xDE <= 1)
	m.addConstr(xDT <= 5)
	m.addConstr(xET <= 7)

	# Solve it!
	m.optimize()

	print(f"Optimal objective value: {m.objVal}")
	print(f"Solution values: xOA={xOA.X}, xOB={xOB.X}, xOC={xOC.X}, xAB={xAB.X}, xBC={xBC.X}, xAD={xAD.X}, xBD={xBD.X}, xBE={xBE.X}, xCE={xCE.X}, xDE={xDE.X}, xDT={xDT.X}, xET={xET.X}")

#network_flow()




