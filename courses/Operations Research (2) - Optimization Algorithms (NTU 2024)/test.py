from pulp import *

def solve_and_extract_solution(problem, list_of_vars):
    ## Solve and check status again
    problem.solve() # solve the problem
    print('Status is :', LpStatus[problem.status])
    if problem.status == constants.LpStatusOptimal:
        print('Optimal Solution Found!!')
        sols = [x.varValue for x in list_of_vars]
        ## Alternatively you could write a for loop 
        ## sols = []
        ## for x in list_of_vars:
        ##    sols.append(x.varValue)
        print('Solution:',sols)
        print('Objective Value:', problem.objective.value())
        return sols
    elif problem.status == constants.LpStatusUnbounded:
        print('Unbounded solution -- need more constraints')
        return None
    elif problem.status == constants.LpStatusInfeasible:
        print('Problem has no feasible solution')
        return None
    else: 
        print('Problem has an undefined status -- something went wrong.')
        return None

'''
problem = LpProblem('max', LpMaximize) # Use LpMaximize if you are maximizing an objective function
x_1 = LpVariable('x_1', 0)
x_2 = LpVariable('x_2', 0)
problem += (x_1 + 2*x_2)
problem += (x_1 + x_2  <= 16)
problem += (x_1 + 4*x_2 >= 20)
problem += (x_2 <= 8)
print(solve_and_extract_solution(problem, [x_1, x_2]))
'''

'''
problem = LpProblem('max', LpMaximize) # Use LpMaximize if you are maximizing an objective function
#x_1 = LpVariable('x_1', 0, cat='Integer')
#x_2 = LpVariable('x_2', 0, cat='Integer')
x_1 = LpVariable('x_1', 0)
x_2 = LpVariable('x_2', 0)
problem += (3*x_1 + 5*x_2)
problem += (x_1 + x_2  <= 16)
problem += (x_2 <= 7.5)
#problem += (x_1 <= 8)
problem += (x_1 >= 9)
#problem += (x_2 <= 7)
print(solve_and_extract_solution(problem, [x_1, x_2]))
'''
'''
problem = LpProblem('min', LpMinimize) # Use LpMaximize if you are maximizing an objective function
n, m = 15, 3
x = [[LpVariable(f'x{i}[j]',lowBound=0, upBound=1) for j in range(m)] for i in range(n)]
#x = [[LpVariable(f'x{i}[j]',lowBound=0, cat='Binary') for j in range(m)] for i in range(n)]
c = [7,4,6,9,12,6,10,11,8,7,6,8,15,14,3]
problem += sum([c[i]*x[i][j] for j in range(m) for i in range(n)])
for i in range(n):
	problem += sum([x[i][j] for j in range(m)]) == 1
problem.solve() # solve the problem
print('Status is :', LpStatus[problem.status])
if problem.status == constants.LpStatusOptimal:
	print('Optimal Solution Found!!')
	print('Objective Value:', problem.objective.value())
'''