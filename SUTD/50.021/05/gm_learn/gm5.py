import pdb
import math
import operator
import random
from itertools import product
def mul(seq):
    return reduce(operator.mul, seq, 1)

print 'Version for working on Markov Models.'

class Potential:
    # Make a potential that assigns every possible element (give
    # domains of each of the variables) to value c
    @staticmethod
    def makeConstant(vars, domains, c):
        return Potential(vars,
                         dict([(e, c) for e in product(*domains)]))

    # variables: list of strings naming the variables
    # pot: dictionary mapping tuples of variable values to potential value
    def __init__(self, variables, pot):
        n = len(variables)
        self.vars = variables
        self.indices = dict(zip(variables, range(n)))
        self.pot = pot
        for k in self.pot.keys():
            assert type(k) == tuple and len(k) == n

    def __str__(self):
        return 'Potential('+str(self.vars)+','+str(self.pot)+')'
    __repr__ = __str__

    # Make a copy but with new variable names
    def rename(self, varNames):
        return Potential(varNames, self.pot)

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

    # Assume it's normalized
    def sample(self):
        r = random.random()
        tp = 0
        for (k, p) in self.pot.items():
            tp += p
            if r <= tp: return k
        return None

    def cpdSample(self, cond):
        r = random.random()
        tp = 0
        for (k, p) in self.pot.items():
            if k[1:] == cond:
                tp += p
                if r <= tp: return k[0]
        print cond, r, tp
        raw_input('cpd sample returning None')
        return None
        
# Useful as the multiplicitive identity:  p.mul(iPot) = p 
iPot = Potential([], {tuple() : 1.0})

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
    # sum_{values of parents} cpd([v] + values of parents) = 1
    # domain is the list of possible values for this node; supply it
    # if cpd is not supplied
    def __init__(self, name, parents, cpd = None, domain = None):
        self.name = name
        self.parents = parents
        self.cpd = cpd
        self.domain = domain

    def estimateParams(self, data, indices, domains, laplace):
        # First just count, then normalize appropriately
        self.cpd = Potential.makeConstant([self.name] + self.parents,
                                     domains,
                                     1 if laplace else 0)
        for d in data:
            # Increment appropriate potential entry
            self.cpd.incValTuple(tuple([d[i] for i in indices]))
        self.cpd.cpdNormalize()

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

    # Use factor graph inference to get marginal on a single variable
    def qm(self, v, eVars = [], eValues = []):
        return self.factorGraph().computeMarginalWithEvidence(v, eVars,eValues)

    # Construct an instance of FactorGraph representing this same
    # distribution.  One variable and one factor for each node in the
    # Bayes Net
    def factorGraph(self):
        # Make the nodes
        factorNodes = [FactorNode(n.cpd) for n in self.nodes]
        varNodes = [VarNode(n.name) for n in self.nodes]
        return FactorGraph(factorNodes, varNodes)

    # Will replace the potentials in this object (which need not be defined)
    # data is an array, each row is length D, where D is the number of
    # variables in bn indexed in the same order as self.vars
    # If laplace = True, then use the "Laplace correction" for the ML
    # estimator.  
    def estimateParams(self, data, laplace = False, verbose = False):
        for n in self.nodes:
            nodeNames = [n.name] + n.parents
            indices = [self.indices[name] for name in nodeNames]
            domains = [self.nodes[i].domain for i in indices]
            n.estimateParams(data, indices, domains, laplace)
        if verbose:
            print '------------- new model params ----------------'
            for n in self.nodes: print n.cpd
            print '------------------------------------------------'

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
        self.varNodeDict = dict([(n.name, n) for n in varNodes])
        for fn in factorNodes:
            for a in fn.potential.vars:
                vn = self.varNodeDict[a]
                vn.neighborNodes.append(fn)
                fn.neighborNodes.append(vn)

    # Compute and return marginal distribution over var varName
    def computeMarginal(self, varName):
        return self.varNodeDict[varName].computeMarginal()

    # eVars: list of variable names
    # eVals: list of values, same lenght as eVars
    # Conditioned on eVars = eVals, 
    # compute all marginal distributions in all VarNodes, and return
    # a list of them
    def computeMarginalWithEvidence(self, varName, eVars, eVals):
        return self.varNodeDict[varName].\
                                 computeMarginal(dict(zip(eVars, eVals)))

BP_VERBOSE = False

class FactorGraphNode:
    def __init__(self, name):
        self.name = name
        self.neighborNodes = []

class FactorNode(FactorGraphNode):
    idCounter = 0
    def __init__(self, pot):
        # Make uniqe id and use it as name
        FactorGraphNode.__init__(self, FactorNode.idCounter)
        FactorNode.idCounter += 1
        self.potential = pot

    def getMessage(self, target, ev = {}):
        m = reduce(Potential.mul,
                      [n.getMessage(self, ev) for n in self.neighborNodes \
                           if n != target], self.potential).\
                      marginalize([target.name])
        if BP_VERBOSE: print self.name, '->', target.name, m
        return m
                      
class VarNode(FactorGraphNode):
    def getMessage(self, target, ev = {}):
        if self.name in ev:
            m = DeltaPotential((self.name,), (ev[self.name],))
        else:
            m = reduce(Potential.mul,
                          [n.getMessage(self, ev) for n in self.neighborNodes \
                               if n != target], iPot)
        if BP_VERBOSE: print self.name, '->', target.name, m
        return m

    def computeMarginal(self, ev = {}):
        return reduce(Potential.mul,
                      [n.getMessage(self, ev) for n in self.neighborNodes],
                      iPot).normalize()

######################################################################
# Markov models
######################################################################

class MarkovChain:
    # p0 is a potential on 'S0' representing the prior distribution on
    # the state at time 0
    
    # pTrans is a potential on 'St' and 'St+1' representing the transition
    # model.
    def __init__(self, p0, pTrans):
        self.p0 = p0
        self.pTrans = pTrans

    # Unroll into a Bayes net with nodes S0, S1, ... ST
    def bn(self, T):
        # your code here
        return BN([BNNode(
            'S0',
            [],
            cpd = self.p0.rename(['S0']),
            domain = set(k[0] for k in self.p0.pot.iterkeys()))]
            + [BNNode(
                'S' + str(i + 1),
                ['S' + str(i)],
                cpd = self.pTrans.rename(['S' + str(i + 1), 'S' + str(i)]),
                domain = set(k[1] for k in self.pTrans.pot.iterkeys())) for i in range(T)])

    def logLikelihood(self, seq):
        # your code here
        assert seq
        return math.log(self.bn(len(seq) - 1).probT(seq))

    def sampleSequence(self, n):
        result = [self.p0.sample()[0]]
        for i in range(n):
            result.append(self.pTrans.cpdSample((result[-1],)))
        return result

# Data is a list of state sequences;  they do not need to have the
# same length.  Use our bn parameter estimation abiities!
# Domain is a list of possible values that might be encountered; need
# if iwe are going to use laplace.
def estMarkovChainFromData(data, domain, laplace = 0):
    # Estimate P(S0) using first element of each sequence
    n0 = BNNode('S0', [])
    n0.estimateParams(data, [0], [domain], laplace = laplace)
    n1 = BNNode('S1', ['S0'])
    # Rearrange the data set
    # so it consists of all S_t -> S_{t+1} transitions in the data
    # Estimate using all pairs
    pairData = makePairs(data)
    n1.estimateParams(pairData, [1, 0], [domain, domain], laplace = laplace)
    return MarkovChain(n0.cpd, n1.cpd)

######################################################################
# Utilities
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

# Data is a list of sequences of different lengths
# Return a list of all sequential pairs occurring in all sequences
def makePairs(data):
    result = []
    for seq in data:
        result.extend(zip(seq[:-1], seq[1:]))
    return result

######################################################################
# Naive Bayes
######################################################################

# train_data and test_data are each a list of data lists, each data
# list has all the feature_values (typically 0 or 1) followed by a
# "class" value, for example, 1 for spam and 0 for not spam.

def NB(train_data, test_data, feature_names, laplace, verbose):
    # Define the network structure of bn
    bn = None      # your code here
    leafNodes = [BNNode(v, ['Y'], domain = (0, 1)) for v in feature_names]
    root = BNNode('Y', [], domain = (0,1))
    # Take care that the nodes are in the same order as the features in data
    bn = BN(leafNodes + [root])

    # Train network
    bn.estimateParams(train_data, laplace)

    if verbose:
        classes = bn.nodes[-1].domain   # classes in this problem
        print 'Probability of feature given two classes', classes[:2]
        for n in bn.nodes[:-1]:
            print n.name, n.cpd.valTuple((1, classes[0])),n.cpd.valTuple((1, classes[1]))

    # Given a new test case, return the most likely class
    def predictor(x):
    	# your code here
        #print bn.factorGraph().computeMarginalWithEvidence('Y', feature_names, x).pot
        try:
            return max(bn.qm('Y', feature_names, x).pot.iteritems(), key = lambda x: x[1])[0][0]
        except ValueError:
            # Unexpected input (usually happens without laplace)
            # Use default value instead
            return 0


    return errorRate(predictor, test_data)

def errorRate(predictor, testData):
    n_test = len(testData)
    n_wrong = 0
    for d in testData:
        pred = predictor(d[:-1])
        true = d[-1]
        if pred != true: n_wrong += 1
    return n_wrong / float(n_test)

######################################################################
#  Naive Bayes test cases
######################################################################

# Cereal test case
def NBCereal(laplace = False, verbose = True):
    # Class 0 is "older", 1 is "younger"
    trainData = [[1, 0, 0, 0, 0], [1, 0, 0, 1, 0], [1, 1, 1, 1, 0],
                 [0, 0, 0, 1, 0], [0, 1, 1, 0, 1], [1, 1, 1, 0, 1]]
    testData = [[0, 1, 1, 0, 1]]
    featureNames = ('Cornflakes', 'Frosties', 'Sugar Puffs', 'Branflakes')
    return NB(trainData, testData, featureNames, laplace, verbose)

# Spam test case
def NBSpam(n_train = 200, n_test = 200, laplace = False, verbose = True):
    # Get training and test data, eash as a list of data lists, each
    # data list has all the feature values (0 or 1) followed by a
    # "class" value, in this case, 1 for spam and 0 for not spam.
    trainData, testData = getData(n_train, n_test)
    featureNames = ['make', 'address', 'all', '3d', 'our', 'over', 'remove',
            'internet', 'order', 'mail', 'receive', 'will', 'people',
            'report', 'addresses', 'free', 'business', 'email', 'you',
            'credit', 'your', 'font', '000', 'money', 'hp', 'hpl',
            'george', '650', 'lab', 'labs', 'telnet', '857', 'data',
            '415', '85', 'technology', '1999', 'parts', 'pm', 'direct',
            'cs', 'meeting', 'original', 'project', 're', 'edu', 'table',
            'conference', ';', '(', '[', '!', '$', '#', 'capitals']
    return NB(trainData, testData, featureNames, laplace, verbose)

def getData(n_train, n_test):
    from spam import allData
    # Mix up positive and negative examples
    random.shuffle(allData)
    trainData = allData[:n_train]
    testData = allData[n_train:n_train+n_test]
    return trainData, testData

######################################################################
#  Weather Markov chain
######################################################################

def weatherInference():
    # states: sunny, rainy
    weather = MarkovChain(P(['S0'], {('sunny',) : 0.3, ('rainy',) : 0.7}),
                          P(['St+1','St'],
                            {('sunny', 'sunny') : 0.9,
                             ('rainy', 'sunny') : 0.1,
                             ('sunny', 'rainy') : 0.2,
                             ('rainy', 'rainy') : 0.8}))
    week = weather.bn(7)

    global BP_VERBOSE
    BP_VERBOSE = True

    print "week.qm('S3')"
    print week.qm('S3')

    print "\nweek.qm('S7')"
    print week.qm('S7')

    print "\nweek.qm('S3', ['S0'], ['rainy'])"
    print week.qm('S3', ['S0'], ['rainy'])

    print "\nweek.qm('S3', ['S0', 'S7'], ['rainy', 'rainy'])"
    print week.qm('S3', ['S0', 'S7'], ['rainy', 'rainy'])


######################################################################
#  Language classifier
######################################################################

# Learn models for two classes, then do classification.
def testBigramModel(showSamples = False, laplace = 1):
    trainSize = 50000
    testSize = 100  # can go up to 5000, but LL computation is slow

    # Get data and shuffle it, so we get different results each time
    engData = readWords('baskervilles.txt'); random.shuffle(engData)
    frData = readWords('mousquetaires.txt'); random.shuffle(frData)
    # A list of all characters in both doamins
    domain = charDomain(engData).union(charDomain(frData))

    # Construct Markov chains for English and French.  Just use data up
    # to trainSize.

    engMM = estMarkovChainFromData(engData, domain, laplace)
    frMM = estMarkovChainFromData(frData, domain, laplace)

    def predictor(w):
        # Given a new word, return 'english' or 'french' according to which is
        # most likely given your learned models.
        return 'french' if engMM.logLikelihood(w) < frMM.logLikelihood(w) else 'english'

    testData = [(w, 'english') for w in engData[trainSize:trainSize+testSize]]+\
               [(w, 'french') for w in frData[trainSize:trainSize+testSize]]
    print 'Error rate', seqErrorRate(predictor, testData)

    if showSamples:
        print "English-ish words"
        for i in range(10):
            print ''.join(engMM.sampleSequence(5))
        print "\nFrenchish-ish words"
        for i in range(10):
            print ''.join(frMM.sampleSequence(5))

def seqErrorRate(predictor, testData):
    n_test = len(testData)
    n_wrong = 0
    for (seq, true) in testData:
        pred = predictor(seq)
        if pred != true:
            n_wrong += 1
    return n_wrong / float(n_test)        

def readWords(fileName):
    result = []
    with open(fileName,'r') as f:
        for line in f:
            result.extend(unicode(line, 'utf-8').split())
    return result

def charDomain(wordList):
    result = set()
    for w in wordList:
        result.update(w)
    return result

print "Loaded gm.py"        
        
