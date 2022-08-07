from search import *
from highways import *
import time

# An undirected graph of highways in USA.  The cost is defined using
# the distance function from highways.py.  The neighbors dictionary is
# also defined in highways.py. Make sure that you have downloaded the
# maps.zip file and placed it in the same directory as this file.

# NOTE THAT CREATING THIS GRAPH TAKES A BIT OF TIME, so do it only
# once if already defined in the environment.
try:
    # See if it is defined
    usa
except:
    # If it isn't, evaluate it
    usa = UndirectedGraph({id1:{id2:distance(id1,id2) for id2 in neighbors[id1]} \
                           for id1 in neighbors})

class MyFIFOQueue(FIFOQueue):
    def getNode(self, state):
        '''Returns node in queue with matching state'''
        for i in range(self.start, len(self.A)):
            if self.A[i].state == state:
                return self.A[i]
    def __contains__(self, node):
        '''Returns boolean if there is node in queue with matching
        state.  The implementation in utils.py is very slow.'''
        for i in range(self.start, len(self.A)):
            if self.A[i].state == node.state:
                return True

def bidirectional_search(problem):
    '''
    Perform bidirectional search, both directions as breadth-first
    search, should return either the final (goal) node if a path is
    found or None if no path is found.
    '''
    assert problem.goal                # a fixed goal state

    # Below is the definition of BREADTH_FIRST_SEARCH from search.py.
    # You will need to (a) UNDERSTAND and (b) MODIFY this to do
    # bidirectional search.

    #print problem.goal
    node_start = Node(problem.initial)
    node_end = Node(problem.goal)
    if problem.goal_test(node_start.state):
        return node_start
    frontier_start = MyFIFOQueue()
    frontier_end = MyFIFOQueue()
    frontier_start.append(node_start)
    frontier_end.append(node_end)
    explored_start = set()
    explored_end = set()
    while frontier_start and frontier_end:
        node_start = frontier_start.pop()
        explored_start.add(node_start.state)
        for child in node_start.expand(problem):
            if child.state not in explored_start and child not in frontier_start:
                #print 'search: ', child.state
                if child in frontier_end:
                    # Found
                    #print 'found'
                    n = frontier_end.getNode(child.state)
                    tmp_n = n.parent
                    tmp_parent = child
                    tmp_child = None
                    while tmp_n:
                        tmp_child = Node(tmp_n.state, tmp_parent, tmp_n.action)
                        tmp_n = tmp_n.parent
                        tmp_parent = tmp_child
                        #tmp_child = None
                    if problem.goal_test(tmp_parent.state):
                        return tmp_parent
                frontier_start.append(child)
        node_end = frontier_end.pop()
        explored_end.add(node_end.state)
        for child in node_end.expand(problem):
            if child.state not in explored_end and child not in frontier_end:
                #print 'search (backwards): ',child.state
                if child in frontier_start:
                    # Found
                    #print 'found (backwards)'
                    n = frontier_start.getNode(child.state)
                    tmp_n = child.parent
                    tmp_parent = n
                    tmp_child = None
                    #print tmp_n.state, tmp_parent.state
                    while tmp_n:
                        tmp_child = Node(tmp_n.state, tmp_parent, tmp_n.action)
                        tmp_n = tmp_n.parent
                        tmp_parent = tmp_child
                        #tmp_child = None
                        #print tmp_n.state, tmp_parent.state
                    if problem.goal_test(tmp_parent.state):
                        return tmp_parent
                frontier_end.append(child)
    return None

# Modified from search.py
def compare_searchers(problems, header,
                      h = None,
                      searchers=[breadth_first_search]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        print 'Starting', name(searcher)
        t0 = time.time()
        if name(searcher) in ('astar_search', 'greedy_best_first_graph_search'):
            searcher(p, h)
        else:
            searcher(p)
        t1 = time.time()
        print 'Completed', name(searcher)
        return p, t1-t0
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)

def test_map():
    heuristic = lambda x: distance(x.state, 25000502)
    compare_searchers(problems = [GraphProblem(20000071, 25000502, usa)],
                      h = heuristic,
                      searchers = [breadth_first_search,
                                   bidirectional_search,
                                   uniform_cost_search,
                                   astar_search],
                      header = ['Searcher', 'USA(Smith Center, Cambridge)'])

if __name__ == '__main__':
    pass
    test_map()