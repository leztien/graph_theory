"""
recursive depth-first-search
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


#make adjacency matrix
mx = \
[(0,1,1,1,0,0,0,0,0,0),   #0
 (0,0,0,0,0,0,0,0,0,0),   #1
 (0,0,0,0,1,0,0,0,0,0),   #2
 (0,0,0,0,0,1,0,0,0,0),   #3
 (0,0,0,0,0,0,0,0,0,0),   #4
 (0,0,0,0,0,0,1,1,0,0),   #5
 (0,0,0,0,0,0,0,0,0,0),   #6
 (0,0,0,0,0,0,0,0,1,1),   #7
 (0,0,0,0,0,0,0,0,0,0),   #8
 (0,0,0,0,0,0,0,0,0,0)]   #9
# 0 1 2 3 4 5 6 7 8 9

mx = np.array(mx, dtype=np.uint8)
mx = mx | mx.T


#vizualize the graph
G = nx.from_numpy_matrix(mx)
nx.draw(G, with_labels=True)


#dfs procedure
n = len(mx)  # number fo nodes
visited = [False,]*n
stack = []  #stack
log = []    #optinal log list

def dfs(start, destination=None):
    global mx, visited, log
    
    ix = start
    
    #base case
    if visited[ix] == True:
        return  # backtrack
   
    #recursive case
    visited[ix] = True #mark as visited
    log.append(ix)
    if destination and destination == ix:
        print("found the searched node:", ix)
    
    neigbors = (ix for ix,v in enumerate(mx[ix]) if v==1)
    for node in neigbors:
        dfs(node, destination=destination)
    

#test  
start = 0
destination = 9
dfs(start, destination=9)
print(stack, log)
