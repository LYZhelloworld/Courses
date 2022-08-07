""" CS5340 Lab 1: Belief Propagation and Maximal Probability
See accompanying PDF for instructions.
"""

import copy
from typing import List

import numpy as np

from factor import Factor, index_to_assignment, assignment_to_index, generate_graph_from_factors, \
    visualize_graph

from functools import reduce


"""For sum product message passing"""
def factor_product(A, B):
    """Compute product of two factors.

    Suppose A = phi(X_1, X_2), B = phi(X_2, X_3), the function should return
    phi(X_1, X_2, X_3)
    """
    if A.is_empty():
        return B
    if B.is_empty():
        return A

    # Create output factor. Variables should be the union between of the
    # variables contained in the two input factors
    out = Factor()
    out.var = np.union1d(A.var, B.var)

    # Compute mapping between the variable ordering between the two factors
    # and the output to set the cardinality
    out.card = np.zeros(len(out.var), np.int64)
    mapA = np.argmax(out.var[None, :] == A.var[:, None], axis=-1)
    mapB = np.argmax(out.var[None, :] == B.var[:, None], axis=-1)
    out.card[mapA] = A.card
    out.card[mapB] = B.card

    # For each assignment in the output, compute which row of the input factors
    # it comes from
    out.val = np.zeros(np.prod(out.card))
    assignments = out.get_all_assignments()
    idxA = assignment_to_index(assignments[:, mapA], A.card)
    idxB = assignment_to_index(assignments[:, mapB], B.card)

    """ YOUR CODE HERE
    You should populate the .val field with the factor product
    Hint: The code for this function should be very short (~1 line). Try to
      understand what the above lines are doing, in order to implement
      subsequent parts.
    """
    out.val = np.array([A.val[idxA[i]] * B.val[idxB[i]] for i in range(len(out.val))])
    return out


def factor_marginalize(factor, var):
    """Sums over a list of variables.

    Args:
        factor (Factor): Input factor
        var (List): Variables to marginalize out

    Returns:
        out: Factor with variables in 'var' marginalized out.
    """
    out = Factor()

    """ YOUR CODE HERE
    Marginalize out the variables given in var
    """
    index_marginalized = np.where(np.isin(factor.var, var))
    index_keep = np.where(np.isin(factor.var, var, invert=True))
    out.var = np.delete(factor.var, index_marginalized)
    out.card = np.delete(factor.card, index_marginalized)
    
    out.val = np.zeros(np.prod(out.card))
    for assignment in factor.get_all_assignments():
        # assignment_out contains the assignment with the variables to be marginalized removed
        assignment_out = np.delete(assignment, index_marginalized)
        # add the probability to out.val, where the sum is stored
        out.val[assignment_to_index(assignment_out, out.card)] += factor.val[assignment_to_index(assignment, factor.card)]

    return out


def observe_evidence(factors, evidence=None):
    """Modify a set of factors given some evidence

    Args:
        factors (List[Factor]): List of input factors
        evidence (Dict): Dictionary, where the keys are the observed variables
          and the values are the observed values.

    Returns:
        List of factors after observing evidence
    """
    if evidence is None:
        return factors
    out = copy.deepcopy(factors)

    """ YOUR CODE HERE
    Set the probabilities of assignments which are inconsistent with the 
    evidence to zero.
    """
    for factor in out:
        for assignment in factor.get_all_assignments():
            if any([assignment[np.where(factor.var == key)] != evidence[key] for key in evidence]):
                factor.val[assignment_to_index(assignment, factor.card)] = 0

    return out


"""For max sum meessage passing (for MAP)"""
def factor_sum(A, B):
    """Same as factor_product, but sums instead of multiplies
    """
    if A.is_empty():
        return B
    if B.is_empty():
        return A

    # Create output factor. Variables should be the union between of the
    # variables contained in the two input factors
    out = Factor()
    out.var = np.union1d(A.var, B.var)

    # Compute mapping between the variable ordering between the two factors
    # and the output to set the cardinality
    out.card = np.zeros(len(out.var), np.int64)
    mapA = np.argmax(out.var[None, :] == A.var[:, None], axis=-1)
    mapB = np.argmax(out.var[None, :] == B.var[:, None], axis=-1)
    out.card[mapA] = A.card
    out.card[mapB] = B.card

    # For each assignment in the output, compute which row of the input factors
    # it comes from
    out.val = np.zeros(np.prod(out.card))
    assignments = out.get_all_assignments()
    idxA = assignment_to_index(assignments[:, mapA], A.card)
    idxB = assignment_to_index(assignments[:, mapB], B.card)

    """ YOUR CODE HERE
    You should populate the .val field with the factor sum. The code for this
    should be very similar to the factor_product().
    """
    out.val = np.array([A.val[idxA[i]] + B.val[idxB[i]] for i in range(len(out.val))])

    if A.val_argmax is None:
        A.val_argmax = [{}] * np.prod(A.card)
    if B.val_argmax is None:
        B.val_argmax = [{}] * np.prod(B.card)
    
    out.val_argmax = np.array([
        {**A.val_argmax[idxA[i]],
            **B.val_argmax[idxB[i]]
        } for i in range(len(out.val))
    ])
    if all(out.val_argmax == {}):
        out.val_argmax = None # for test_factor_sum()

    return out


def factor_max_marginalize(factor, var):
    """Marginalize over a list of variables by taking the max.

    Args:
        factor (Factor): Input factor
        var (List): Variable to marginalize out.

    Returns:
        out: Factor with variables in 'var' marginalized out. The factor's
          .val_argmax field should be a list of dictionary that keep track
          of the maximizing values of the marginalized variables.
          e.g. when out.val_argmax[i][j] = k, this means that
            when assignments of out is index_to_assignment[i],
            variable j has a maximizing value of k.
          See test_lab1.py::test_factor_max_marginalize() for an example.
    """
    out = Factor()

    """ YOUR CODE HERE
    Marginalize out the variables given in var. 
    You should make use of val_argmax to keep track of the location with the
    maximum probability.
    """
    index_marginalized = np.where(np.isin(factor.var, var))[0]
    index_keep = np.where(np.isin(factor.var, var, invert=True))[0]
    out.var = np.delete(factor.var, index_marginalized)
    out.card = np.delete(factor.card, index_marginalized)

    all_assignments = factor.get_all_assignments()
    
    out.val = np.full(np.prod(out.card), -np.inf)
    out.val_argmax = [{}] * (np.prod(out.card))
    for assignment in all_assignments:
        # assignment_out contains the assignment with the variables to be marginalized removed
        assignment_out = np.delete(assignment, index_marginalized)
        # update the probability to out.val, where the sum is stored
        index_new = assignment_to_index(assignment_out, out.card)
        index_old = assignment_to_index(assignment, factor.card)
        new = factor.val[index_old]
        old = out.val[index_new]
        if new > old:
            out.val[assignment_to_index(assignment_out, out.card)] = new
            out.val_argmax[index_new] = {factor.var[i]:assignment[i] for i in range(len(assignment)) if i not in index_keep}
            if factor.val_argmax is not None:
                out.val_argmax[index_new].update(factor.val_argmax[index_old])
                #print(out.val_argmax)

        #out.val[assignment_to_index(assignment_out, out.card)] += factor.val[assignment_to_index(assignment, factor.card)]
    #print(out)
    #print(out.val_argmax)
    return out


def compute_joint_distribution(factors):
    """Computes the joint distribution defined by a list of given factors

    Args:
        factors (List[Factor]): List of factors

    Returns:
        Factor containing the joint distribution of the input factor list
    """
    #joint = Factor()

    """ YOUR CODE HERE
    Compute the joint distribution from the list of factors. You may assume
    that the input factors are valid so no input checking is required.
    """
    # simply multiply all factors
    return reduce(factor_product, factors)


def compute_marginals_naive(V, factors, evidence):
    """Computes the marginal over a set of given variables

    Args:
        V (int): Single Variable to perform inference on
        factors (List[Factor]): List of factors representing the graphical model
        evidence (Dict): Observed evidence. evidence[k] = v indicates that
          variable k has the value v.

    Returns:
        Factor representing the marginals
    """

    #output = Factor()

    """ YOUR CODE HERE
    Compute the marginal. Output should be a factor.
    Remember to normalize the probabilities!
    """
    joint = compute_joint_distribution(factors)
    observed = observe_evidence([joint], evidence)[0]
    #print(observed)
    var_to_marginalize = np.delete(observed.var, np.where(observed.var == V))
    output = factor_marginalize(observed, var_to_marginalize)
    #print(output)
    
    # the output is almost correct, but the sum of probabilities is not 1.0
    # due to the evidence observation after computing joint distribution
    # normalize it to get the final result
    output.val = output.val / np.sum(output.val)
    #print(output)
    return output


def compute_marginals_bp(V, factors, evidence):
    """Compute single node marginals for multiple variables
    using sum-product belief propagation algorithm

    Args:
        V (List): Variables to infer single node marginals for
        factors (List[Factor]): List of factors representing the grpahical model
        evidence (Dict): Observed evidence. evidence[k]=v denotes that the
          variable k is assigned to value v.

    Returns:
        marginals: List of factors. The ordering of the factors should follow
          that of V, i.e. marginals[i] should be the factor for variable V[i].
    """
    # Dummy outputs, you should overwrite this with the correct factors
    marginals = []

    # Setting up messages which will be passed
    factors = observe_evidence(factors, evidence)
    graph = generate_graph_from_factors(factors)

    # Uncomment the following line to visualize the graph. Note that we create
    # an undirected graph regardless of the input graph since 1) this
    # facilitates graph traversal, and 2) the algorithm for undirected and
    # directed graphs is essentially the same for tree-like graphs.
    #visualize_graph(graph)

    # You can use any node as the root since the graph is a tree. For simplicity
    # we always use node 0 for this assignment.
    #root = 0
    root = [factor.var[0] for factor in factors if len(factor.var) == 1][0]

    # Create structure to hold messages
    num_nodes = graph.number_of_nodes()
    messages = [[None] * num_nodes for _ in range(num_nodes)]
    # we assume that messages[a][b] means message from a to b

    """ YOUR CODE HERE
    Use the algorithm from lecture 4 and perform message passing over the entire
    graph. Recall the message passing protocol, that a node can only send a
    message to a neighboring node only when it has received messages from all
    its other neighbors.
    Since the provided graphical model is a tree, we can use a two-phase 
    approach. First we send messages inward from leaves towards the root.
    After this is done, we can send messages from the root node outward.
    
    Hint: You might find it useful to add auxilliary functions. You may add 
      them as either inner (nested) or external functions.
    """
    def generate_message(a, b):
        if messages[a][b] is not None:
            return

        children = [i for i in graph.neighbors(a) if i != b] # childrens of a
        for child in children:
            generate_message(child, a)
        joint_factors = [graph.edges[a, b]['factor']] + [messages[child][a] for child in children]
        # unary factor is needed for message going out from the root
        # but message coming in does not need it
        if a == root:
            joint_factors += [graph.nodes[root]['factor']]
        #print(joint_factors)
        children += [a] # Now marginalize all children including the sender
        messages[a][b] = factor_marginalize(compute_joint_distribution(joint_factors), children)
    
    # generate messages
    for node in graph.nodes:
        for child in graph.neighbors(node):
            generate_message(child, node)
            generate_message(node, child)

    #for a in range(len(messages)):
        #for b in range(len(messages[a])):
            #print(a, b, messages[a][b])

    for var in V:
        children = list(graph.neighbors(var))
        joint_factors = [messages[child][var] for child in children]
        #joint_factors += [graph.nodes[root]['factor']]

        #if var == root or var in graph.neighbors(root):
            #joint_factors += [graph.nodes[root]['factor']]
        
        # When calculating probabilities of root, the unary factor should be included
        if var == root:
            joint_factors += [graph.nodes[root]['factor']]
        
        joint = compute_joint_distribution(joint_factors)
        var_to_marginalize = np.delete(joint.var, np.where(joint.var == var))
        
        result = factor_marginalize(joint, var_to_marginalize)
        result.val /= np.sum(result.val)
        marginals += [result]

    #print(marginals)
    return marginals


def map_eliminate(factors, evidence):
    """Obtains the maximum a posteriori configuration for a tree graph
    given optional evidence

    Args:
        factors (List[Factor]): List of factors representing the graphical model
        evidence (Dict): Observed evidence. evidence[k]=v denotes that the
          variable k is assigned to value v.

    Returns:
        max_decoding (Dict): MAP configuration
        log_prob_max: Log probability of MAP configuration. Note that this is
          log p(MAP, e) instead of p(MAP|e), i.e. it is the unnormalized
          representation of the conditional probability.
    """

    max_decoding = {}
    log_prob_max = 0.0

    """ YOUR CODE HERE
    Use the algorithm from lecture 5 and perform message passing over the entire
    graph to obtain the MAP configuration. Again, recall the message passing 
    protocol.
    Your code should be similar to compute_marginals_bp().
    To avoid underflow, first transform the factors in the probabilities
    to **log scale** and perform all operations on log scale instead.
    You may ignore the warning for taking log of zero, that is the desired
    behavior.
    """

    # Dummy outputs, you should overwrite this with the correct factors
    #marginals = []

    # Setting up messages which will be passed
    factors = observe_evidence(factors, evidence)
    graph = generate_graph_from_factors(factors)

    # Uncomment the following line to visualize the graph. Note that we create
    # an undirected graph regardless of the input graph since 1) this
    # facilitates graph traversal, and 2) the algorithm for undirected and
    # directed graphs is essentially the same for tree-like graphs.
    #visualize_graph(graph)

    # You can use any node as the root since the graph is a tree. For simplicity
    # we always use node 0 for this assignment.
    #root = 0
    root = [factor.var[0] for factor in factors if len(factor.var) == 1][0]

    # Create structure to hold messages
    num_nodes = graph.number_of_nodes()
    messages = [[None] * num_nodes for _ in range(num_nodes)]
    # we assume that messages[a][b] means message from a to b

    def log(factor):
        return Factor(factor.var, factor.card, np.log(factor.val), factor.val_argmax)

    def compute_factor_sum(factors):
        return reduce(factor_sum, factors)

    def generate_message(a, b):
        if messages[a][b] is not None:
            return

        children = [i for i in graph.neighbors(a) if i != b] # childrens of a
        for child in children:
            generate_message(child, a)
        joint_factors = [log(graph.edges[a, b]['factor'])] + [messages[child][a] for child in children]
        # unary factor is needed for message going out from the root
        # but message coming in does not need it
        if a == root:
            joint_factors += [log(graph.nodes[root]['factor'])]
        #print('joint_factors', joint_factors)
        children += [a] # Now marginalize all children including the sender
        messages[a][b] = factor_max_marginalize(compute_factor_sum(joint_factors), children)
    
    # generate messages
    for node in graph.nodes:
        for child in graph.neighbors(node):
            generate_message(child, node)
            generate_message(node, child)

    var = root
    children = list(graph.neighbors(var))
    joint_factors = [messages[child][var] for child in children]
    
    # When calculating probabilities of root, the unary factor should be included
    joint_factors += [log(graph.nodes[root]['factor'])]
    
    joint = compute_factor_sum(joint_factors)
    var_to_marginalize = np.delete(joint.var, np.where(joint.var == var))
    
    result = factor_max_marginalize(joint, var_to_marginalize)
    #result.val /= np.sum(result.val)

    max_arg = np.argmax(result.val)
    #print(result.val_argmax[max_arg])
    #max_decoding = {k: v for k, v in result.val_argmax[max_arg].items()}
    max_decoding = result.val_argmax[max_arg]
    log_prob_max = result.val[max_arg]
    #print(max_decoding)

    # add max arg of root node
    max_decoding[var] = max_arg
    # remove evidence key
    for e in evidence:
        if e in max_decoding:
            del max_decoding[e]

    #print(log_prob_max, max_decoding, result)
    return max_decoding, log_prob_max
