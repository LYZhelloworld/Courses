""" CS5340 Lab 4 Part 2: Gibbs Sampling
See accompanying PDF for instructions.
"""


import copy
import os
import json
import numpy as np
from tqdm import tqdm
from collections import Counter
from argparse import ArgumentParser
from factor_utils import factor_evidence, factor_marginalize, assignment_to_index
from factor import Factor


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'inputs')
PREDICTION_DIR = os.path.join(DATA_DIR, 'predictions')
GROUND_TRUTH_DIR = os.path.join(DATA_DIR, 'ground-truth')

""" HELPER FUNCTIONS HERE """
from typing import Dict, Tuple, Set
from functools import reduce

def convert_sample(sample: Dict[int, int]) -> Tuple[Tuple[int, int], ...]:
    return tuple(sample.items())


def sample_to_index(sample: Tuple[Tuple[int, int], ...], var: np.ndarray, evidence: Dict[int, int], card: np.ndarray) -> int:
    result = [None] * len(var)
    for i in range(len(var)):
        v = var[i]
        if v in evidence.keys():
            result[i] = evidence[v]
            continue
        for s in sample:
            if s[0] == v:
                result[i] = s[1]
                continue
    assert None not in result
    return assignment_to_index(np.array(result), card)


def factor_product_no_val(A: Factor, B: Factor) -> Factor:
    if A.is_empty():
        return B
    if B.is_empty():
        return A

    out = Factor()

    # Set the variables of the output
    out.var = np.union1d(A.var, B.var)

    # Set the cardinality of the output
    out.card = np.zeros(len(out.var), np.int64)
    mapA = np.argmax(out.var[None, :] == A.var[:, None], axis=-1)
    mapB = np.argmax(out.var[None, :] == B.var[:, None], axis=-1)
    out.card[mapA] = A.card
    out.card[mapB] = B.card

    # Initialize the factor values to zero
    out.val = np.zeros(np.prod(out.card))
    return out


def reduce_distribution(nodes: np.ndarray, edges: np.ndarray, factors: Dict[int, Factor]) -> Dict[int, Factor]:
    def get_markov_blanket_nodes(node: int, edges: np.ndarray) -> Set[int]:
        blanket = {node}
        children = set()
        
        for edge in edges:
            # parents
            if edge[1] == node:
                blanket.add(edge[0])
            # children
            if edge[0] == node:
                blanket.add(edge[1])
                children.add(edge[1])
        for edge in edges:
            # co-parents
            if edge[1] in children:
                blanket.add(edge[0])
        return blanket
    
    result = {}
    for node in nodes:
        factor = factors[node]
        blanket = get_markov_blanket_nodes(node, edges)
        var_marginalized = factor.var[np.isin(factor.var, list(blanket), invert=True)]
        result[node] = factor_marginalize(factor, var_marginalized)

    return result


""" END HELPER FUNCTIONS HERE"""


def _sample_step(nodes: np.ndarray, factors: Dict[int, Factor], in_samples: Dict[int, int]) -> Dict[int, int]:
    """
    Performs gibbs sampling for a single iteration. Returns a sample for each node

    Args:
        nodes: numpy array of nodes
        factors: dictionary of factors e.g. factors[x1] returns the local factor for x1
        in_samples: dictionary of input samples (from previous iteration)

    Returns:
        dictionary of output samples where samples[x1] returns the sample for x1.
    """
    samples = copy.deepcopy(in_samples)

    """ YOUR CODE HERE """
    for node in nodes:
        factor = factors[node]
        new_sample = copy.deepcopy(samples)
        del new_sample[node]
        new_factor = factor_evidence(factor, new_sample)
        assert len(new_factor.var) == 1
        probs = new_factor.val / np.sum(new_factor.val)
        samples[node] = np.random.choice(new_factor.card[0], 1, p=probs)[0]

    """ END YOUR CODE HERE """
    return samples


def _get_conditional_probability(nodes: np.ndarray, edges: np.ndarray, factors: Dict[int, Factor], evidence: Dict[int, int], initial_samples: Dict[int, int], num_iterations: int, num_burn_in: int) -> Factor:
    """
    Returns the conditional probability p(Xf | Xe) where Xe is the set of observed nodes and Xf are the query nodes
    i.e. the unobserved nodes. The conditional probability is approximated using Gibbs sampling.

    Args:
        nodes: numpy array of nodes e.g. [x1, x2, ...].
        edges: numpy array of edges e.g. [i, j] implies that nodes[i] is the parent of nodes[j].
        factors: dictionary of Factors e.g. factors[x1] returns the conditional probability of x1 given all other nodes.
        evidence: dictionary of evidence e.g. evidence[x4] returns the provided evidence for x4.
        initial_samples: dictionary of initial samples to initialize Gibbs sampling.
        num_iterations: number of sampling iterations
        num_burn_in: number of burn-in iterations

    Returns:
        returns Factor of conditional probability.
    """
    assert num_iterations > num_burn_in
    conditional_prob = Factor()

    """ YOUR CODE HERE """
    factors = reduce_distribution(nodes, edges, factors)
    observed_factors = {key: factor_evidence(factor, evidence) for key, factor in factors.items()}
    observed_factors = {key: factor for key, factor in observed_factors.items() if key in factor.var}
    nodes = np.array([i for i in nodes if i not in evidence.keys()])
    counter = {}
    samples = initial_samples
    for _ in range(num_burn_in):
        samples = _sample_step(nodes, observed_factors, samples)
    for _ in range(num_iterations):
        samples = _sample_step(nodes, observed_factors, samples)
        key = convert_sample(samples)
        counter[key] = counter.get(key, 0) + 1
    
    conditional_prob = reduce(factor_product_no_val, observed_factors.values())
    for sample in counter:
        conditional_prob.val[sample_to_index(sample, conditional_prob.var, evidence, conditional_prob.card)] = counter.get(sample, 0)
    conditional_prob.val = conditional_prob.val / np.sum(conditional_prob.val)

    """ END YOUR CODE HERE """

    return conditional_prob


def load_input_file(input_file: str) -> (Factor, dict, dict, int):
    """
    Returns the target factor, proposal factors for each node and evidence. DO NOT EDIT THIS FUNCTION

    Args:
        input_file: input file to open

    Returns:
        Factor of the target factor which is the target joint distribution of all nodes in the Bayesian network
        dictionary of node:Factor pair where Factor is the proposal distribution to sample node observations. Other
                    nodes in the Factor are parent nodes of the node
        dictionary of node:val pair where node is an evidence node while val is the evidence for the node.
    """
    with open(input_file, 'r') as f:
        input_config = json.load(f)
    proposal_factors_dict = input_config['proposal-factors']

    def parse_factor_dict(factor_dict):
        var = np.array(factor_dict['var'])
        card = np.array(factor_dict['card'])
        val = np.array(factor_dict['val'])
        return Factor(var=var, card=card, val=val)

    nodes = np.array(input_config['nodes'], dtype=int)
    edges = np.array(input_config['edges'], dtype=int)
    node_factors = {int(node): parse_factor_dict(factor_dict=proposal_factor_dict) for
                    node, proposal_factor_dict in proposal_factors_dict.items()}

    evidence = {int(node): ev for node, ev in input_config['evidence'].items()}
    initial_samples = {int(node): initial for node, initial in input_config['initial-samples'].items()}

    num_iterations = input_config['num-iterations']
    num_burn_in = input_config['num-burn-in']
    return nodes, edges, node_factors, evidence, initial_samples, num_iterations, num_burn_in


def main():
    """
    Helper function to load the observations, call your parameter learning function and save your results.
    DO NOT EDIT THIS FUNCTION.
    """
    argparser = ArgumentParser()
    argparser.add_argument('--case', type=int, required=True,
                           help='case number to create observations e.g. 1 if 1.json')
    args = argparser.parse_args()
    # np.random.seed(0)

    case = args.case
    input_file = os.path.join(INPUT_DIR, '{}.json'.format(case))
    nodes, edges, node_factors, evidence, initial_samples, num_iterations, num_burn_in = \
        load_input_file(input_file=input_file)

    # solution part
    conditional_probability = _get_conditional_probability(nodes=nodes, edges=edges, factors=node_factors,
                                                           evidence=evidence, initial_samples=initial_samples,
                                                           num_iterations=num_iterations, num_burn_in=num_burn_in)
    print(conditional_probability)
    # end solution part

    # json only recognises floats, not np.float, so we need to cast the values into floats.
    save__dict = {
        'var': np.array(conditional_probability.var).astype(int).tolist(),
        'card': np.array(conditional_probability.card).astype(int).tolist(),
        'val': np.array(conditional_probability.val).astype(float).tolist()
    }

    if not os.path.exists(PREDICTION_DIR):
        os.makedirs(PREDICTION_DIR)
    prediction_file = os.path.join(PREDICTION_DIR, '{}.json'.format(case))

    with open(prediction_file, 'w') as f:
        json.dump(save__dict, f, indent=1)
    print('INFO: Results for test case {} are stored in {}'.format(case, prediction_file))


if __name__ == '__main__':
    main()
