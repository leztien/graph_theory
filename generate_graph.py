"""
contains:
function generating random graphs as per specifications
function traversing a graph with bfs/dfs algorithms
function detecting cycle(s) in a dircted graph
"""


import numpy as np
import networkx as nx


def make_adjacency_matrix(n_nodes, connected=False, directed=False, with_loops=False, 
                          edge_probability=1.0, random_state=None):
    """makes an adjacency matrix representing a random graph"""
    
    #directed or undirected?
    from operator import gt, ne
    condition = ne if directed else gt
    
    #hyper-arguments
    n,p = n_nodes, edge_probability
    nx = [(i,j) for i in range(n) for j in range(n)]
    
    #loop
    while(True):
        #handle randomness
        random_seed = random_state if (type(random_state) is int) else np.random.randint(0, 999)
        rs = np.random.RandomState(random_seed)
        
        #make empty matrix
        mx = np.zeros(shape=(n,n), dtype='uint8')
        
        #fill with ones with probability
        for (i,j) in nx:
            if condition(i,j):
                mx[i,j] = int(rs.rand() <= p)
            if  with_loops and i == j:
                mx[i,j] = int(rs.rand() <= 1/n)
        
        #if user wants a connected graph
        if connected and (type(random_state) is not int) and (0 in mx.sum(0)[:-1]):
            p += 0.001  #increase probability to rule out an infinite loop
            continue
        #after at least one run
        break
    
    #print random seed/state to the console
    if random_state is True: print("random state:", random_seed)
    
    #if not directed
    if not directed:
        mx = mx | mx.T  #symetrical matrix
    
    #remove double edges (if any) from a directed graph
    mxmx = mx + mx.T
    if directed and 2 in mxmx.ravel():
        for (i,j) in nx:
            if mxmx[i,j]==2 and (i > j):
                mx[i,j] = 0
    return mx



def get_neighbors(matrix, node):
    return tuple(matrix[node].nonzero()[0])



def search_graph(matrix, method='bfs', searched_node=None):
    """docstring"""
    
    #search method parameter
    from collections import deque
    stack = deque() if str(method).lower() in ('bfs', 'none') else list()
    
    #define the propper "getter"
    from operator import methodcaller
    popfrom = methodcaller('pop' if isinstance(stack, list) else 'popleft')
    
    #hyper-arguments
    found_node = None
    visited = set()
    start_node = searched_node or 0
    
    #put the start node into the stack/queue
    stack.append(start_node)
    
    while(stack):
        current_node = popfrom(stack)
        #print("exploring node:", current_node)
        if current_node == searched_node: found_node = current_node
        visited.add(current_node)
        neighbors = get_neighbors(matrix, current_node)
        neighbors_to_add = set(neighbors).difference(set(stack)).difference(visited)
        stack.extend(neighbors_to_add)
    print("nodes visited with {}:".format('DFS' if isinstance(stack, list) else 'BFS'), visited)
    return found_node


def detect_cycle(matrix):
    """searches from each node with DFS for a cycle,
       and returns [] if no cycle was detected else a tuple (from-edge, backward-edge-node)"""
    
    cycles = []  # (start-node, backward-edge-node)
    
    for start_node in range(len(matrix)):
        visited = set()
        stack = list()
        stack.append(start_node)  # prime the dfs
        
        while(stack):
            current_node = stack.pop()
            visited.add(current_node)
            children = get_neighbors(matrix, current_node)
            if start_node in children:
                cycles.append((start_node, current_node))
            children_to_add = set(children).difference(set(stack)).difference(visited)
            stack.extend(children_to_add)
    return cycles

##########################################################################################

#make a random graph
mx = make_adjacency_matrix(n_nodes=5, connected=False, directed=True, with_loops=False,
                           edge_probability=0.3, random_state=True)
print(mx)

directed = not (mx == mx.T).all()  # does mx represent a directed graph or not?

#make a networkx-graph-object and draw the graph
G = nx.DiGraph(mx) if directed else nx.from_numpy_array(mx)
nx.draw(G, with_labels=True)

#bfs/dfs search
node = search_graph(mx, method='dfs', searched_node=0)

#detect cycles (if any)
l = detect_cycle(mx)
print(l)

