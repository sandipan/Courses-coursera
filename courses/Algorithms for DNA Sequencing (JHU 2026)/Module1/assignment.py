def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            # ignore header line with genome information
            if not line[0] == '>':
                genome += line.rstrip()
    return genome

def reverseComplement(s):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    t = ''
    for base in s:
        t = complement[base] + t
    return t


def naive(p, t):
    occurrences = []
    for i in range(len(t) - len(p) + 1):
        match = True
        for j in range(len(p)):
            if t[i+j] != p[j]:
                match = False
                break
        if match:
            occurrences.append(i)
    return occurrences

def naivemm(p, t, k):
    occurrences = []
    for i in range(len(t) - len(p) + 1):
        match = True
        count = 0
        for j in range(len(p)):
            if t[i+j] != p[j]:
                if count >= k:
                    match = False
                    break
                count += 1
        if match:
            occurrences.append(i)
    return occurrences

def readFastq(filename):
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline() # skip name line
            seq = fh.readline().rstrip() # read base sequence
            fh.readline() # skip placeholder line
            qual = fh.readline().rstrip() #base quality line
            if len(seq) == 0:
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities

def phred33ToQ(qual):
    return ord(qual) - 33

lambda_genome = readGenome('lambda_virus.fa')
#print(lambda_genome)


def find_occurences(p):
    occurrences =  list(set(naive(p, lambda_genome) + naive(reverseComplement(p), lambda_genome)))
    occurrences = sorted(occurrences)
    print(occurrences, len(occurrences))

#find_occurences('AGGT')
#find_occurences('TTAA')
#find_occurences('ACTAAGT')
#find_occurences('AGTCGA')
#print(naivemm('ABACA', 'ABABBAAB', 2))
#occ = naivemm('TTCAAGCC', lambda_genome, 2)
#print(occ[0], 'TTCAAGCC', lambda_genome[occ[0]:occ[0]+len('TTCAAGCC')])
#print(len(occ))
#occ = naivemm('AGGAGGTT', lambda_genome, 2)
#print(occ[0], 'AGGAGGTT', lambda_genome[occ[0]:occ[0]+len('AGGAGGTT')])
#print(len(occ))

def find_wrong_pos():
    import numpy as np

    genome, qualities = readFastq('ERR037900_1.first1000.fastq')
    qualities = np.array([[phred33ToQ(q) for q in quality] for quality in qualities])
    #print(genome)
    #print(qualities)
    #print(len(qualities[0]))
    #print(qualities.shape)
    print(qualities.mean(axis=0))
    print(np.argmin(qualities.mean(axis=0)))

find_wrong_pos()