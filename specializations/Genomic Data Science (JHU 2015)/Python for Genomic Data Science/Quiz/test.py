# lecture 3
type([1e-10,(1,2),"BGP",[3]])
t = ('a', 'c', 'g', 't')
t.append( ('A','C','G','T') ) 
print len(t)
dna=input("Enter DNA sequence:") 
dna_counts={'t':dna.count('t'),'c':dna.count('c'),'g':dna.count('g'),'a':dna.count('a')} 
nt=sorted(dna_counts.keys()) 
print(nt[-1])
dna = 'aaacctg'
dna_counts={'t':dna.count('t'),'c':dna.count('c'),'g':dna.count('g'),'a':dna.count('a')}
max_freq=sorted(dna_counts.values())[-1]
L1, L2 = [1,2,2], [2,3]
L3 = list(set(L1)&set(L2))

# lecture 4
seq='abc'
for i in range(len(seq)+1) :    # line 1 
        for j in range(i) :        # line 2 
                print(seq[j:i])     # line 3 
 
i=0 
while i<len(seq) : 
     j=0 
     while(j<i) : 
         print(seq[j:i]) 
         j+=1 
     i+=1 

mylist=[1,2,3,3]

d = {} 
result = False 
for x in mylist: 
     if x in d: 
       result=True 
       break 
     d[x] = True 

d = {} 
result = False 
for x in mylist: 
     if not x in d: 
       d[x]=True 
       continue 
     result = True 
	 
i,j=1,1
while i< 2048 : 
	i,j=2*i,j+1
range(1,-23,-3)

# lecture 5
def function2(length): 
    while length > 0: 
        print(length) 
        function2(length - 1) 

def valid_dna3(dna): 
    for c in dna: 
       flag = c in 'acgtACGT' 
    return flag 

def f(mystring): 
	print(message) 
	print(mystring) 
	message="Inside function now!" 
	print(message) 
message="Outside function!" 
f("Test function:")

#def afunction(a1 = 1, a2): 
#	pass

# lecture 6

import random

def create_dna(n, alphabet='acgt'): 
     return ''.join([random.choice(alphabet) for i in range(n)]) 

dna = create_dna(1000000)

def count1(dna, base): 
     i = 0 
     for c in dna: 
         if c == base: 
             i += 1 
     return i 

def count2(dna, base): 
     i = 0 
     for j in range(len(dna)): 
         if dna[j] == base: 
             i += 1 
     return i 

def count3(dna, base): 
     match = [c == base for c in dna] 
     return sum(match) 

def count4(dna, base): 
     return dna.count(base) 

def count5(dna, base): 
     return len([i for i in range(len(dna)) if dna[i] == base]) 

def count6(dna,base): 
     return sum(c == base for c in dna) 

import time

time1 = time.clock()
count1(dna, 'a')
time2 = time.clock()
print time2 - time1

time1 = time.clock()
count2(dna, 'a')
time2 = time.clock()
print time2 - time1

time1 = time.clock()
count3(dna, 'a')
time2 = time.clock()
print time2 - time1

time1 = time.clock()
count4(dna, 'a')
time2 = time.clock()
print time2 - time1

time1 = time.clock()
count5(dna, 'a')
time2 = time.clock()
print time2 - time1

time1 = time.clock()
count6(dna, 'a')
time2 = time.clock()
print time2 - time1

# lecture 7

def get_extension1(filename): 
     return(filename.split(".")[-1]) 

def get_extension2(filename): 
     import os.path 
     return(os.path.splitext(filename)[1]) 

def get_extension3(filename): 
     return filename[filename.rfind('.'):][1:] 

import os 
filenames = os.listdir('mydir') 
f= open(filenames[0])

# BioPython
from Bio.Blast import NCBIWWW
fasta_string = "TGGGCCTCATATTTATCCTATATACCATGTTCGTATGGTGGCGCGATGTTCTACGTGAATCCACGTTCGAAGGACATCATACCAAAGTCGTACAATTAGGACCTCGATATGGTTTTATTCTGTTTATCGTATCGGAGGTTATGTTCTTTTTTGCTCTTTTTCGGGCTTCTTCTCATTCTTCTTTGGCACCTACGGTAGAG"
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
from Bio.Blast import NCBIXML
blast_record = NCBIXML.read(result_handle)
len(blast_record.alignments)
E_VALUE_THRESH = 0.01
eval_seq = {}
for alignment in blast_record.alignments:
	for hsp in alignment.hsps:
		if hsp.expect < E_VALUE_THRESH:
			#print('****Alignment****')
			print('sequence:', alignment.title)
			#print('length:', alignment.length)
			print('e value:', hsp.expect)
			eval_seq[hsp.expect] = eval_seq.get(hsp.expect, []) + [alignment.title]
			#print(hsp.query)
			#print(hsp.match)
			#print(hsp.sbjct)

print [(k, eval_seq[k]) for k in sorted(eval_seq)[:5]]			

from Bio.Seq import Seq 
seq = Seq('TGGGCCTCATATTTATCCTATATACCATGTTCGTATGGTGGCGCGATGTTCTACGTGAATCCACGTTCGAAGGACATCATACCAAAGTCGTACAATTAGGACCTCGATATGGTTTTATTCTGTTTATCGTATCGGAGGTTATGTTCTTTTTTGCTCTTTTTCGGGCTTCTTCTCATTCTTCTTTGGCACCTACGGTAGAG')
print seq.translate()
