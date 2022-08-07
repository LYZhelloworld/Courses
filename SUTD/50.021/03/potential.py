######################################################################
# Potential class
######################################################################

class Potential:
    # variables: list of strings naming the variables
    # pot: dictionary mapping tuples of variable values to potential value
    def __init__(self, variables, pot):
        self.vars = variables
        self.indices = dict(zip(variables, range(len(variables))))
        self.pot = pot

    def __str__(self):
        return 'Potential('+str(self.vars)+','+str(self.pot)+')'
    
    # qVars is a list of variable names
    # Sum out all other variables, returning a new potential on qVars
    def marginalize(self, qVars):
        # Your code here
        result = {}
        new_indices = removeVals(range(len(self.vars)), [self.indices[v] for v in qVars])
        #print new_indices
        for key, value in self.pot.items():
            new_key = removeIndices(key, new_indices)
            addToEntry(result, new_key, self.pot[key] if key in self.pot else 0.0)
        return Potential(qVars, result)
    

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
        # Your code here
        result = {}
        new_indices = [self.indices[value] for value in cVars]
        for key, value in self.pot.items():
            if all(key[index] == value for (index, value) in zip(new_indices, cVals)):
                result[removeIndices(key, new_indices)] = self.pot[key]
        return Potential(removeIndices(self.vars, new_indices), result).normalize()

    # Divide through by sum of values; returns a new Potential on the
    # same variables with potential values that sum to 1 over the
    # whole domain.
    def normalize(self):
        # Your code here
        total = sum(self.pot.values())
        result = dict([(value, prob / total) for (value, prob) in self.pot.items()])
        return Potential(self.vars, result)

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

######################################################################
# Utilities
######################################################################

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
