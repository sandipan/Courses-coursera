def naive(p, t):
    occurrences = []
    for i in range(len(t) - len(p) + 1):  # loop over alignments
        match = True
        for j in range(len(p)):  # loop over characters
            if t[i+j] != p[j]:  # compare characters
                match = False
                break
        if match:
            occurrences.append(i)  # all chars matched; record
    return occurrences

def reverseComplement(s):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    t = ''
    for base in s:
        t = complement[base] + t
    return t
	
def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            # ignore header line with genome information
            if not line[0] == '>':
                genome += line.rstrip()
    return genome
	
def readFastq(filename):
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline()  # skip name line
            seq = fh.readline().rstrip()  # read base sequence
            fh.readline()  # skip placeholder line
            qual = fh.readline().rstrip() # base quality line
            if len(seq) == 0:
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities
	
def naive_with_rc(p, t):
    occurrences = naive(p, t)
    rp = reverseComplement(p)
    if p != rp:
       occurrences += naive(rp, t)
    return occurrences
	   
sequence = readGenome('lambda_virus.fa')
#print qualities[0]

# Q1-2
p =  'TTAA' #'ACCGGCT' #'ATTTG' # 'TTAA' #'AGGT'
#print len(naive_with_rc(p, sequence))

# Q3-4
p = 'AGTCGA' #'AGTCGA' #'ACTAAGT'
#occurrences = naive_with_rc(p, sequence)
#print occurrences
#print sorted(occurrences)[0]

def naive_2mm(p, t):
    occurrences = []
    for i in range(len(t) - len(p) + 1):  # loop over alignments
        match, num_mismatch = True, 0
        for j in range(len(p)):  # loop over characters
            if t[i+j] != p[j]:  # compare characters
                if num_mismatch > 2:
                   match = False
                   break
                else:
                   num_mismatch += 1
        if match:
            occurrences.append(i)  # all chars matched; record
    return occurrences

# Q5-6
p = 'TTCAAGCC' #'TTCAAGCC' 'AGGAGGTT'
#print len(naive_2mm(p, sequence))

p = 'AGGAGGTT' #'TTCAAGCC' 'AGGAGGTT'
#print sorted(naive_2mm(p, sequence))[0]
#print 'CCCTAACCCTAACCCTAACCCTAACCCCAACCCTAACCCTAACCCTAACCCTAACCCTAACCCTAANCCTAACCCTAACCCTAACCCTAACCCTAACCCA'.index('N')