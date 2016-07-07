import pdb
import operator
import numpy as np
from itertools import product
def mul(seq):
    return reduce(operator.mul, seq, 1)

print 'Use to for implementing parameter estimation'

class Potential:
    # variables: list of strings naming the variables
    # pot: dictionary mapping tuples of variable values to potential value
    def __init__(self, variables, pot):
        self.vars = variables
        self.indices = dict(zip(variables, range(len(variables))))
        self.pot = pot

    def __str__(self):
        return 'Potential('+str(self.vars)+','+str(self.pot)+')'
    __repr__ = __str__

    # vt is a tuple of values; return the associated potential value
    # return 0 if vt is not explicitly represented in self.pot
    def valTuple(self, vt):
        return self.pot[vt] if vt in self.pot else 0.0

    # vt is a tuple of values; increment an entry in self.ppt
    def incValTuple(self, vt, inc=1):
        self.pot[vt] = self.pot[vt]+inc

    # Return a list of all elements that have weight > 0 in this potential
    def support(self):
        return [k for (k, v) in self.pot.items() if v > 0]

    # assign is a dictionary mapping variable names to values; return
    # the associated potential value.
    def val(self, assign):
        return self.valTuple(tuple([assign[var] for var in self.vars]))

    # Product of two instances of Potential is a new Potential defined
    # on the union of the variables of self and other
    # LPK:  make a better implementation!?
    def mul(self, other):
        # Three sets of vars: only in self, in both, only in other
        selfOnly = set(self.vars).difference(set(other.vars))
        otherOnly = list(set(other.vars).difference(set(self.vars)))
        both = set(self.vars).intersection(set(other.vars))
        # keep whole tuple from self; add some indices from other
        otherIndices = [other.indices[v] for v in otherOnly]
        newPot = {}
        for e1 in self.support():
            for e2 in other.support():
                if self.agrees(other, e1, e2, both):
                    newElt = tuple(list(e1) + [e2[i] for i in otherIndices])
                    newPot[newElt] = self.valTuple(e1) * other.valTuple(e2)
        return Potential(self.vars + otherOnly, newPot)


    # vs is a list of variable names
    # Assume: tuple1 is an assignment of the variables in self, tuple
    # 2 is an assignment of variables in other.  Return True if they
    # agree on the values of the variables in vs
    def agrees(self, other, tuple1, tuple2, vs):
        for v in vs:
            if tuple1[self.indices[v]] != tuple2[other.indices[v]]:
                return False
        return True

    # cVars is a list of variable names
    # cVals is a list of the same length of values for those variables
    # Treat self as a joint probability distribution, and this as the
    # operation of conditioning on the event cVars = cVals
    # - select out entries for which cVars = cVals
    # - remove cVars from the potential
    # - sum potential values if there are duplicate entries
    # - renormalize to obtain a distribution
    # Returns a new instance of Potential defined on previous vars minus cVars
    def condition(self, cVars, cVals):
        newPot = {}
        indices = [self.indices[v] for v in cVars]
        for e in self.support():
            if all(e[i] == v for (i, v) in zip(indices, cVals)):
                newPot[removeIndices(e, indices)] = self.pot[e]
        return Potential(removeIndices(self.vars, indices), newPot).normalize()

    # qVars is a list of variable names
    # Sum out all other variables, returning a new potential on qVars
    def marginalize(self, qVars):
        newPot = {}
        indices = removeVals(range(len(self.vars)),
                             [self.indices[v] for v in qVars])
        for e in self.support():
            newE = removeIndices(e, indices)
            addToEntry(newPot, newE, self.valTuple(e))
        return Potential(qVars, newPot)

    # Divide through by sum of values; returns a new Potential on the
    # same variables with potential values that sum to 1 over the
    # whole domain.
    def normalize(self):
        total = sum(self.pot.values())
        newPot = dict([(v, p/total) for (v, p) in self.pot.items()])
        return Potential(self.vars, newPot)

    # For each value of the rest of the indices, normalize the values
    # over the first index.
    def cpdNormalize(self):
        totals = {}
        for e in self.support():
            addToEntry(totals, e[1:], self.pot[e])
        for e in self.support():
            self.pot[e] /= float(totals[e[1:]])
            
# Useful as the multiplicitive identity:  p.mul(iPot) = p 
iPot = Potential([], {tuple() : 1.0})

# Make a potential that assigns every possible element (give
# domains of each of the variables) to value c
def makeConstant(vars, domains, c):
    return Potential(vars,
                     dict([(e, c) for e in product(*domains)]))

# Assign probability 1 to a single value.  Val should be a tuple of
# the same length as variables
class DeltaPotential(Potential):
    def __init__(self, variables, val):
        self.vars = variables
        self.val = val
        self.indices = dict(zip(variables, range(len(variables))))
        
    def __str__(self):
        return 'Potential('+str(self.vars)+','+str(self.val)+': 1.0)'

    # vt is a tuple of values; return the associated potential value
    def valTuple(self, vt):
        return 1.0 if vt == self.val else 0.0

    def support(self):
        return [self.val]

# Convenient abbreviation
P = Potential

######################################################################
# Bayesian networks
######################################################################

class BNNode:
    # name is a string naming the variable
    # parents is a list of strings naming parent variables
    # cpd is an instance of Potential, defined on variables [name] + parents
    # It needs to be a well-formed conditional probability
    # distribution, so that for each value v of name,
    # sum_{v} cpd([v] + values of parents) = 1
    # domain is the list of possible values for this node; supply it
    # if cpd is not supplied
    def __init__(self, name, parents, cpd = None, domain = None):
        self.name = name
        self.parents = parents
        self.cpd = cpd
        self.domain = domain

class BN:
    # bn is a dictionary
    # key: string
    # value: (list of strings, Potential on varName and parents)
    def __init__(self, nodes):
        self.vars = [n.name for n in nodes]
        # LPK: Check to be sure all parents are in network
        self.nodes = nodes
        # Map a var name to its index into the list of vars
        self.indices = dict([(self.vars[i], i) for i in range(len(self.vars))])
        # Keep the list of domains around
        self.domains = [n.domain for n in self.nodes]

    # assign is a dictionary from variable names to values, with an
    # entry for every variable in the network
    # Returns probability of that assignment
    def prob(self, assign):
        return mul([n.cpd.val(assign) for n in self.nodes])

    # Prob, but with tuple as argument
    def probT(self, tupl):
        return self.prob(dict(zip(self.vars, tupl)))
    
    # Create a joint probability distribution
    # Returns a potential reprsenting the joint distribution, defined
    # over all the variables in the network
    def joint(self):
        j = reduce(Potential.mul, [n.cpd for n in self.nodes], iPot)
        assert 1-1e-8 < sum(j.pot.values()) < 1 + 1e-8
        return j

    # queryVars is a list of variable names
    # eVars is a list of variable names
    # eValues is a list of values, one for each of eVars
    # Returns a joint distribution on the query variables representing
    # P(queryVars | eVars = eValues)
    # This is slow:  works by constructing the joint distribution,
    # then conditioning and then marginalizing.
    def query(self, queryVars, eVars = [], eValues = []):
        return self.joint().condition(eVars, eValues).marginalize(queryVars)

    # Construct an instance of FactorGraph representing this same
    # distribution.  One variable and one factor for each node in the
    # Bayes Net
    def factorGraph(self):
        # Make the nodes
        factorNodes = [FactorNode(n.cpd) for n in self.nodes]
        varNodes = [VarNode(n.name) for n in self.nodes]
        return FactorGraph(factorNodes, varNodes)

    # Will replace the potentials in this object (which need not be
    # defined) data is a list of data lists, each data list is length
    # D, where D is the number of variables in bn indexed in the same
    # order as self.vars If laplace = True, then use the "Laplace
    # correction" for the ML estimator.
    def estimateParams(self, data, laplace = False):
        # your code here
        for n in self.nodes:
            nodeNames = [n.name] + n.parents
            indices = [self.indices[name] for name in nodeNames]
            domains = [self.nodes[i].domain for i in indices]

            # make empty potential
            pot = makeConstant(nodeNames, domains, 1 if laplace else 0)

            # go through the data and increment counts in the pot
            for d in data:
                pot.incValTuple(tuple([d[i] for i in indices]))

            # normalize to get a conditional prob distribution
            pot.cpdNormalize()
            n.cpd = pot


    # Assume some missing data.  Indicated by a None in the data set.
    # Will do EM iterations until change in log likelihood is < epsilon
    def estimateParamsEM(self, partial_data, laplace = True,
                         epsilon = .0001):
        # Use this completed data to initialize the parameters
        completedData = completeDataRandomly(partial_data, self.domains)
        # your code here
        pass

    def completeData(self, data):
        # your code here
        pass
        
    # Compute the log likelihood.  Data may be partial.
    def logLikelihood(self, data):
        return sum([np.log(sum([self.probT(r) \
                                for r in allRowCompletions(row, self.domains)])) \
                    for row in data])

######################################################################
# Factor graphs
######################################################################

class FactorGraph:
    # factorNodes: a list of  instances of class FactorNode
    # varNodes: a list of  instances of class VarNode
    def __init__(self, factorNodes, varNodes):
        self.factorNodes = factorNodes
        self.varNodes = varNodes
        # Make var nodes point to their factors and factors point to
        # their var nodes
        varNodeDict = dict([(n.name, n) for n in varNodes])
        for fn in factorNodes:
            for a in fn.potential.vars:
                varNodeDict[a].addNeighbor(fn.name, fn)
                fn.addNeighbor(a, varNodeDict[a])

class FactorGraphNode:
    def __init__(self, name):
        self.name = name
        # Dictionary from variable name to node; neighbors in factor graph
        self.neighborNodes = {}
        
    def addNeighbor(self, name, node):
        self.neighborNodes[name] = node

    # Return set of names of neighbor nodes
    def neighbors(self):
        return set(self.neighborNodes.keys())

class FactorNode(FactorGraphNode):
    idCounter = 0
    def __init__(self, pot):
        # Make uniqe id and use it as name
        FactorGraphNode.__init__(self, FactorNode.idCounter)
        FactorNode.idCounter += 1
        self.potential = pot

class VarNode(FactorGraphNode):
    pass

######################################################################


# xs is a tuple (or list) of items and indices is a list of indices
# returns a new tuple containing only those items whose indices are
#  not in the list
def removeIndices(xs, indices):
    return tuple([xs[i] for i in range(len(xs)) if not i in indices])

# xs is a tuple (or list) of items and vals is a list of values
# returns a new tuple containing only those items whose indices are
# not in the list.  Use this instead of set difference because we want
# maintain the order of the remaining xs
def removeVals(xs, vals):
    return tuple([x for x in xs if x not in vals])

# Assuming d is a dictionary mapping elements to numeric values
# Adds e to the dictionary if it is not already there
# Increments the value of e by v
def addToEntry(d, e, v):
    if not e in d: d[e] = 0
    d[e] += v


# Data is an N x D array or list of lists.  If a data item is missing, it
# will be indicated by a value of None.  Domains is a list of D lists,
# sets, or tuples, indicating the domain of each of the D variables.

# Returns a 'weighted' data set, which is N x (D + 1), where the last
# element is a weight for that data item.

# Any row that its complete (no missing data) will be copied over and
# given a weight of 1.
    
# For any row in data that contains missing k items, substitute
# a set of rows (number is the product of sizes of domains of missing
# items), and they will be given weights randomly assigned that sum to
# 1.   (Uniform weighting risks starting on an unstable local optimum.)

def completeDataRandomly(data, domains):
    result = []
    for row in data:
        result.extend(completeRowRandomly(row, domains))
    return result

# Fill in the None values in row, in order, with the values in comp
def fillIn(row, comp):
    result = []; i = 0
    for x in row:
        if x is None:
            result.append(comp[i])
            i += 1
        else:
            result.append(x)
    return result

def allRowCompletions(row, domains):
    indices = [i for (i, v) in enumerate(row) if v == None]
    if not indices:
        # No missing data!
        return [row]
    n = len(indices)
    idomains = [domains[i] for i in indices]
    return [fillIn(row, comp) for comp in product(*idomains)]

def completeRowRandomly(row, domains):
    completions = allRowCompletions(row, domains)
    weights = np.random.dirichlet([10]*len(completions))
    #weights = [1.0/len(completions)]*len(completions)
    return [comp + [w] for (comp, w) in zip(completions, weights)]


######################################################################
# Test cases for parameter estimation
######################################################################
        
# Test 0 for BN parameter estimation.
def test0():
    d = [[1, 1], [1, 1], [1, 0], [1, 1],
         [0, 0], [0, 0], [0, 1], [0, 1]]
    n = BN([BNNode('A', [], domain = (0, 1)),
            BNNode('B', ['A'], domain = (0, 1))])
    n.estimateParams(d)
    for v in n.vars:
        print n.query([v])
    return n

###############################
# Printer Nightmare
###############################

printerNightmare = BN([BNNode('Fuse', [], domain = (0, 1)),
                       BNNode('Drum', [], domain = (0, 1)),                  
                       BNNode('Toner', [], domain = (0, 1)),
                       BNNode('Paper', [], domain = (0, 1)),         
                       BNNode('Roller', [], domain = (0, 1)),              
                       BNNode('Burning', ['Fuse'], domain = (0, 1)),            
                       BNNode('Quality', ['Drum', 'Toner', 'Paper'],
                                 domain = (0, 1)), 
                       BNNode('Wrinkled', ['Fuse', 'Paper'], domain = (0, 1)),
                       BNNode('MultPages', ['Paper', 'Roller'], domain = (0,1)),
                       BNNode('PaperJam', ['Fuse', 'Roller'], domain = (0, 1))])

#          F  D  T  P  R  B  Q  W  M  J
pnData = [[0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
          [0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
          [0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
          [0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
          [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
          [1, 0, 0, 0, 1, 0, 0, 1, 1, 0]]

def test1(laplace = False):
    printerNightmare.estimateParams(pnData, laplace)
    return printerNightmare.query(['Fuse'],
                   ['Burning', 'Quality', 'Wrinkled', 'MultPages', 'PaperJam'],
                   [1, 0, 0, 0, 1])


###############################
# Naive Bayes implementation with spam data
###############################
    
def NBSpam(n_train = 200, n_test = 200, laplace = False, verbose = False):
    # Get data
    trainData, testData = getData(n_train, n_test)
    featureNames = ['make', 'address', 'all', '3d', 'our', 'over', 'remove',
            'internet', 'order', 'mail', 'receive', 'will', 'people',
            'report', 'addresses', 'free', 'business', 'email', 'you',
            'credit', 'your', 'font', '000', 'money', 'hp', 'hpl',
            'george', '650', 'lab', 'labs', 'telnet', '857', 'data',
            '415', '85', 'technology', '1999', 'parts', 'pm', 'direct',
            'cs', 'meeting', 'original', 'project', 're', 'edu', 'table',
            'conference', ';', '(', '[', '!', '$', '#', 'capitals']
    # Define the network structure of bn
    bn = None      # your code here

    # Train network
    bn.estimateParams(trainData, laplace)

    if verbose:
        print 'Probability of feature given not spam, and given spam'
        for n in bn.nodes[:-1]:
            print n.name, n.cpd.valTuple((1, 0)), n.cpd.valTuple((1, 1))

    # Given a new test case, return the most likely class
    def predictor(x):
        # your code here
        pass

    return errorRate(predictor, testData)

def errorRate(predictor, testData):
    n_test = len(testData)
    n_wrong = 0
    for d in testData:
        pred = predictor(d[:-1])
        true = d[-1]
        if pred != true: n_wrong += 1
    return n_wrong / float(n_test)

def getData(n_train, n_test):
    from spam import *
    allData = np.array(allData)
    # Mix up positive and negative examples
    np.random.shuffle(allData)
    trainData = allData[:n_train]
    testData = allData[n_train:n_train+n_test]
    return trainData, testData

######################################################################
# Test cases for parameter estimation with missing data (EM)
######################################################################

def test2():
    # Easy EM
    easyEMData = [[1, 1], [1, 1], [0, 0], [0, 0], [0, 0], [0, None],
              [0, 1], [1, 0]]
    bn = BN([BNNode('A', [], domain = (0, 1)),
             BNNode('B', ['A'], domain = (0, 1))])
    bn.estimateParamsEM(easyEMData, laplace = False)
    for n in bn.nodes:
        print n.cpd
    print bn.joint()


def test3():
    # Simple Clustering!
    data = \
    [[0, 1, 1, 1, 0, 0, 0, 1, None],
     [1, 1, 0, 1, 0, 1, 0, 0, None],
     [1, 0, 1, 1, 0, 0, 0, 0, None],
     [1, 1, 1, 1, 1, 0, 1, 0, None],
     [1, 0, 0, 1, 1, 0, 0, 0, None],
     [0, 1, 1, 1, 0, 0, 0, 0, None],
     [1, 1, 1, 0, 0, 0, 0, 0, None],
     [1, 1, 1, 1, 0, 0, 1, 0, None],
     [1, 1, 1, 1, 0, 0, 0, 1, None],
     [1, 1, 0, 1, 0, 1, 0, 0, None],
     [0, 1, 1, 0, 0, 0, 0, 0, None],
     [1, 0, 1, 1, 0, 0, 0, 0, None],
     
     [0, 0, 0, 0, 0, 1, 1, 1, None],
     [1, 0, 0, 0, 1, 1, 0, 1, None],
     [0, 1, 0, 0, 1, 1, 1, 0, None],
     [0, 0, 1, 0, 1, 0, 1, 1, None],
     [0, 0, 0, 1, 1, 1, 1, 1, None],
     [0, 0, 0, 0, 1, 1, 0, 1, None],
     [1, 0, 0, 0, 1, 1, 1, 1, None],
     [0, 0, 1, 0, 0, 1, 1, 1, None],
     [0, 1, 0, 0, 1, 1, 1, 1, None],
     [0, 0, 0, 1, 1, 1, 0, 1, None],
     [0, 0, 0, 0, 1, 1, 1, 0, None],
     [0, 0, 1, 0, 1, 0, 1, 1, None],

     [1, 0, 1, 0, 1, 0, 1, 0, None],
     [0, 0, 1, 1, 0, 0, 1, 1, None],
     [1, 1, 0, 0, 1, 1, 0, 0, None],
     [0, 1, 0, 1, 0, 1, 0, 1, None]]

    bn = BN([BNNode(w, ['Cluster'], domain = (0, 1)) \
                 for w in ['eigenvalue', 'matrix', 'bug', 'estimate',
                           'game', 'score', 'goal', 'lose']] + \
            [BNNode('Cluster', [], domain = (0, 1))])
    bn.estimateParamsEM(data, laplace = False, epsilon = 1e-10)
    for n in bn.nodes:
        print n.cpd

###############################
# EM based clustering with spam data
###############################

def test4(n = 200):
    # Given a new test case, return the most likely class
    trainData, _ = getData(n, 0)
    data = [d[:-1].tolist()+[None] for d in trainData]

    featureNames = ['make', 'address', 'all', '3d', 'our', 'over', 'remove',
            'internet', 'order', 'mail', 'receive', 'will', 'people',
            'report', 'addresses', 'free', 'business', 'email', 'you',
            'credit', 'your', 'font', '000', 'money', 'hp', 'hpl',
            'george', '650', 'lab', 'labs', 'telnet', '857', 'data',
            '415', '85', 'technology', '1999', 'parts', 'pm', 'direct',
            'cs', 'meeting', 'original', 'project', 're', 'edu', 'table',
            'conference', ';', '(', '[', '!', '$', '#', 'capitals']
    # Define the network structure
    leafNodes = [BNNode(v, ['class'], domain = (0, 1)) for v in featureNames]
    root = BNNode('class', [], domain = (0,1))
    # Take care that the nodes are in the same order as the features in data
    bn = BN(leafNodes + [root])

    bn.estimateParamsEM(data, laplace = False, epsilon = 1e-3, verbose=False)

    # Given a new test case, return the most likely class
    def predictor(x):
        # your code here
        pass
    # Predict the class (spam?) based on the learned parameters
    results = [(trainData[i][-1], predictor(x)) for i, x in enumerate(data)]
    # Calculate the error rate
    error = errorRateCluster(results)
    print 'error rate', error
    return error

def errorRateCluster(vals):
    n = float(len(vals))
    agree = sum(1 for (x,y) in vals if x==y)
    disagree = sum(1 for (x,y) in vals if x!=y)
    error = min(agree/n, disagree/n)
    print 'agreee', agree, 'disagree', disagree
    return error

print "Loaded gm.py"        
        
