
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 3
# 
# In this assignment you will explore measures of centrality on two networks, a friendship network in Part 1, and a blog network in Part 2.

# ## Part 1
# 
# Answer questions 1-4 using the network `G1`, a network of friendships at a university department. Each node corresponds to a person, and an edge indicates friendship. 
# 
# *The network has been loaded as networkx graph object `G1`.*

# In[13]:

import networkx as nx
get_ipython().magic(u'matplotlib inline')
import matplotlib.pylab as plt
import seaborn as sns

G1 = nx.read_gml('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friendships.gml')


# In[15]:

d = max([G1.degree(n) for n in G1.nodes()])
plt.figure(figsize=(15,15))
nx.draw_spring(G1,  
                 node_color = [(0, G1.degree(n)/float(d), (G1.degree(n)/float(d))**0.5) for n in G1.nodes()], 
                 with_labels = True, 
                 node_size = [10000*G1.degree(n)/float(d) for n in G1.nodes()],
                 edge_color='lightgray')


# In[62]:

print(len(G1.nodes()), len(G1.edges()))
dc = nx.degree_centrality(G1)
#print(dc)
plt.figure(figsize=(10,10))
sns.distplot(dc.values())


# In[77]:

from graphviz import Graph
from IPython.display import Image
s = Graph('friendnet', node_attr={'shape': 'plaintext'}, format='png',engine='sfdp') #,engine='circo') #engine='neato')
s.attr('node', style='filled', color='lightblue2', shape='circle')
s.attr('edge', color='saddlebrown')
m, M = float(min(dc.values())), float(max(dc.values()))
for e in G1.edges():
    #print(str(dc[e[0]]/m) + ' ' + str(dc[e[0]]/m) + ' 0')
    s.node(str(e[0]), **{'width':str(4*(dc[e[0]]-m)/(M-m)+1), 'height':str(4*(dc[e[0]]-m)/(M-m)+1), #'style':'filled',
                         #'fillcolor': '0.5 0.3 0.2 ' + str(dc[e[0]]/M), 
                         'fillcolor':'gold',
                         'color':'fuchsia',
                         'penwidth':'5',
                         'fontsize':str(40)})
    s.node(str(e[1]), **{'width':str(4*(dc[e[1]]-m)/(M-m)+1), 'height':str(4*(dc[e[1]]-m)/(M-m)+1), #'style':'filled', 
                         #'fillcolor':'0.5 0.3 0.2 ' + str(dc[e[1]]/M), 
                         'fillcolor':'gold',
                         'color':'fuchsia',
                         'penwidth':'5',
                         'fontsize':str(40)})
    s.edge(str(e[0]),str(e[1]), penwidth='2')
s.render('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends', view=False)
Image(filename='C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends.png')#,width=200, height=2000)     


# In[71]:

print(len(G1.nodes()), len(G1.edges()))
cc = nx.closeness_centrality(G1)
#print(dc)
plt.figure(figsize=(10,10))
sns.distplot(cc.values())


# In[78]:

from graphviz import Graph
from IPython.display import Image
s = Graph('friendnet', node_attr={'shape': 'plaintext'}, format='png',engine='sfdp') #,engine='circo') #engine='neato')
s.attr('node', style='filled', color='lightblue2', shape='circle')
s.attr('edge', color='firebrick')
m, M = float(min(cc.values())), float(max(cc.values()))
for e in G1.edges():
    s.node(str(e[0]), **{'width':str(4*(cc[e[0]]-m)/(M-m)+1), 'height':str(4*(cc[e[0]]-m)/(M-m)+1), #'style':'filled',
                         #'fillcolor': '0.5 0.3 0.2 ' + str(dc[e[0]]/M), 
                         'fillcolor':'forestgreen',
                         'color':'greenyellow',
                         'penwidth':'5',
                         'fontsize':str(60)})
    s.node(str(e[1]), **{'width':str(4*(cc[e[1]]-m)/(M-m)+1), 'height':str(4*(cc[e[1]]-m)/(M-m)+1), #'style':'filled', 
                         #'fillcolor':'0.5 0.3 0.2 ' + str(dc[e[1]]/M), 
                         'fillcolor':'forestgreen',
                         'color':'greenyellow',
                         'penwidth':'5',
                         'fontsize':str(60)})
    s.edge(str(e[0]),str(e[1]), penwidth='2')
s.render('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends2', view=False)
Image(filename='C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends2.png')#,width=200, height=2000)     


# In[108]:

print(len(G1.nodes()), len(G1.edges()))
bc = nx.betweenness_centrality(G1)
#print(dc)
plt.figure(figsize=(10,10))
sns.distplot(bc.values())
plt.xlabel('betweenness centrality'); plt.ylabel('count')


# In[74]:

from graphviz import Graph
from IPython.display import Image
s = Graph('friendnet', node_attr={'shape': 'plaintext'}, format='png',engine='sfdp') #,engine='circo') #engine='neato')
s.attr('node', style='filled', color='lightblue2', shape='circle')
s.attr('edge', color='steelblue')
m, M = float(min(bc.values())), float(max(bc.values()))
for e in G1.edges():
    s.node(str(e[0]), **{'width':str(4*(bc[e[0]]-m)/(M-m)+1), 'height':str(4*(bc[e[0]]-m)/(M-m)+1), #'style':'filled',
                         #'fillcolor': '0.5 0.3 0.2 ' + str(dc[e[0]]/M), 
                         'fillcolor':'sandybrown',
                         'color':'dodgerblue4',
                         'penwidth':'5',
                         'fontsize':str(40)})
    s.node(str(e[1]), **{'width':str(4*(bc[e[1]]-m)/(M-m)+1), 'height':str(4*(bc[e[1]]-m)/(M-m)+1), #'style':'filled', 
                         #'fillcolor':'0.5 0.3 0.2 ' + str(dc[e[1]]/M), 
                         'fillcolor':'sandybrown',
                         'color':'dodgerblue4',
                         'penwidth':'5',
                         'fontsize':str(40)})
    s.edge(str(e[0]),str(e[1]), penwidth='2')
s.render('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends3', view=False)
Image(filename='C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\friends3.png')#,width=200, height=2000)     


# ### Question 1
# 
# Find the degree centrality, closeness centrality, and normalized betweeness centrality (excluding endpoints) of node 100.
# 
# *This function should return a tuple of floats `(degree_centrality, closeness_centrality, betweenness_centrality)`.*

# In[2]:

def answer_one():
        
    # Your Code Here
    
    return (nx.degree_centrality(G1)[100], nx.closeness_centrality(G1)[100], nx.betweenness_centrality(G1, normalized=True, endpoints=False)[100]) # Your Answer Here
#answer_one()


# <br>
# #### For Questions 2, 3, and 4, use one of the covered centrality measures to rank the nodes and find the most appropriate candidate.
# <br>

# ### Question 2
# 
# Suppose you are employed by an online shopping website and are tasked with selecting one user in network G1 to send an online shopping voucher to. We expect that the user who receives the voucher will send it to their friends in the network.  You want the voucher to reach as many nodes as possible. The voucher can be forwarded to multiple users at the same time, but the travel distance of the voucher is limited to one step, which means if the voucher travels more than one step in this network, it is no longer valid. Apply your knowledge in network centrality to select the best candidate for the voucher. 
# 
# *This function should return an integer, the name of the node.*

# In[29]:

def answer_two():
        
    # Your Code Here
    import operator
    return max(nx.degree_centrality(G1).items(), key=operator.itemgetter(1))[0]
 # Your Answer Here
#answer_two()


# ### Question 3
# 
# Now the limit of the voucher’s travel distance has been removed. Because the network is connected, regardless of who you pick, every node in the network will eventually receive the voucher. However, we now want to ensure that the voucher reaches the nodes in the lowest average number of hops.
# 
# How would you change your selection strategy? Write a function to tell us who is the best candidate in the network under this condition.
# 
# *This function should return an integer, the name of the node.*

# In[30]:

def answer_three():
        
    # Your Code Here
    import operator
    return max(nx.closeness_centrality(G1).items(), key=operator.itemgetter(1))[0]
#answer_three()


# ### Question 4
# 
# Assume the restriction on the voucher’s travel distance is still removed, but now a competitor has developed a strategy to remove a person from the network in order to disrupt the distribution of your company’s voucher. Identify the single riskiest person to be removed under your competitor’s strategy?
# 
# *This function should return an integer, the name of the node.*

# In[31]:

def answer_four():
        
    # Your Code Here
    import operator
    return max(nx.betweenness_centrality(G1, normalized=True, endpoints=False).items(), key=operator.itemgetter(1))[0]
#answer_four()


# ## Part 2
# 
# `G2` is a directed network of political blogs, where nodes correspond to a blog and edges correspond to links between blogs. Use your knowledge of PageRank and HITS to answer Questions 5-9.

# In[90]:

import pandas as pd
G2 = nx.read_gml('C:\courses\Coursera\Past\Specialization-UMich Applied Data Science with Python\Social Network Analysis Python\Week3\\blogs.gml')
#print(G2.nodes(data=True))
#print(G2.edges(data=True))
#print(nx.get_node_attributes(G2, u'source'))
df = pd.DataFrame(index=G2.nodes())
df[u'source'] = pd.Series(nx.get_node_attributes(G2, u'source'))
df[u'value'] = pd.Series(nx.get_node_attributes(G2, u'value'))
print(len(df[u'source'].unique()))
df.head(20)    


# In[92]:

from random import random
ss = nx.get_node_attributes(G2, u'source')
cmap = {s:(random(), random(), random()) for s in set(ss.values())}
colors = [cmap[s] for s in ss.values()]
d = max([G2.degree(n) for n in G2.nodes()])
plt.figure(figsize=(15,15))
nx.draw_spring(G2,  
                 node_color = colors, 
                 with_labels = True, 
                 node_size = [10000*G2.degree(n)/float(d) for n in G2.nodes()],
                 edge_color='lightgray',
                 font_size=6)


# In[93]:

plt.figure(figsize=(15,15))
nx.draw_spring(G2,  
                 node_color = colors, 
                 with_labels = False, 
                 node_size = [10000*G2.degree(n)/float(d) for n in G2.nodes()],
                 edge_color='lightgray')


# ### Question 5
# 
# Apply the Scaled Page Rank Algorithm to this network. Find the Page Rank of node 'realclearpolitics.com' with damping value 0.85.
# 
# *This function should return a float.*

# In[32]:

def answer_five():
        
    # Your Code Here
    
    return nx.pagerank(G2, alpha=0.85)['realclearpolitics.com'] # Your Answer Here
#answer_five()


# In[103]:

pr = nx.pagerank(G2, alpha=0.85)
pr = [500000*pr[n] for n in G2.nodes()]
#print pr


# In[104]:

plt.figure(figsize=(15,15))
nx.draw_spring(G2,  
                 node_color = colors, 
                 with_labels = True, 
                 node_size = pr,
                 edge_color='lightgray',
                 font_size=6)


# ### Question 6
# 
# Apply the Scaled Page Rank Algorithm to this network with damping value 0.85. Find the 5 nodes with highest Page Rank. 
# 
# *This function should return a list of the top 5 blogs in desending order of Page Rank.*

# In[105]:

def answer_six():
        
    # Your Code Here
    import operator
    return [x[0] for x in sorted(nx.pagerank(G2, alpha=0.85).items(), key=operator.itemgetter(1), reverse=True)[:5]]
answer_six()


# In[109]:

print(len(G2.nodes()), len(G2.edges()))
pr = nx.pagerank(G2, alpha=0.85)
#print(dc)
plt.figure(figsize=(10,10))
sns.distplot(pr.values())
plt.xlabel('page-rank'); plt.ylabel('count')


# ### Question 7
# 
# Apply the HITS Algorithm to the network to find the hub and authority scores of node 'realclearpolitics.com'. 
# 
# *Your result should return a tuple of floats `(hub_score, authority_score)`.*

# In[110]:

def answer_seven():
        
    # Your Code Here
    hubs, authorities = nx.hits(G2)
    return hubs['realclearpolitics.com'], authorities['realclearpolitics.com'] # Your Answer Here
answer_seven()


# ### Question 8 
# 
# Apply the HITS Algorithm to this network to find the 5 nodes with highest hub scores.
# 
# *This function should return a list of the top 5 blogs in desending order of hub scores.*

# In[111]:

def answer_eight():
        
    # Your Code Here
    import operator
    hubs, authorities = nx.hits(G2)
    return [x[0] for x in sorted(hubs.items(), key=operator.itemgetter(1), reverse=True)[:5]]
answer_eight()


# ### Question 9 
# 
# Apply the HITS Algorithm to this network to find the 5 nodes with highest authority scores.
# 
# *This function should return a list of the top 5 blogs in desending order of authority scores.*

# In[112]:

def answer_nine():
        
    # Your Code Here
    import operator
    hubs, authorities = nx.hits(G2)
    return [x[0] for x in sorted(authorities.items(), key=operator.itemgetter(1), reverse=True)[:5]]
answer_nine()


# In[120]:

hubs, authorities = nx.hits(G2)
hubs = [2000000*hubs[n] for n in G2.nodes()]
authorities = [500000*authorities[n] for n in G2.nodes()]


# In[121]:

plt.figure(figsize=(15,15))
nx.draw_spring(G2,  
                 node_color = colors, 
                 with_labels = True, 
                 node_size = hubs,
                 edge_color='lightgray',
                 font_size=6)


# In[119]:

plt.figure(figsize=(15,15))
nx.draw_spring(G2,  
                 node_color = colors, 
                 with_labels = True, 
                 node_size = authorities,
                 edge_color='lightgray',
                 font_size=6)


# In[126]:

hubs, authorities = nx.hits(G2)
plt.figure(figsize=(10,10))
sns.distplot(hubs.values())
plt.xlabel('hub scores with HITS'); plt.ylabel('count')


# In[128]:

plt.figure(figsize=(10,10))
sns.distplot(authorities.values())
plt.xlabel('authority scores with HITS'); plt.ylabel('count')
#fig, ax = plt.subplots()
#for a in [hubs.values(), authorities.values()]:
#    sns.distplot(a, ax=ax, kde=True)
#ax.set_xlim([0, 1])

