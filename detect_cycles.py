"""
two functions detecting a cycle in a directed graph
"""

#utility functions

def make_adjacency_matrix(n_nodes, connected=False, directed=False, with_loops=False, 
                          edge_probability=0.5, random_state=None):
    """makes an adjacency matrix representing a random graph"""
    #imports
    from numpy import random, zeros
    
    #directed or undirected?
    from operator import gt, ne
    condition = ne if directed else gt
    
    #hyper-arguments
    n,p = n_nodes, edge_probability
    nx = [(i,j) for i in range(n) for j in range(n)]
    
    #loop
    while(True):
        #handle randomness
        random_seed = random_state if (type(random_state) is int) else random.randint(0, 999)
        rs = random.RandomState(random_seed)
        
        #make empty matrix
        mx = zeros(shape=(n,n), dtype='uint8')
        
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
            if i > j and mxmx[i,j]==2:
                if random.rand() > 0.5:
                    mx[i,j] = 0
                else: mx[j,i] = 0
    return mx


####################################################################################

def detect_cycle_dfs(matrix):
    """searches from each node with DFS for a cycle,
       and returns [] if no cycle was detected else a tuple (from-edge, backward-edge-node)"""
    
    def get_children(node):
        return tuple(index for (index, value) in enumerate(matrix[node]) if value)
    
    cycles = []  # (start-node, backward-edge-node)
    
    #loop over all nodes
    for start_node in range(len(matrix)):
        visited = set()
        stack = list()
        stack.append(start_node)  # prime the dfs
        
        while(stack):
            current_node = stack.pop()
            visited.add(current_node)
            children = get_children(current_node)
            if start_node in children:
                cycles.append((start_node, current_node))
            children_to_add = set(children).difference(set(stack)).difference(visited)
            stack.extend(children_to_add)
    return cycles




def detect_cycle_recursively(matrix):
    """Returns True if a directed graph has at least one cycle
        Explores the graph with a recursive search.
        The outer loop is iterative. The inner loop is recursive (dfs in effect)"""
    
    def get_children(node):
        return tuple(index for (index, value) in enumerate(matrix[node]) if value)
        
    def recursive_search(node, path):
        children = get_children(node)
        
        #base cases
        if set(path).intersection(set(children)): return True
        if not children: return False
        
        #recursive case (within a for-loop)
        for child in children:
            if child in explored: continue
            
            #recurse deep into the tree
            if recursive_search(child, path+(child,)): return True
        
            #add child to explored
            explored.add(child)
        
        #if no cycled nodes found
        return False
            
        
    #body of the function
    explored = set()
    all_nodes = [i for i in range(len(matrix))]
    
    #for-loop  looping over each node, treating each node as a starting node
    for start_node in all_nodes:
        if start_node in explored: continue
        if recursive_search(start_node, path=tuple()): return True
    
    #after the for-loop
    return False


###########################################################################################



def test(n_nodes, edge_probability=None):
    
    from random import random
    edge_probability = edge_probability or random()
    
    #make a random directed graph
    mx = make_adjacency_matrix(n_nodes=n_nodes, connected=False, directed=True, with_loops=False,
                               edge_probability=edge_probability, random_state=None)
    print(mx)
    
    
    ##
    s = str(mx.tolist()).replace('[', '{').replace(']','}')
    #print(s)
    
    
    #detect cycles
    l = detect_cycle_dfs(mx)
    b = detect_cycle_recursively(mx)
    print(b, bool(l))
    
    
    import re
    p = re.compile("[^01\n]")
    s = p.sub('', str(mx)) + '\n'
    #print(s)
    
    
    #save to file
    path = "/home/linux-ubuntu/Working/data.txt"
    with open(path, mode='wt', encoding='utf_8') as fh:
        fh.write(s)
    

def main():
    from sys import argv
    from sys import exit
    
    edge_probability = None


    if len(argv) < 2:
        print("must provide: number of nodes (and optionally edge probability)")
        exit()
    
    if len(argv) >= 2:
        n_nodes = int(argv[1])
        if n_nodes < 3:
            print("number of nodes must be at least 3")
            exit()
    if len(argv) == 3:
        edge_probability = float(argv[2])

    
    
    print("running with the following arguments:\nnumber of nodes:", n_nodes, "\tedge probability:", edge_probability, "...")
    test(n_nodes=n_nodes, edge_probability=edge_probability)



if __name__ == '__main__': main()
#main()











"""
#make a networkx-graph-object and draw the graph
import networkx as nx
G = nx.DiGraph(mx)
nx.draw(G, with_labels=True)


#test
import networkx as nx
from random import randint, random

n_tests = 20
for no in range(n_tests):
    mx = make_adjacency_matrix(n_nodes=randint(3, 10), edge_probability=random()/2,
                               connected=False, directed=True, with_loops=False)
    G = nx.DiGraph(mx)
    r0 = bool([t for t in nx.simple_cycles(G)])
    r1 = bool(detect_cycle_dfs(mx))
    r2 = detect_cycle_recursively(mx)
    
    print("test {:0>2d}\t".format(no), "OK\t" if r1==r2==r0 else "error\t", r0,r1, r2)
"""





