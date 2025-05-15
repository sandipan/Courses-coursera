# pip install networkx
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from random import random
import operator

def draw_graph(G, i, colors, pr):
	sc = 500000	
	pr1 = map(lambda x: x*sc, pr)
	plt.figure(figsize=(15,15))
	nx.draw_spring(G,  
					 node_color = colors, 
					 #with_labels = True, 
					 node_size = pr1, 
					 edge_color='lightgray' #,
					 #font_size=6,
					 #alpha=0.05
				)
	nn = nx.draw_networkx_labels(G, nx.spring_layout(G), 
							alpha=0.01, 
							font_color='k',
							font_size=6)
	plt.savefig('pr' + str(i) + '.png')
	plt.close()		
	#pr = pr.flatten()
	plt.figure(figsize=(10,10))
	ax = sns.barplot(list(range(1,len(pr)+1)), pr, color='g')
	ax.set_xticks([])
	ax.set_xlabel('nodes')
	ax.set_ylabel('page rank')
	ax.set_title('page ranks of nodes at iteration' + str(i+1))
	plt.savefig('pr' + str(i) + 'g.png')
	plt.close()		

def pr(I, T, n=5, G=None):
	#sc = 500000	
	#print T
	if G:
		ss = nx.get_node_attributes(G, u'source')
		cmap = {s:(random(), random(), random()) for s in set(ss.values())}
		colors = [cmap[s] for s in ss.values()]
		draw_graph(G, 0, colors, I) #map(lambda x: x*sc, I))
	for i in range(n):
		#I = np.matmul(T, I)
		I = np.matmul(I, T) 
		I = np.squeeze(np.asarray(I))
		#I /= np.sum(I)
		print i+1, np.sum(I), I.shape, np.sum(I), I, sum(I)
		if G:
			draw_graph(G, i+1, colors, I) #map(lambda x: x*sc, I))
	ns = G.nodes()
	print('A', [(ns[i],I[i]) for i in np.argsort(I)[::-1][:5]])		
	if G:
		print('B', sorted(nx.pagerank(G, alpha=0.85).items(), key=operator.itemgetter(1), reverse=True)[:10])		
			
def hits(h, a, A, n=5):
	for i in range(n):
		#a = np.matmul(np.matmul(A.T, A), a) / sum(a)
		#h = np.matmul(np.matmul(A, A.T), h) / sum(h)
		a = np.matmul(A.T, h)  # in-degrees
		h = np.matmul(A, a)    # out-degrees	
		a, h = np.round(a / sum(a),2), np.round(h / sum(h),2)
		print i+1, h, a

def exercise():

	G=nx.Graph()
	G.add_nodes_from(['A','B','C','D','E','F','G'])
	G.add_edges_from([('A','B'),('B','D'),('C','D'),('A','C'),('D','E'),('C','E'),('D','G'),('E','G'),('G','F')])

	#nx.draw_networkx(G)
	#plt.show()

	print nx.degree_centrality(G)['D']
	print nx.closeness_centrality(G)['G']
	print nx.betweenness_centrality(G, normalized=True, endpoints=False)['G']
	print nx.edge_betweenness_centrality(G, normalized=False)[('G', 'F')]

	G=nx.DiGraph()
	G.add_nodes_from(['A','B','C','D'])
	G.add_edges_from([('A','B'),('B','C'),('A','C'),('C','A'),('D','C')])

	#print nx.hits(G, max_iter=2, tol=0.05, nstart=None, normalized=True)
	#print nx.pagerank(G, max_iter=1, tol=0.5, nstart=None)
	#print nx.pagerank(G, max_iter=2, tol=0.5, nstart=None)
	#print sum(nx.pagerank(G, max_iter=2, tol=0.5, nstart=None).values())
	
	#pr(np.array([1/5.]*5), np.array([[0,1,0,0,0],[0,0,.5,.5,0],[0,1,0,0,0],[1/3.,0,1/3.,0,1/3.],[1,0,0,0,0]]).T)		T column-stochastic
	pr(np.array([1/4.]*4), np.array([[0,1/2.,1/2.,0],[0,0,1,0],[1,0,0,0],[0,0,1,0]]).T)		
	#hits(np.array([1.]*8), np.array([1.]*8), np.array([[0,0,0,1.,0,0,0,0],[0,0,1.,0,1.,0,0,0],[1.,0,0,0,0,0,0,0],[0,1.,1.,0,0,0,0,0],[0,1.,1.,1.,0,1.,0,0],[0,0,1.,0,0,0,0,1.],[1.,0,1.,0,0,0,0,0],[1.,0,0,0,0,0,0,0]]))		
	hits(np.array([1.]*4), np.array([1.]*4), np.array([[0,1.,1.,0],[0,0,1.,0],[1.,0,0,0],[0,0,1.,0]]))		
		

def run_pr():

	G = nx.read_gml('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\blogs.gml')
	T = nx.to_numpy_matrix(G)
	print T.shape
	T = 0.85*T + 0.15*(1./T.shape[0])*np.ones((T.shape[0], T.shape[1]))
	#T /= T.sum(axis=1)[:,None] # make row stochastic
	#T = (T.T/T.sum(axis=1)).T # make row stochastic
	for i in range(T.shape[0]):
		S = np.sum(T[i,:])
		if S > 0:
			T[i,:] = T[i,:] / S # make row stochastic
	print T.sum(axis=1)
	print T.T
	plt.imshow(10**6*T.T,cmap='hot',origin='lower',aspect='auto')
	plt.show()
	I = np.array([1./T.shape[0]]*T.shape[0])
	max_iter = 25
	pr(I, T, max_iter, G)	
	
run_pr()	