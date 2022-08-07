""" CS5340 Lab 2 Part 1: Junction Tree Algorithm
See accompanying PDF for instructions.
"""

import os
import numpy as np
import json
import networkx as nx
from argparse import ArgumentParser

from factor import Factor
from jt_construction import construct_junction_tree
from factor_utils import factor_product, factor_evidence, factor_marginalize

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'inputs')  # we will store the input data files here!
PREDICTION_DIR = os.path.join(DATA_DIR, 'predictions')  # we will store the prediction files here!


""" ADD HELPER FUNCTIONS HERE """
from functools import reduce

def get_message(messages, G, jt_factors, a, b):
    if messages[a][b] is not None:
        return messages[a][b]

    children = [i for i in G.neighbors(a) if i != b]
    joint_factors = [get_message(messages, G, jt_factors, child, a) for child in children]
    joint_factors.append(jt_factors[a])
    prod = reduce(factor_product, joint_factors)
    #print("get_message prod", prod)
    args_to_be_marginalized = list(set(jt_factors[a].var) - (set(jt_factors[a].var) & set(jt_factors[b].var)))
    #print("get_message args_to_be_marginalized", args_to_be_marginalized)
    messages[a][b] = factor_marginalize(prod, args_to_be_marginalized)
    #print("get_message messages[a][b]", messages[a][b])
    return messages[a][b]

""" END HELPER FUNCTIONS HERE """


def _update_mrf_w_evidence(all_nodes, evidence, edges, factors):
    """
    Update the MRF graph structure from observing the evidence

    Args:
        all_nodes: numpy array of nodes in the MRF
        evidence: dictionary of node:observation pairs where evidence[x1] returns the observed value of x1
        edges: numpy array of edges in the MRF
        factors: list of Factors in teh MRF

    Returns:
        numpy array of query nodes
        numpy array of updated edges (after observing evidence)
        list of Factors (after observing evidence; empty factors should be removed)
    """

    query_nodes = all_nodes
    updated_edges = edges
    updated_factors = factors
    #print("_update_mrf_w_evidence", all_nodes, evidence, edges, factors)
    """ YOUR CODE HERE """
    updated_factors = [factor_evidence(i, evidence) for i in updated_factors]
    for e in evidence:
        updated_edges = [i for i in edges if i[0] != e and i[1] != e]
        query_nodes = [i for i in all_nodes if i != e]

    # check empty factors
    updated_factors = [i for i in updated_factors if not i.is_empty()]
    non_existing_nodes = [node for node in query_nodes if not any([node in i.var for i in updated_factors])]
    query_nodes = [i for i in query_nodes if i not in non_existing_nodes]
    updated_edges = [i for i in updated_edges if i[0] not in non_existing_nodes and i[1] not in non_existing_nodes]
    """ END YOUR CODE HERE """
    #print("_update_mrf_w_evidence return", query_nodes, updated_edges, updated_factors)
    return query_nodes, updated_edges, updated_factors


def _get_clique_potentials(jt_cliques, jt_edges, jt_clique_factors):
    """
    Returns the list of clique potentials after performing the sum-product algorithm on the junction tree

    Args:
        jt_cliques: list of junction tree nodes e.g. [[x1, x2], ...]
        jt_edges: numpy array of junction tree edges e.g. [i,j] implies that jt_cliques[i] and jt_cliques[j] are
                neighbors
        jt_clique_factors: list of clique factors where jt_clique_factors[i] is the factor for cliques[i]

    Returns:
        list of clique potentials computed from the sum-product algorithm
    """
    #print("_get_clique_potentials", jt_cliques, jt_edges, jt_clique_factors)
    clique_potentials = [None] * len(jt_cliques)

    """ YOUR CODE HERE """
    num_nodes = len(jt_cliques)
    messages = [[None] * num_nodes for _ in range(num_nodes)] # messages[a][b] = message from a to b

    G = nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)
    for edge in jt_edges:
        G.add_edge(edge[0], edge[1])
    
    for i in range(num_nodes):
        # loop over every clique
        children = G.neighbors(i)
        clique_potentials[i] = reduce(factor_product, [get_message(messages, G, jt_clique_factors, child, i) for child in children] + [jt_clique_factors[i]])

    """ END YOUR CODE HERE """

    assert len(clique_potentials) == len(jt_cliques)
    #print("_get_clique_potentials return", clique_potentials)
    return clique_potentials


def _get_node_marginal_probabilities(query_nodes, cliques, clique_potentials):
    """
    Returns the marginal probability for each query node from the clique potentials.

    Args:
        query_nodes: numpy array of query nodes e.g. [x1, x2, ..., xN]
        cliques: list of cliques e.g. [[x1, x2], ... [x2, x3, .., xN]]
        clique_potentials: list of clique potentials (Factor class)

    Returns:
        list of node marginal probabilities (Factor class)

    """
    #print("_get_node_marginal_probabilities", query_nodes, cliques, clique_potentials)
    query_marginal_probabilities = [Factor() for _ in query_nodes]

    """ YOUR CODE HERE """
    assert len(cliques) == len(clique_potentials)
    for i in range(len(clique_potentials)):
        clique = cliques[i]
        clique_potential = clique_potentials[i]
        for var in clique:
            p = Factor(var=clique_potential.var, card=clique_potential.card, val=clique_potential.val)
            p.val = p.val / np.sum(p.val) # normalize
            query_marginal_probabilities[list(query_nodes).index(var)] = factor_marginalize(p, list(set(p.var) - set([var])))

    """ END YOUR CODE HERE """

    return query_marginal_probabilities


def get_conditional_probabilities(all_nodes, evidence, edges, factors):
    """
    Returns query nodes and query Factors representing the conditional probability of each query node
    given the evidence e.g. p(xf|Xe) where xf is a single query node and Xe is the set of evidence nodes.

    Args:
        all_nodes: numpy array of all nodes (random variables) in the graph
        evidence: dictionary of node:evidence pairs e.g. evidence[x1] returns the observed value for x1
        edges: numpy array of all edges in the graph e.g. [[x1, x2],...] implies that x1 is a neighbor of x2
        factors: list of factors in the MRF.

    Returns:
        numpy array of query nodes
        list of Factor
    """
    query_nodes, updated_edges, updated_node_factors = _update_mrf_w_evidence(all_nodes=all_nodes, evidence=evidence,
                                                                              edges=edges, factors=factors)

    jt_cliques, jt_edges, jt_factors = construct_junction_tree(nodes=query_nodes, edges=updated_edges,
                                                               factors=updated_node_factors)

    clique_potentials = _get_clique_potentials(jt_cliques=jt_cliques, jt_edges=jt_edges, jt_clique_factors=jt_factors)

    query_node_marginals = _get_node_marginal_probabilities(query_nodes=query_nodes, cliques=jt_cliques,
                                                            clique_potentials=clique_potentials)

    return query_nodes, query_node_marginals


def parse_input_file(input_file: str):
    """ Reads the input file and parses it. DO NOT EDIT THIS FUNCTION. """
    with open(input_file, 'r') as f:
        input_config = json.load(f)

    nodes = np.array(input_config['nodes'])
    edges = np.array(input_config['edges'])

    # parse evidence
    raw_evidence = input_config['evidence']
    evidence = {}
    for k, v in raw_evidence.items():
        evidence[int(k)] = v

    # parse factors
    raw_factors = input_config['factors']
    factors = []
    for raw_factor in raw_factors:
        factor = Factor(var=np.array(raw_factor['var']), card=np.array(raw_factor['card']),
                        val=np.array(raw_factor['val']))
        factors.append(factor)
    return nodes, edges, evidence, factors


def main():
    """ Entry function to handle loading inputs and saving outputs. DO NOT EDIT THIS FUNCTION. """
    argparser = ArgumentParser()
    argparser.add_argument('--case', type=int, required=True,
                           help='case number to create observations e.g. 1 if 1.json')
    args = argparser.parse_args()

    case = args.case
    input_file = os.path.join(INPUT_DIR, '{}.json'.format(case))
    nodes, edges, evidence, factors = parse_input_file(input_file=input_file)

    # solution part:
    query_nodes, query_conditional_probabilities = get_conditional_probabilities(all_nodes=nodes, edges=edges,
                                                                                 factors=factors, evidence=evidence)
    #print(query_nodes, query_conditional_probabilities)

    predictions = {}
    for i, node in enumerate(query_nodes):
        probability = query_conditional_probabilities[i].val
        predictions[int(node)] = list(np.array(probability, dtype=float))

    if not os.path.exists(PREDICTION_DIR):
        os.makedirs(PREDICTION_DIR)
    prediction_file = os.path.join(PREDICTION_DIR, '{}.json'.format(case))
    with open(prediction_file, 'w') as f:
        json.dump(predictions, f, indent=1)
    print('INFO: Results for test case {} are stored in {}'.format(case, prediction_file))


if __name__ == '__main__':
    main()
