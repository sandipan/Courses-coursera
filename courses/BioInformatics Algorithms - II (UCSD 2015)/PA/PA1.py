import os.path
from graphviz import Digraph

n = 0
def plot_tree(tr):
    global n
    s = Digraph('suffix_tree', node_attr={'shape': 'circle', 'size':'1', 'style': 'filled', 'fillcolor': '#996633'}, format='png')
    for node in tr:
        s.node(str(node), label='')
        nbrs = tr[node]
        for e in nbrs:
            s.node(str(nbrs[e]), label='')
            s.edge(str(node), str(nbrs[e]), label=e)
    s.render('st/tree' + str(n), view=False)
    n += 1	
			
def SuffixTreeConstruction(text):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	for suffix in suffixes:
		node, done = root, False
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						id += 1
						del tree[node][string]
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
					elif lcp == lstr and lcp == lsuffix:
						done = True
					#plot_tree(tree)	
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		plot_tree(tree)	
		#print suffix, tree
	print tree
	texts = sum([x.keys() for x in tree.values()], [])
	leaves = 0
	for x in texts:
		print x
		if '$' in x:
			leaves += 1
	print leaves
	
#SuffixTreeConstruction("ATAAATG$")
#SuffixTreeConstruction("panamabananas$")
#SuffixTreeConstruction("ATCTACCAGCAGTGAACATGGGAGGACCAGTAAGGAAGGCTTACCCTCGATGTGTTACAGACTCGTTCGTAGGGTGTATAACGCCGCCGCTGG$")
#SuffixTreeConstruction("TCTGAGCCCTACTGTCGAGAAATATGTATCTCGCCCCCGCAGCTT$")

def LongestRepeat(text):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	max_repeated_text = ''
	for suffix in suffixes:
		node, done = root, False
		repeated_text = ''
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						id += 1
						del tree[node][string]
						repeated_text += cp
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
						repeated_text += cp
					elif lcp == lstr and lcp == lsuffix:
						done = True
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		#print suffix, tree
		print 'here', repeated_text
		if len(max_repeated_text) < len(repeated_text):
			max_repeated_text = repeated_text
	
	#print tree
	plot_tree(tree)	
	#texts = sum([x.keys() for x in tree.values()], [])
	#for x in texts:
	#	print x
	print max_repeated_text

#LongestRepeat("ATATCGTTTTATCGTT$")
LongestRepeat("GCGACCCACCGAGACCAACCTAGTACCGTATCTTGCGCCCGGTGGCATGCTTTCTAGCGCATACGAAAACCGTGAGACGGGTGGTCGTCCGATAGATCAGCACGCGTGTGGATCCTTGTCTAGGAGGAAGGGGTCCTCATCTGTTCTCCAGCTGCCACGGGTCAAGGCGAGCTGACATTGTCTCGAGGCCCGTATGATACCTCTCAAAAGCGTCTGCCCGGTACGCGTAACTAGTGGGTACCGTATCTTGCGCCCGGTGGCATGCTTTCTAGCGCATACGAAAACCGTGAGAATGCGTTCTCTCTCCCACGCCCCGTAGGACCATCGTAAAACGAGCAGATCCGACGTCAACAGGGTTTGCGACTCTCTCCATTCCGCCTTAATGGAGTCGAGGCGGGCGACCAGCATAAGAGATAGAATGACTTGTGTCCGGACGTGAGTATCCGTTATGTGTACATTCGTGTGGGTTGATGATCCTACCGTGAAGTGCCAAGCAAGTCGCCGTTCCTAGCCCCCAAAACGAAGGTCATGCTGTGTATCGCTCATGGCTGGAAGAGGTTGCTACAGGGATGGAAGACCGGCCATGTAGAAGCGACGATCTGATATTCATACTTGGCCTCAAACCTCTTCCTTGATTTGCACTACTTTGCGAGACTTTCAAATTTTTGCGCAGGAGCTCAGAACAGGGCTATCCGCACATTTAGGTTGGGTGTTACCCCTTCTATGGGTGTACATCTGTTTTCCTGATGGCTACGCAATGCTCAAGCAACCATTTCGTGCAACGATGACCGCTGACAGTAACTAGCATATCTAGTGGGAGGTGAGCTAGTAGGTGCGTACAAAGATCGGTGAAGAATCAAGTGGGTACCGTATCTTGCGCCCGGTGGCATGCTTTCTAGCGCATACGAAAACCGTGAGCCGTCGTTTACTCAGCCGGGTCATTCTAGCATTCACGGGTCTGTTTTTATGATAAACGCCCGGTGACTCTCACGTATGCGCGCACCATCGGACTGCCGGACGCGAGCAAAGTATTACTACCGTCCTGCAGGCAGGCCCTATTCCGCGTAGGAGAACTCACCCCCGCGGAATGAATAGGGGGTAGGTTAAAAAAGCGGAATTCCTCACCGGATCCCCGCACCGATGCAGTCCAAGTTCCTAGTGA$")
