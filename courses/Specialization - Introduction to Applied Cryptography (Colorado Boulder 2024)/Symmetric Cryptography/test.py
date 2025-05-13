def cesar(m, k, encrypt=True):
	return ''.join([chr(ord('a') + (ord(x) - ord('a') + k * (1 if encrypt else -1)) % 26)  if x.isalpha() else x for x in m.lower()])

def mono_decrypt(k, m):
	return ''.join([chr(ord('A') + k.find(x)) for x in m.upper()])
	
def Vigenere(k, p, encrypt=True):
	k, m, n = k.upper(), len(k), len(p)
	return ''.join([chr(ord('A') + ((ord(p[i]) - ord('A')) + (1 if encrypt else -1) * (ord(k[i % m]) - ord('A'))) % 26) for i in range(n)])

def permutation(k, p, pad=' '):
	mat = []
	s = 0
	n = len(k)
	while s < len(p):
		mat.append(list(p[s:s+n].ljust(n, pad)))
		s += n
	#print(mat)
	sorted_indices = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(k))]
	print(sorted_indices)
	c = ''
	for j in sorted_indices:
		c += ''.join([x[j] for x in mat])
	return c
	
def railfence(k, p):
	c = [[] for _ in range(k)]
	i = 0
	inc = True
	for x in p:
		c[i].append(x)
		i = i + 1 if inc else i - 1
		if i > k - 1:
			i, inc = k - 2, False
		if i < 0:
			i, inc = 1, True
	#print(c)
	return ''.join(sum(c, []))
	
#print(cesar('meet me later', 2))
#print(cesar(cesar('meet me later', 2), 2, False))
#print(cesar("QNGWFWD", 5, False))
#print(mono_decrypt('DKVQFIBJWPESCXHTMYAUOLRGZN', 'AOVVFAA'))
#print(Vigenere('LEMON', 'DTXSAOMP'))
#print(Vigenere('XO', 'DRAGON'))
#print('RGZNFIBJWPESCXHTMYAUOLDKVQ')
#print(Vigenere('XO', 'RGZNFIBJWPESCXHTMYAUOLDKVQ', False))
#print(permutation([4,3,1,2], 'MEETMELATER'))
#print(permutation([4,3,1,2], 'OKAYSEEYOULATER'))
#print(railfence(4, 'MEETMELATER'))
#print(permutation([2,3,5,4,1], 'MEETMELATER', 'z'))
print(permutation([5,3,1,4,2], cesar('MEETMELATER', 23).upper()))
