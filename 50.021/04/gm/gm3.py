import pdb
import operator

def mul(seq):
    return reduce(operator.mul, seq, 1)

print 'Version for week 4 homework'

class Potential:
    # variables: list of strings naming the variables
    # pot: dictionary mapping tuples of variable values to potential value
    def __init__(self, variables, pot):
        self.vars = variables
        self.indices = dict(zip(variables, range(len(variables))))
        self.pot = pot

    def __str__(self):
        return 'Potential('+str(self.vars)+','+str(self.pot)+')'

    # vt is a tuple of values; return the associated potential value
    # return 0 if vt is not explicitly represented in self.pot
    def valTuple(self, vt):
        return self.pot[vt] if vt in self.pot else 0.0

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
    # sum_{v} cpd([v] + values of parents) = 1
    def __init__(self, name, parents, cpd):
        self.name = name
        self.parents = parents
        self.cpd = cpd

class BN:
    # bn is a dictionary
    # key: string
    # value: (list of strings, Potential on varName and parents)
    def __init__(self, nodes):
        self.vars = [n.name for n in nodes]
        # LPK: Check to be sure all parents are in network
        self.nodes = nodes

    # assign is a dictionary from variable names to values, with an
    # entry for every variable in the network
    # Returns probability of that assignment
    def prob(self, assign):
        return mul([n.cpd.val(assign) for n in self.nodes])

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
                self.varNodeDict[a].addNeighbor(fn.name, fn)
                fn.addNeighbor(a, self.varNodeDict[a])

    # Return a Potential representing the marginal distribution on 
    # variable varName
    def computeMarginal(self, varName):
        # your code here
        #print self.varNodeDict
        return self.varNodeDict[varName].computeMarginal()

    # varName: name of variable to compute marginal on
    # eVars: list of variable names
    # eVals: list of values, same lenght as eVars
    # Conditioned on eVars = eVals, 
    # compute all marginal distributions in all VarNodes, and return
    # a list of them
    def computeMarginalWithEvidence(self, varName, eVars, eVals):
        # your code here
        return self.varNodeDict[varName].computeMarginal(dict(zip(eVars, eVals)))

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

    def getMessage(self, target, ev = {}):
        m = reduce(Potential.mul, [self.neighborNodes[k].getMessage(self, ev) for k in self.neighbors() if self.neighborNodes[k] != target], self.potential).marginalize([target.name])
        return m

class VarNode(FactorGraphNode):
    def getMessage(self, target, ev = {}):
        if self.name in ev:
            m = DeltaPotential((self.name,), (ev[self.name],))
        else:
            m = reduce(Potential.mul, [self.neighborNodes[k].getMessage(self, ev) for k in self.neighbors() if self.neighborNodes[k] != target], iPot)
        return m

    def computeMarginal(self, ev = {}):
        #print self.neighborNodes
        #print ev
        return reduce(Potential.mul, [self.neighborNodes[k].getMessage(self, ev) for k in self.neighbors()], iPot).normalize()
        

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

######################################################################
# Parsing BIF files
######################################################################

import re

def bn_parse(file):
    nodes = []
    var_vals = dict()
    f = open(file)
    while True:
        line = f.readline()
        if not line: break
        p = parse_line(line)
        if 'variable' in p[0]:
            var, vals = bn_parse_var_vals(f, p)
            var_vals[var] = vals
        elif 'probability' in p[0]:
            node = bn_parse_node(f, p, var_vals)
            nodes.append(node)
    return BN(nodes)

# def parse_line(line):
#     return [x for x in re.split('(\W+)', line) if x.strip()]
def parse_line(line):
    p = [x for x in re.split('((\s|\(|\)|\{|\}|\,|;)+)', line) if x.strip()]
    return p

def bn_parse_node(f, p, var_vals):
    var, cvars = bn_parse_node_vars(p)
    vals = var_vals[var]
    cpt = bn_parse_node_cpt(f, len(cvars), len(vals))
    pdict = dict()
    for (cvals, probs) in cpt:
        for v,p in zip(vals, probs):
            pdict[tuple([v]+cvals)] = p
    return BNNode(var, cvars, Potential([var]+cvars, pdict))
    
def bn_parse_node_vars(p):
    assert 'probability' in p[0]
    assert '(' in p[1]
    var = p[2]
    if '|' not in p[3]:
        if ')' in p[3]:
            return var, []
        else:
            assert None
    i = 4
    cvars = []
    while ')' not in p[i]:
        pi = p[i]
        i += 1
        if ',' in pi: continue
        cvars.append(pi)
    return var, cvars

def bn_parse_var_vals(f, p):
    vals = []
    assert 'variable' in p[0]
    var = p[1]
    line = f.readline()
    assert line
    np = parse_line(line)
    assert 'type' in np[0]
    assert 'discrete' in np[1]
    assert '[' in np[2]
    n = int(np[3])
    assert ']' in np[4]
    assert '{' in np[5]
    index = 6
    for i in range(n):
        vals.append(np[index])
        index += 2                      # skip ,
    line = f.readline()
    assert line
    np = parse_line(line)
    assert '}' in np[0]
    return var, vals

def bn_parse_node_cpt(f, ncvars, nvals):
    cpt = []
    while True:
        line = f.readline()
        p = parse_line(line)
        if '}' in p[0]: return cpt
        if ncvars == 0:
            assert 'table' in p[0]
            index = 1
            probs = []
            for i in range(nvals):
                probs.append(float(p[index]))
                index += 2
            return [([], probs)]     # one line
        assert '(' in p[0]
        index = 2
        vals = []
        for i in range(ncvars):
            vals.append(p[index])
            index += 2                      # skip ,
        probs = []
        for i in range(nvals):
            probs.append(float(p[index]))
            index += 2                      # skip ,
        cpt.append((vals, probs))


######################################################################
# Test cases
######################################################################
    

# Party animal 
pp = P(['P'], {(0,) : 0.8, (1,) : 0.2})
dp = P(['D'], {(0,) : 0.6, (1,) : 0.4})
hp = P(['H', 'P'], {(0, 0) : .8, (1, 0) : .2,
                    (0, 1) : .1, (1, 1) : .9})
up = P(['U', 'P', 'D'],
       {(0, 0, 0) : .99, (1, 0, 0) : .01,
        (0, 0, 1) :  .1, (1, 0, 1) : .9,
        (0, 1, 0) :  .1, (1, 1, 0) : .9,
        (0, 1, 1) : .001, (1, 1, 1) : .999})
ap = P(['A', 'U'],
        {(0, 0) : 0.5, (1, 0) : 0.5,
         (0, 1) : .05, (1, 1) : .95})

party = BN([BNNode('P', [], pp),
         BNNode('D', [], dp),    
         BNNode('H', ['P'], hp),    
         BNNode('U', ['P','D'], up),    
         BNNode('A', ['U'], ap)])


# Test marginalization and conditioning
def test1():
    joint = {(0, 0, 0) : .03,
             (0, 0, 1) : .07,            
             (0, 1, 0) : .3,            
             (0, 1, 1) : .1,            
             (1, 0, 0) : .02,            
             (1, 0, 1) : .08,            
             (1, 1, 0) : .05,            
             (1, 1, 1) : .35}
    jp = Potential(['A', 'B', 'C'], joint)

    print 'Testing marginalization'
    print "jp.marginalize(['A'])"
    print jp.marginalize(['A'])
    print "jp.marginalize(['B'])"
    print jp.marginalize(['B'])
    print "jp.marginalize(['C'])"
    print jp.marginalize(['C'])
    print "jp.marginalize(['A', 'B'])"
    print jp.marginalize(['A', 'B'])
    print "jp.marginalize([])"
    print jp.marginalize([])
    print "jp.marginalize(['A', 'B', 'C'])"
    print jp.marginalize(['A', 'B', 'C'])

    print 'Testing conditioning'
    print "jp.condition(['C', 'B'], [0, 1])"
    print jp.condition(['C', 'B'], [0, 1])
    print "jp.condition(['B', 'C'], [0, 1])"
    print jp.condition(['B', 'C'], [0, 1])
    print "jp.condition(['C'], [0])"
    print jp.condition(['C'], [0])
    print "jp.condition([], [])"
    print jp.condition([], [])
    print "jp.condition(['A','B','C'], [0, 1, 0])"
    print jp.condition(['A','B','C'], [0, 1, 0])

# Wet grass
wg = BN([BNNode('R', [], P(['R'], {(0,) : .8, (1,) : .2})),
         BNNode('S', [], P(['S'], {(0,) : .9, (1,) : .1})),
         BNNode('J', ['R'], 
               P(['J', 'R'], 
                  {(0, 0) : 0.8, (0, 1) : 0.0, (1, 0) : 0.2, (1, 1) : 1.0})),
         BNNode('T', ['R', 'S'],
                P(['T', 'R', 'S'], 
                   {(0, 0, 0) : 1.0, (1, 0, 0) : 0.0,
                   (0, 0, 1) : 0.1, (1, 0, 1) : 0.9,
                   (0, 1, 0) : 0.0, (1, 1, 0) : 1.0,
                   (0, 1, 1) : 0.0, (1, 1, 1) : 1.0}))])

# Test BN query method using the wet grass model.
def test2():
    print 'Testing prob'

    print "wg.prob({'R' : 1, 'S' : 1, 'T' : 0, 'J' : 0})"
    print wg.prob({'R' : 1, 'S' : 1, 'T' : 0, 'J' : 0})
    print "wg.prob({'R' : 0, 'S' : 0, 'T' : 0, 'J' : 0})"
    print wg.prob({'R' : 0, 'S' : 0, 'T' : 0, 'J' : 0})
    print "wg.prob({'R' : 1, 'S' : 0, 'T' : 0, 'J' : 0})"
    print wg.prob({'R' : 1, 'S' : 0, 'T' : 0, 'J' : 0})
    print "wg.prob({'R' : 0, 'S' : 1, 'T' : 0, 'J' : 0})"
    print wg.prob({'R' : 0, 'S' : 1, 'T' : 0, 'J' : 0})

    
    print 'Testing query'
    
    print "wg.query(['S'])"
    print wg.query(['S'])
    print "wg.query(['S'], ['T'], [1])"
    print wg.query(['S'], ['T'], [1])
    print "wg.query(['S'], ['T', 'J'], [1, 1])"
    print wg.query(['S'], ['T', 'J'], [1, 1])

    print "wg.query('R')"
    print wg.query('R')
    print "wg.query('R', ['T'], [1])"
    print wg.query('R', ['T'], [1])
    print "wg.query('R', ['T', 'S'], [1, 1])"
    print wg.query('R', ['T', 'S'], [1, 1])

def test3():
    print 'Testing wet grass marginals'
    for v in wg.vars:
        m = wg.factorGraph().computeMarginal(v)
        print m

    print 'Testing party animal (Barber question 3.1) marginals'
    for v in party.vars:
        m = party.factorGraph().computeMarginal(v)
        print m

# Test belief propagation with evidence

def test4():
    m = wg.factorGraph().computeMarginalWithEvidence('S', ['T'], [1])
    print m
    m = party.factorGraph().computeMarginalWithEvidence('P', ['A', 'H'], [1, 1])
    print m

# Factor graph example from 6.867 notes

pdg = Potential(['D','G'], {(0, 0) : 1, (0, 1) : 4, (1, 0) : 4, (1, 1) : 1})
pb = Potential(['B'], {(0,) : 3, (1,) : 7})
pabd = Potential(['A','B','D'],
              {(0, 0, 0) : 1, (0, 0, 1) : 2, (0, 1, 0) : 4,
               (0, 1, 1) : 2, (1, 0, 0) : 2, (1, 0, 1) : 4,
               (1, 1, 0) : 1, (1, 1, 1) : 3})
pa = Potential(['A'], {(0,) : 3, (1,) : 7})
pac = Potential(['A', 'C'], {(0,0) : 1, (0, 1) : 4, (1, 0) : 4, (1, 1) : 1})
pcf = Potential(['C', 'F'], {(0,0) : 1, (0, 1) : 4, (1, 0) : 3, (1, 1) : 1})
pce = Potential(['C', 'E'], {(0,0) : 1, (0, 1) : 4, (1, 0) : 2, (1, 1) : 1})

fg6867 = FactorGraph([FactorNode(p) for p in [pdg, pb, pabd, pa, pac, pcf,pce]],
                     [VarNode(n) for n in ['A','B','C','D','E','F','G']])

def test5():
    m = fg6867.computeMarginal('A')
    print m

def test6():
    # Crate the BN instance from a file
    bn = bn_parse('alarmBottom.bif')    # Assumes it is in same directory
    # your code here
    #print bn
    print bn.factorGraph().computeMarginalWithEvidence('HR', ['BP'], ['LOW'])
    print bn.query(['HR'], ['BP'], ['LOW'])

def test_dancing_bees():
    bn = BN([BNNode('Day', [], P(['Day'], {(name, ) : 1.0 / 7.0 for name in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']})),
             BNNode('Event', ['Day'], P(['Event', 'Day'], dict(
                [((event, day), prob) for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
                    for event, prob in zip(('food', 'other bees', 'Japanese Giant Hornets ATTACKING!', 'Nothing'), (0.4, 0.1, 0.2, 0.3))]
                + [((event, day), prob) for day in ['Sat', 'Sun']
                    for event, prob in zip(('food', 'other bees', 'Japanese Giant Hornets ATTACKING!', 'Nothing'), (0.2, 0.3, 0.0, 0.5))]))),
             BNNode('Shake', ['Event'], P(['Shake', 'Event'], {
                (1, 'food'): 1.0,
                (1, 'other bees'): 1.0,
                (1, 'Japanese Giant Hornets ATTACKING!'): 1.0,
                (0, 'Nothing'): 1.0})),
             BNNode('Circles', ['Event'], P(['Circles', 'Event'], {
                (1, 'food'): 1.0,
                (0, 'other bees'): 1.0,
                (0, 'Japanese Giant Hornets ATTACKING!'): 1.0,
                (1, 'Nothing'): 1.0})),
             BNNode('Flap', ['Event'], P(['Flap', 'Event'], {
                (0, 'food'): 1.0,
                (1, 'other bees'): 1.0,
                (1, 'Japanese Giant Hornets ATTACKING!'): 1.0,
                (0, 'Nothing'): 1.0})),
             BNNode('Moonwalk', ['Event'], P(['Moonwalk', 'Event'], {
                (1, 'food'): 1.0,
                (1, 'other bees'): 1.0,
                (0, 'Japanese Giant Hornets ATTACKING!'): 1.0,
                (1, 'Nothing'): 1.0}))])

    print 'Probability of having found food:'
    print bn.factorGraph().computeMarginal('Event').valTuple(('food', ))

    print 
    print 'Probability of it being Tuesday when shaking in circles and doing moonwalk:'
    print bn.factorGraph().computeMarginalWithEvidence('Day', ['Shake', 'Circles', 'Moonwalk'], [1, 1, 1]).valTuple(('Tue', ))
    
    print 
    print 'Probability of shaking:'
    print bn.factorGraph().computeMarginal('Shake').valTuple((1, ))

    print 
    print 'Probability of shaking:'
    print bn.factorGraph().computeMarginalWithEvidence('Event', ['Shake'], [1]).valTuple(('Japanese Giant Hornets ATTACKING!', ))

    print 
    print 'Probability of Monday given it is ONLY shaking and flapping:'
    print bn.factorGraph().computeMarginalWithEvidence('Day', ['Shake', 'Flap', 'Circles', 'Moonwalk'], [1, 1, 0, 0]).valTuple(('Mon', ))

print "Loaded gm.py"        
