"""
iterative depth-first-search on a graph (with frontier_stack and explored_set data-structures)
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def make_adjacency_matrix(n_nodes, density=None):
    """makes a random adjacency matrix representing agraph"""
    n = n_nodes
    p = density or 0.05
    
    while True:
        mx = np.random.rand(n,n)
        mx = np.triu(mx)
        mx += mx.T
        mx = (mx <= p).astype("uint8")
        mx[np.diag_indices(n)] = 0
        assert (mx == mx.T).all()
        
        
        if np.logical_or.reduce(mx, axis=0).all() and np.logical_or.reduce(mx, axis=1).all():
            break
        else:
            p += 0.01
    return(mx)


#display the graph
mx = make_adjacency_matrix(n_nodes=20)
G = nx.from_numpy_matrix(mx)
nx.draw(G, with_labels=True)


###################

def get_frontier(mx, node, explored_list, frontier_stack):
    neighbours_list = [ix for ix,value in enumerate(mx[node]) 
                       if value==1 and (ix not in explored_list)
                       and (ix not in frontier_stack)] 
    return neighbours_list



def dfs(graph, start=None, destination=None):
    start = start or 0

    #initialize
    frontier_stack = []
    explored_list = list()
    
    #zero'th iteration
    frontier_stack.append(start)
    
    #loop
    while frontier_stack:
        explored_node = frontier_stack.pop()
        explored_list.append(explored_node)
        
        #running report
        print("exploring node", explored_node)
        if explored_node == destination:
            print("found the searched for node:", explored_node)
        
        assert len(explored_list) == len(set(explored_list)),"error1"
        
        neighbors = get_frontier(mx, node=explored_node,
                                 explored_list=explored_list,
                                 frontier_stack=frontier_stack)
        
        
        for node in neighbors:
            frontier_stack.append(node)
            assert len(frontier_stack) == len(set(frontier_stack)),"error2"
    
    assert len(frontier_stack)==0,"error3"
    return(explored_list)


#test
explored_list = dfs(graph=mx, start=0, destination=9)
print(explored_list)
