"""
Generate canonical deterministic topologies
"""
import networkx as nx
from fnss.topologies.topology import Topology, DirectedTopology


__all__ = [
    'ring_topology',
    'line_topology',
    'star_topology',
    'full_mesh_topology',
    'k_ary_tree_topology',
    'dumbbell_topology',
    'chord_topology',
           ]


def ring_topology(n):
    """
    Return a ring topology of n nodes
    
    Parameters
    ----------
    n : int
        The number of nodes
        
    Returns
    -------
    topology : A Topology object
    """
    if not isinstance(n, int):
        raise TypeError('n argument must be of int type')
    if n < 1:
        raise ValueError('n argument must be a positive integer')
    G = Topology(nx.path_graph(n))
    G.add_edge(n-1, 0)
    G.name = "ring_topology(%d)" % (n)
    G.graph['type'] = 'ring'
    return G


def line_topology(n):
    """
    Return a line topology of n nodes
    
    Parameters
    ----------
    n : int
        The number of nodes
        
    Returns
    -------
    topology : A Topology object
    
    """
    if not isinstance(n, int):
        raise TypeError('n argument must be of int type')
    if n < 1:
        raise ValueError('n argument must be a positive integer')
    G = Topology(nx.path_graph(n))
    G.name = "line_topology(%d)" % (n)
    G.graph['type'] = 'line'
    return G


def star_topology(n):
    """
    Return a star (a.k.a hub-and-spoke) topology of :math:`n+1` nodes
    
    The root (hub) node has id 0 while all leaf (spoke) nodes have id
    :math:`(1, n+1)`. 
    
    Each node has the attribute type which can either be *root* (for node 0) or
    *leaf* for all other nodes
    
    Parameters
    ----------
    n : int
        The number of leaf nodes

    Returns
    -------
    topology : A Topology object
    """
    if not isinstance(n, int):
        raise TypeError('n argument must be of int type')
    if n < 1:
        raise ValueError('n argument must be a positive integer')
    G = Topology(nx.star_graph(n))
    G.name = "star_topology(%d)" % (n)
    G.graph['type'] = 'star'
    G.node[0]['type'] = 'root'
    for v in range(1, n + 1):
        G.node[v]['type'] = 'leaf'
    return G


def full_mesh_topology(n):
    """
    Return a fully connected mesh topology of n nodes
    
    Parameters
    ----------
    n : int
        The number of nodes

    Returns
    -------
    topology : A Topology object
    """
    if not isinstance(n, int):
        raise TypeError('n argument must be of int type')
    if n < 1:
        raise ValueError('n argument must be a positive integer')
    G = Topology(nx.complete_graph(n))
    G.name = "full_mesh_topology(%d)" % (n)
    G.graph['type'] = 'full_mesh'
    return G


def k_ary_tree_topology(k, h):
    """
    Return a balanced k-ary tree topology of with depth h
    
    Each node has two attributes:
     * type: which can either be *root*, *intermediate* or *leaf*
     * depth:math:`(0, h)` the height of the node in the tree, where 0 is the
       root and h are leaves.
    
    Parameters
    ----------
    k : int
        The branching factor of the tree
    h : int 
        The height or depth of the tree

    Returns
    -------
    topology : A Topology object
    """
    if not isinstance(k, int) or not isinstance(h, int):
        raise TypeError('k and h arguments must be of int type')
    if k <= 1:
        raise ValueError("Invalid k parameter. It should be > 1")
    if h < 1:
        raise ValueError("Invalid h parameter. It should be >=1")
    G = Topology(nx.balanced_tree(k, h))
    G.name = "k_ary_tree_topology(%d,%d)" % (k, h)
    G.graph['type'] = 'tree'
    G.graph['k'] = k
    G.graph['h'] = h
    G.node[0]['type'] = 'root'
    G.node[0]['depth'] = 0
    # Iterate through the tree to assign labels to nodes
    v = 1
    for depth in range(1, h + 1):
        for _ in range(k**depth):
            G.node[v]['depth'] = depth
            if depth == h:
                G.node[v]['type'] = 'leaf'
            else:
                G.node[v]['type'] = 'intermediate'
            v += 1                   
    return G


def dumbbell_topology(m1, m2):
    """
    Return a dumbbell topology consisting of two star topologies
    connected by a path.

    More precisely, two star graphs :math:`K_{m1}` form the left and right
    bells, and are connected by a path :math:`P_{m2}`.

    The :math:`2*m1+m2`  nodes are numbered as follows.
     * :math:`0,...,m1-1` for the left barbell,
     * :math:`m1,...,m1+m2-1` for the path,
     * :math:`m1+m2,...,2*m1+m2-1` for the right barbell.

    The 3 subgraphs are joined via the edges :math:`(m1-1,m1)` and
    :math:`(m1+m2-1,m1+m2)`. If m2 = 0, this is merely two star topologies
    joined together.

    Please notice that this dumbbell topology is different from the barbell 
    graph generated by networkx's barbell_graph function. That barbell graph 
    consists of two complete graphs connected by a path. This consists of two 
    stars whose roots are connected by a path. This dumbbell topology is 
    particularly useful for simulating transport layer protocols. 

    All nodes and edges of this topology have an attribute *type* which can be
    either *right bell*, *core* or *left_bell*

    Parameters
    ----------
    m1 : int
        The number of nodes in each bell
    m2 : int
        The number of nodes in the path

    Returns
    -------
    topology : A Topology object
    """
    if not isinstance(m1, int) or not isinstance(m2, int):
        raise TypeError('m1 and m2 arguments must be of int type')
    if m1 < 2:
        raise ValueError("Invalid graph description, m1 should be >= 2")
    if m2 < 1:
        raise ValueError("Invalid graph description, m2 should be >= 1")

    G = Topology(type='dumbbell')
    G.name = "dumbbell_topology(%d,%d)" % (m1, m2)
    
    # left bell
    G.add_node(m1)
    for v in range(m1):
        G.add_node(v, type='left_bell')
        G.add_edge(v, m1, type='left_bell')
    
    # right bell
    for v in range(m1):
        G.add_node(v + m1 + m2, type='right_bell')
        G.add_edge(v + m1 + m2, m1 + m2 - 1, type='right_bell')
        
    # connecting path
    for v in range(m1, m1 + m2 - 1):
        G.node[v]['type'] = 'core'
        G.add_edge(v, v + 1, type='core')
    G.node[m1 + m2 - 1]['type'] = 'core'
    
    return G


def chord_topology(m, r=1):
    """Return a Chord topology, as described in [1]_:
    
    Chord is a Distributed Hash Table (DHT) providing guaranteed correctness.
    In Chord, both nodes and keys are identified by sequences of :math:`m`
    bits. Keys can be resolved in at most :math:`log(n)` steps (with :math:`n`
    being the number of nodes) as long as each node maintains a routing table
    o :math:`n` entries.
    
    In this implementation, it is possible only to generate topologies with a
    number of nodes :math:`n = 2^m`. where :math:`m` is the length (in bits) of
    the keys used by Chord and also corresponds the the size of the finger
    table kept by each node.
    
    The :math:`r` argument is the number of nearest successors which can be
    optionally kept at each node to guarantee correctness in case of node
    failures.
    
    Parameters
    ----------
    m : int
        The length of keys (in bits), which also corresponds to the length of
        the finger table of each node
    r : int, optional
        The length of the nearest successors table
    
    Returns
    -------
    G : DirectedTopology
        A Chord topology
        
    References
    ----------
    .. [1] I. Stoica, R. Morris, D. Karger, M. Frans Kaashoek, H. Balakrishnan,
           Chord: A Scalable Peer-to-peer Lookup Service for Internet
           Applications. Proceedings of the ACM SIGCOMM 2001 conference on Data
           communication (SIGCOMM '09). ACM, New York, NY, USA.
    """
    if not isinstance(m, int) or not isinstance(r, int):
        raise TypeError("m and r must be integers")
    if m < 2:
        raise ValueError("m must be an integer >= 2")
    if  r < 1 or r > 2**m - 1:
        raise ValueError("r must be an integer and 1 <= r <= 2^m")
    # n is the number of nodes
    n = 2**m
    G = DirectedTopology()
    for v in range(n):
        for u in range(m):
            G.add_edge(v, (v + 2**u) % n)
    if r > 2:
        for v in range(n):
            for u in range(v + 3, v + r + 1):
                G.add_edge(v, u % n)
    return G
    
