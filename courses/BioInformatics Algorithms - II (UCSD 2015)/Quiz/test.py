def BWT(pat):
	pats = []
	for i in xrange(len(pat)):
		pats += [pat[i:]+pat[:i]]
	print sorted(pats)
	print ''.join([x[-1] for x in sorted(pats)])

def IBWT(pat):
	n = len(pat)
	pat1 = sorted(pat)
	while(True):
		pat1 = sorted([pat[i] + pat1[i] for i in xrange(n)])
		print pat1
		if (len(pat1[0]) == n):
			break
	print ([x for x in pat1 if x[-1] == '$'])
	
#IBWT('annb$aa')
#IBWT('e$elplepa')
#IBWT('TTACA$AAGTC')
#BWT("banana$")
#BWT("CACTTAAAGT$")

#BWT("ACCAACACTG$")
IBWT('TTCCATTGGA$')
#BWT("TGTACCATGT$")