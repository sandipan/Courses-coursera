from PA4 import read_file
from PA8 import dist1
import numpy as np
from math import exp
	
def ProfileHMM(threshold, alphabet, alignments):
	
	nrow, ncol = len(alignments), len(alignments[0])
	transition, emission = {}, {}
	
	inscols = []
	for i in range(ncol):
		count = {a:0 for a in alphabet + ['-']}
		for j in range(nrow):
			count[alignments[j][i]] += 1
		#fracins = sum([1.0 for j in range(nrow) if alignments[j][i] == '-']) / nrow
		fracins = count['-'] / (1.0 * nrow)
		#print i, count['-'], nrow, fracins
		if fracins >= threshold:
			inscols += [i]
	#print inscols
	
	transtrs = []
	for i in range(nrow):
		curstate, nextstate, transtr = 'S', None, 'S'
		ii, im, id = 0, 1, 1
		for j in range(ncol):
			if not j in inscols:
				nextstate = 'D' + str(id) if alignments[i][j] == '-' else 'M' + str(im)
				#im, id = im + 1, id + 1
				ii = im
				id = im = im + 1
			else:
				#ii = im
				if alignments[i][j] == '-':
					continue
				else:
					nextstate = curstate if curstate[0] == 'I' else 'I' + str(ii)
			#if curstate != nextstate:	ii += 1
			transition[curstate, nextstate] = transition.get((curstate, nextstate), 0) + 1
			if alignments[i][j] != '-':
				emission[nextstate, alignments[i][j]] = emission.get((nextstate, alignments[i][j]), 0) + 1
			transtr += '->' + nextstate
			curstate = nextstate
		transtr += '->E'
		#print 'here', curstate
		nextstate = 'E'
		transition[curstate, nextstate] = transition.get((curstate, nextstate), 0) + 1
				
		transtrs.append(transtr)	
		#print alignments[i]
		#print transtr
		
	states = ['S']
	i, j, k = 0, 1, 1
	while j < im:
		states += ['I' + str(i)]
		i += 1
		states += ['M' + str(j)]
		j += 1
		states += ['D' + str(k)]
		k += 1
	states += ['I' + str(i)]
	#if i < ii:
	#	states += ['I' + str(i+1)]
	states += ['E']
	#print states
	#print transition
	#print emission
	
	#print states
	for state in states:
		#print state, {nextstate: transition[curstate, nextstate] for (curstate, nextstate) in transition if curstate == state}
		transfromstate = {nextstate: transition[curstate, nextstate] for (curstate, nextstate) in transition if curstate == state}
		totaltransfromstate = 1.0 * sum([transfromstate[nextstate] for nextstate in transfromstate])
		transfromstate = {nextstate: round(transfromstate[nextstate] / totaltransfromstate, 3) for nextstate in transfromstate}
		for nextstate in transfromstate:
			transition[state, nextstate] = transfromstate[nextstate]
	#print transition
	
	for state in states:
		#print state, {symbol: emission[curstate, symbol] for (curstate, symbol) in emission if curstate == state}
		emitfromstate = {symbol: emission[curstate, symbol] for (curstate, symbol) in emission if curstate == state}
		totalemitfromstate = 1.0 * sum([emitfromstate[symbol] for symbol in emitfromstate])
		emitfromstate = {symbol: round(emitfromstate[symbol] / totalemitfromstate, 3) for symbol in emitfromstate}
		for symbol in emitfromstate:
			emission[state, symbol] = emitfromstate[symbol]
	#print emission
	
	print '  ' + ' '.join(states)
	for state in states:
		line = state
		for state1 in states:
			line += ' ' + str(transition.get((state, state1), 0))
		print line		
	print '--------'
	print '  ' + ' '.join(alphabet)
	for state in states:
		line = state
		for symbol in alphabet:
			line += ' ' + str(emission.get((state, symbol), 0))
		print line		
		
	return states, transition, emission
'''	
lines = read_file("inp28.txt")
#lines = read_file("ProfileHMM.txt")
#lines = read_file("dataset_11632_2.txt")
threshold = float(lines[0])
alphabet = str.split(lines[2])
alignments = lines[4:]
#print threshold
#print alphabet
#print alignments
ProfileHMM(threshold, alphabet, alignments)
'''

def NormalizeSmooth(vec, pseudocount):
	n, tot = len(vec), sum(vec)
	return [round((vec[i] + pseudocount) / (tot + n*pseudocount), 3) for i in range(n)]

def ProfileHMMWithPseudocounts(threshold, alphabet, alignment, pseudocount):
	states, transition, emission = ProfileHMM(threshold, alphabet, alignment)
	#ins = [state for state in states if state[0] == 'I']
	n = len(states)
	for i in range(n - 1):
		if states[i] == 'S':
			nextstates = ['I0', 'M1', 'D1']
		elif i >= n - 4 and i <= n - 2:
			num = int(states[i][1])
			nextstates = ['I' + str(num), 'E']
		else:
			num = int(states[i][1])
			nextstates = ['I' + str(num), 'M' + str(num + 1), 'D' + str(num + 1)]
		vec = []
		for nextstate in nextstates:
			vec.append(transition.get((states[i], nextstate), 0))
		vec = NormalizeSmooth(vec, pseudocount)
		for j in range(len(nextstates)):
			transition[(states[i], nextstates[j])] = vec[j]
		if states[i][0] == 'I' or states[i][0] == 'M':
			vec = []
			for symbol in alphabet:
				vec.append(emission.get((states[i], symbol), 0))
			vec = NormalizeSmooth(vec, pseudocount)
			j = 0
			for symbol in alphabet:
				emission[(states[i], symbol)] = vec[j]
				j += 1
		
	print '  ' + ' '.join(states)
	for state in states:
		line = state
		for state1 in states:
			line += ' ' + str(transition.get((state, state1), 0))
		print line		
	print '--------'
	print '  ' + ' '.join(alphabet)
	for state in states:
		line = state
		for symbol in alphabet:
			line += ' ' + str(emission.get((state, symbol), 0))
		print line		
	
	return states, transition, emission

'''	
lines = read_file("inp29.txt")
lines = read_file("ProfileHMMPseudocounts.txt")
lines = read_file("dataset_11632_4.txt")
threshold, pseudocount = map(float, str.split(lines[0]))
alphabet = str.split(lines[2])
alignments = lines[4:]
#print threshold
#print alphabet
#print alignments
ProfileHMMWithPseudocounts(threshold, alphabet, alignments, pseudocount)
'''

def getCurStates(i):
	return ['I' + str(i-1), 'M' + str(i), 'D' + str(i)]

def getPrevStates(state, i):
	return [('M' + str(i - 1), i - 1), ('I' + str(i - 1), i), ('D' + str(i - 1), i - 1)]

def SequenceAlignmentwithProfileHMM(x, threshold, alphabet, alignment, pseudocount):
	
	states, transition, emission = ProfileHMMWithPseudocounts(threshold, alphabet, alignment, pseudocount)
	m = max(map(int, [state[1:] for state in states if state[0] == 'M']))
	#startStates = ['M1', 'D1', 'I0']
	#initial = {state: 1.0 / len(states) for state in startStates}	
	s, n = {}, len(x)
	#for state in startStates:
	#	s[state, 0] = 1 * initial[state] * emission.get((state, x[0]), 0)
	s['I0', 1, 1] = max([transition.get(('S', 'I0'), 0) * emission.get(('I0', x[0]), 0), transition.get(('I0', 'I0'), 0) * emission.get(('I0', x[0]), 0)])
	s['M1', 1, 1] = max([transition.get(('S', 'M1'), 0) * emission.get(('M1', x[0]), 0), transition.get(('I0', 'M1'), 0) * emission.get(('M1', x[0]), 0)])
	s['D1', 1, 0] = max([transition.get(('S', 'D1'), 0), transition.get(('I0', 'D1'), 0)])
	#print s
	#print m, n
	for i in range(2, m + 1):
		for state in getCurStates(i):
			for j in range(n):
				if state[0] == 'D':
					s[state, i, j] = max([s[prevstate, index, j] * transition.get((prevstate, state), 0) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])
				else:
					if i == 6: print 'here', state, i, j, getPrevStates(state, i), max([(s[prevstate, index, j] * transition.get((prevstate, state), 0), prevstate) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])
					s[state, i, j + 1] = max([s[prevstate, index, j] * transition.get((prevstate, state), 0) * emission.get((state, x[j]), 0) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])			
	print s
	print 'here000', m, n
	
	i = m
	j = n
	
	print 'h', i, getCurStates(i)
	
	ssink, state = max([(s.get((state, i, j), 0), state) for state in getCurStates(i)])
	print ssink, state
	path = state
	print path
	
	i = m
	if state[0] != 'D':
		j -= 1
	while i > 0:
		#prevStates = getPrevStates(state, i)
		prevStates = [(p, index) if state[0] != 'I' else (p[0] + str(int(p[1:]) + 1), index) for (p, index) in getPrevStates(state, i)]
		print 'hhhh', i, j, state, [(s.get((prevstate, index, j), 0) * transition.get((prevstate, state), 0), j, prevstate) for (prevstate, index) in prevStates]
		if state[0] != 'I':
			i -= 1
		smax, state = max([(s.get((prevstate, index, j), 0) * transition.get((prevstate, state), 0), prevstate) for (prevstate, index) in prevStates])
		print smax, state
		path = state + ' ' + path
		print path
		if state[0] != 'D':
			j -= 1
	print path

#lines = read_file("inp30.txt")
#lines = read_file("AlignmentWithHMMProfile.txt")
lines = read_file("dataset_11632_6.txt")
x = lines[0]
threshold, pseudocount = map(float, str.split(lines[2]))
alphabet = str.split(lines[4])
alignments = lines[6:]
#print threshold
#print alphabet
#print alignments
SequenceAlignmentwithProfileHMM(x, threshold, alphabet, alignments, pseudocount)

def HMMParameterEstimation(x, alphabet, path, states):
	transition = {}
	for i in range(len(path) - 1):
		transition[path[i], path[i + 1]] = transition.get((path[i], path[i + 1]), 0) + 1.0
	#print transition
	Z = {state1:sum([transition.get((state1, state2), 0) for state2 in states]) for state1 in states}
	#print Z
	#transition = {(state1, state2):transition.get((state1, state2), 0) / Z[state1] if Z[state1] else 1.0 / len(states)  for (state1, state2) in transition}	
	#print transition
	print ' ' + ' '.join(states)
	for state1 in states:
		string = state1
		for state2 in states:
			transition[state1, state2] = transition.get((state1, state2), 0.0) / Z[state1] if Z[state1] else 1.0 / len(states)
			string += ' ' + str(transition[state1, state2])
		print string
	print '--------'
	emission = {}
	for i in range(len(x)):
		emission[path[i], x[i]] = emission.get((path[i], x[i]), 0) + 1.0
	Z = {state:sum([emission.get((state, symbol), 0) for symbol in alphabet]) for state in states}
	#emission = {(state, symbol):emission.get((state, symbol), 0) / Z[state] if Z[state] else 1.0 / len(alphabet) for (state, symbol) in emission}	
	print ' ' + ' '.join(alphabet)
	for state in states:
		string = state
		for symbol in alphabet:
			emission[state, symbol] = emission.get((state, symbol), 0.0) / Z[state] if Z[state] else 1.0 / len(alphabet)
			string += ' ' + str(emission[state, symbol])
		print string	
	return transition, emission
	
'''		
#lines = read_file("inp32.txt")
#lines = read_file("HMMParameterEstimation.txt")
lines = read_file("dataset_11632_8.txt")
x = lines[0]
alphabet = str.split(lines[2])
path = lines[4]
states = str.split(lines[6])
#print x
#print alphabet
#print path
#print states
HMMParameterEstimation(x, alphabet, path, states)
'''

def ViterbiDecoding(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * 1 * emission[state, x[0]]
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
	return path
	
def ViterbiLearningForEstimatingParametersOfHMM(niter, x, alphabet, states, transition, emission):
	for i in range(niter):
		path = ViterbiDecoding(x, states, transition, emission)
		print path
		transition, emission = HMMParameterEstimation(x, alphabet, path, states)
		#print 'here1', transition
		#print 'here2', emission
	
'''
#lines = read_file("inp33.txt")
#lines = read_file("ViterbiLearning.txt")
lines = read_file("dataset_11632_10.txt")
niter = int(lines[0])
x = lines[2]
alphabet = str.split(lines[4])
states = str.split(lines[6])
transition, emission = {}, {}
i = 0
for line in lines[9:9+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[9+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(alphabet)):
		emission[states[i], alphabet[j]] = probs[j]
	i += 1
print x
print alphabet
print states
print transition
print emission
ViterbiLearningForEstimatingParametersOfHMM(niter, x, alphabet, states, transition, emission)	
'''

def forward(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = sum([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	s['sink'] = sum([s[statel, n - 1] for statel in states])
	#print s['sink']
	return s
	
def backward(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, n - 1] = 1
	for i in range(n - 2, -1, -1):
		for state in states:
			s[state, i] = sum([s[statel, i + 1] * transition[state, statel] * emission[statel, x[i + 1]] for statel in states])			

	return s

def HMMSoftDecodingProblem(x, states, transition, emission):
	pforward = forward(x, states, transition, emission)
	pbackward = backward(x, states, transition, emission)
	print ' ' + ' '.join(states)
	for i in range(len(x)):
		print ' '.join(map(str, [pforward[state, i] * pbackward[state, i] / pforward['sink'] for state in states]))

'''		
lines = read_file("inp34.txt")
lines = read_file("SoftDecoding.txt")
lines = read_file("dataset_11632_12.txt")
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
#initial = {state: 1.0 / len(states) for state in states}	
#print x
#print transition
#print emission
#print initial
HMMSoftDecodingProblem(x, states, transition, emission)
'''