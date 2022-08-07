import numpy as np
import networkx as nx
from networkx.algorithms import tree
from factor import Factor
from factor_utils import factor_product


""" ADD HELPER FUNCTIONS HERE (IF NEEDED) """
from functools import reduce

def show_graph(G):
    nx.draw_networkx(G, with_labels=True, font_weight='bold', node_size=1000, arrowsize=20)
    import matplotlib.pyplot as plt
    plt.axis('off')
    plt.show()

""" END ADD HELPER FUNCTIONS HERE """


def _get_clique_factors(jt_cliques, factors):
    """
    Assign node factors to cliques in the junction tree and derive the clique factors.

    Args:
        jt_cliques: list of junction tree maximal cliques e.g. [[x1, x2, x3], [x2, x3], ... ]
        factors: list of factors from the original graph

    Returns:
        list of clique factors where the factor(jt_cliques[i]) = clique_factors[i]
    """
    #clique_factors = [Factor() for _ in jt_cliques]
    clique_factors = []
    #print("_get_clique_factors", jt_cliques, factors)

    """ YOUR CODE HERE """
    visited = []
    for jt_clique in jt_cliques:
        clique_factor = []
        for factor in factors:
            if factor in visited:
                continue
            if set(factor.var) <= set(jt_clique):
                clique_factor.append(factor)
                visited.append(factor)
        clique_factors.append(reduce(factor_product, clique_factor))

    #cliques = [[factors[j] for j in i] for i in jt_cliques]
    #clique_factors = [reduce(factor_product, clique) for clique in cliques]

    """ END YOUR CODE HERE """

    assert len(clique_factors) == len(jt_cliques), 'there should be equal number of cliques and clique factors'
    #print("_get_clique_factors return", clique_factors)
    return clique_factors


def _get_jt_clique_and_edges(nodes, edges):
    """
    Construct the structure of the junction tree and return the list of cliques (nodes) in the junction tree and
    the list of edges between cliques in the junction tree. [i, j] in jt_edges means that cliques[j] is a neighbor
    of cliques[i] and vice versa. [j, i] should also be included in the numpy array of edges if [i, j] is present.
    You can use nx.Graph() and nx.find_cliques().

    Args:
        nodes: numpy array of nodes [x1, ..., xN]
        edges: numpy array of edges e.g. [x1, x2] implies that x1 and x2 are neighbors.

    Returns:
        list of junction tree cliques. each clique should be a maximal clique. e.g. [[X1, X2], ...]
        numpy array of junction tree edges e.g. [[0,1], ...], [i,j] means that cliques[i]
            and cliques[j] are neighbors.
    """
    #jt_cliques = []
    #jt_edges = np.array(edges)  # dummy value
    jt_edges = []
    #print("_get_jt_clique_and_edges", nodes, edges)

    """ YOUR CODE HERE """
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    # triangulation
    visited = []
    for node in nodes:
        neighbors = G.neighbors(node)
        neighbors = [n for n in neighbors if n not in visited]
        for neighborA in neighbors:
            for neighborB in neighbors:
                if neighborA == neighborB:
                    continue
                if not G.has_edge(neighborA, neighborB):
                    G.add_edge(neighborA, neighborB)
        visited += [node]

    #show_graph(G)

    jt_cliques = list(nx.algorithms.clique.find_cliques(G))

    # create new graph
    G = nx.Graph()
    for i in range(len(jt_cliques)):
        G.add_node(i)
    
    for i in range(len(jt_cliques)):
        for j in range(i + 1, len(jt_cliques)):
            weight = len(set(jt_cliques[i]) & set(jt_cliques[j]))
            if weight > 0:
                G.add_edge(i, j, weight=weight)

    for edge in nx.algorithms.tree.mst.maximum_spanning_edges(G):
        jt_edges += [[edge[0], edge[1]]]

    """ END YOUR CODE HERE """
    #print("_get_jt_clique_and_edges return", jt_cliques, jt_edges)
    #show_graph(G)

    return jt_cliques, np.array(jt_edges)


def construct_junction_tree(nodes, edges, factors):
    """
    Constructs the junction tree and returns its the cliques, edges and clique factors in the junction tree.
    DO NOT EDIT THIS FUNCTION.

    Args:
        nodes: numpy array of random variables e.g. [X1, X2, ..., Xv]
        edges: numpy array of edges e.g. [[X1,X2], [X2,X1], ...]
        factors: list of factors in the graph

    Returns:
        list of cliques e.g. [[X1, X2], ...]
        numpy array of edges e.g. [[0,1], ...], [i,j] means that cliques[i] and cliques[j] are neighbors.
        list of clique factors where jt_cliques[i] has factor jt_factors[i] where i is an index
    """
    jt_cliques, jt_edges = _get_jt_clique_and_edges(nodes=nodes, edges=edges)
    jt_factors = _get_clique_factors(jt_cliques=jt_cliques, factors=factors)
    return jt_cliques, jt_edges, jt_factors
