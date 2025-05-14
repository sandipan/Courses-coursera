from PA4 import read_file
from PA8 import dist1
import numpy as np
from math import exp
	
def ProbabilityHiddenPath(path, transition, initial):

	prob = initial
	for i in range(len(path) - 1):
		prob *= transition[path[i], path[i + 1]]
	return prob

'''	
lines = read_file("inp24.txt")
lines = read_file("ProbabilityOfHiddenPath.txt")
lines = read_file("dataset_11594_2.txt")
path = lines[0]
symbols = str.split(lines[2])
transition = {}
i = 0
for line in lines[5:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		transition[symbols[i], symbols[j]] = probs[j]
	i += 1
initial = 0.5
print path
print transition
print initial
print ProbabilityHiddenPath(path, transition, initial)
'''

def ProbabilityOutcomeHiddenPath(path, hiddenpath, emission):
	
	prob = 1
	for i in range(len(path)):
		prob *= emission[hiddenpath[i], path[i]]
	return prob

'''	
lines = read_file("inp25.txt")
lines = read_file("ProbabilityOfOutcomeGivenHiddenPath.txt")
lines = read_file("dataset_11594_4.txt")
path = lines[0]
symbols = str.split(lines[2])
hiddenpath = lines[4]
states = str.split(lines[6])
emission = {}
i = 0
for line in lines[9:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
	
print path
print hiddenpath
print emission
print ProbabilityOutcomeHiddenPath(path, hiddenpath, emission)
'''


def OutcomeLikelihood(x, states, transition, emission, initial):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * initial[state] * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = sum([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	ssink = sum([s[statel, n - 1] for statel in states])
	print ssink

'''	
lines = read_file("inp27.txt")
lines = read_file("OutcomeLikelihood.txt")
lines = read_file("dataset_11594_8.txt")
x = lines[0]
symbols = str.split(lines[2])
states = str.split(lines[4])
transition, emission = {}, {}
i = 0
for line in lines[7:7+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[7+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
initial = {state: 1.0 / len(states) for state in states}	
print x
print transition
print emission
print initial
OutcomeLikelihood(x, states, transition, emission, initial)
'''

def ViterbiDecoding(x, states, transition, emission, initial):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * initial[state] * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = max([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	ssink, state = max([(s[statel, n - 1], statel) for statel in states])
	path = state
	i = n - 2
	while i >= 0:
		smax, state = max([(s[statel, i] * transition[statel, state], statel) for statel in states])
		path = state + path
		i -= 1
	print path

'''	
lines = read_file("inp26.txt")
lines = read_file("ViterbiAlgorithm.txt")
lines = read_file("dataset_11594_6.txt")
x = lines[0]
symbols = str.split(lines[2])
states = str.split(lines[4])
transition, emission = {}, {}
i = 0
for line in lines[7:7+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[7+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
initial = {state: 1.0 / len(states) for state in states}	
print x
print transition
print emission
print initial
ViterbiDecoding(x, states, transition, emission, initial)
'''
