"""
recursive depth-first-search
"""

g = \
[(0,1,1,1,0,0,0,0,0,0),   #0
 (1,0,0,0,0,0,0,0,0,0),   #1
 (1,0,0,0,1,0,0,0,0,0),   #2
 (1,0,0,0,0,1,0,0,0,0),   #3
 (0,0,1,0,0,0,0,0,0,0),   #4
 (0,0,0,1,0,0,1,1,0,0),   #5
 (0,0,0,0,0,1,0,1,0,0),   #6
 (0,0,0,0,0,1,1,0,1,1),   #7
 (0,0,0,0,0,0,0,1,0,0),   #8
 (0,0,0,0,0,0,0,1,0,0)]   #9

#display the graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

am = np.array(g)
G = nx.from_numpy_matrix(am)
nx.draw(G, with_labels=True)

#
n = len(g)
visited = [False,]*n
log = []
stack = []


def dfs(ix):
    global g, visited, log
    
    #log.append(ix)
    
    #base case
    if visited[ix] == True:
        #log.append(ix)
        return  # backtrack
   
    #recursive case
    visited[ix] = True #mark as visited
    #log.append(ix)
    
    neigbors = (ix for ix,v in enumerate(g[ix]) if v==1)
    for node in neigbors:
        dfs(node)
    
    
start = 0
dfs(start)
print(log)
