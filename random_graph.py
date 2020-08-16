
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def make_graph(n_nodes, density=0.1, return_matrix=True):
    """makes a random graph"""
    n = n_nodes
    p = density
    
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
    return mx if return_matrix else nx.from_numpy_matrix(mx)
    


mx = make_graph(n_nodes=10, density=0.1, return_matrix=True)
G = nx.from_numpy_matrix(mx)
nx.draw(G, with_labels=True)
