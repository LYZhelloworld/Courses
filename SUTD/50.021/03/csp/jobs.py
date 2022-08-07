from csp import *

# jobs is a list of jobs
# a job is a list of operations
# an operation is [name, list of alternative resources that could be
# used, a release time (earliest start time (usually 0), and a duration.

# This example is from "Variable And Value Ordering Heuristics For The
# Job Shop Scheduling Constraint Satisfaction Problem", Norman
# M. Sadeh and Mark S. Fox.  A deadline of 15 should work.

jobs4 = [ [['o_1_1', [1], 0, 3], ['o_1_2', [2], 0, 3], ['o_1_3', [3], 0, 3]],
          [['o_2_1', [1], 0, 3], ['o_2_2', [2], 0, 3]],
          [['o_3_1', [3], 0, 3], ['o_3_2', [1], 0, 3], ['o_3_3', [2], 0, 3]],
          [['o_4_1', [4], 0, 3], ['o_4_2', [2], 0, 3]] ]

# A more compact specification, assuming a single resource per
# operation and start times of 0

# Each row specifies a job by X pairs of consecutive numbers. Each
# pair of numbers defines one task of the job, which represents the
# processing of a job on a machine. For each pair, the first number
# identifies the machine it executes on, and the second number is the
# duration. The order of the X pairs defines the sequence of the
# tasks for a job.

# Simple example from www.columbia.edu/~cs2035/courses/ieor4405.S03/jobshop.doc
# A deadline of 31 should work.
j3 = [
    [1, 10, 2, 8, 3, 4],
    [2, 8, 1, 3, 4, 5, 3, 6],
    [1, 4, 2, 7, 4, 3]
    ]

# http://yetanothermathprogrammingconsultant.blogspot.sg/2012_04_01_archive.html
#            job1  job2  job3  job4  job5  job6  job7  job8  job9  job10 
#  machine1   4     2     1     5     4     3     5     2     1     8 
#  machine2   2     5     8     6     7     4     7     3     6     2 
#  machine3   2     8     6     2     2     4     2     7     1     8
# A deadline of 52 should work.

m3x10 = [
[ 4,     2,     1,     5,     4,     3,     5,     2,     1,     8 ],
[ 2,     5,     8,     6,     7,     4,     7,     3,     6,     2 ],
[ 2,     8,     6,     2,     2,     4,     2,     7,     1,     8 ]]

# This is the transpose of what we want
j10x3 = [[1, 0, 2, 0, 3, 0] for i in range(10)]
for mi, m in enumerate(m3x10):
    for ji, duration in enumerate(m):
        j10x3[ji][mi*2+1] = duration
#print j10x3

# This example is a (very hard) job shop scheduling problem from Lawrence
# (1984). This test is also known as LA19 in the literature, and its
# optimal makespan is known to be 842 (Applegate and Cook,
# 1991). There are 10 jobs (J1-J10) and 10 machines (M0-M9). Every job
# must be processed on each of the 10 machines in a predefined
# sequence. The objective is to minimize the completion time of the
# last job to be processed, known as the makespan.

j10x10 = [
[2,  44,  3,   5,  5,  58,  4,  97,  0,   9,  7,  84,  8,  77,  9,  96,  1,  58,  6,  89],
[4,  15,  7,  31,  1,  87,  8,  57,  0,  77,  3,  85,  2,  81,  5,  39,  9,  73,  6,  21],
[9,  82,  6,  22,  4,  10,  3,  70,  1,  49,  0,  40,  8,  34,  2,  48,  7,  80,  5,  71],
[1,  91,  2,  17,  7,  62,  5,  75,  8,  47,  4,  11,  3,   7,  6,  72,  9,  35,  0,  55],
[6,  71,  1,  90,  3,  75,  0,  64,  2,  94,  8,  15,  4,  12,  7,  67,  9,  20,  5,  50],
[7,  70,  5,  93,  8,  77,  2,  29,  4,  58,  6,  93,  3,  68,  1,  57,  9,   7,  0,  52],
[6,  87,  1,  63,  4,  26,  5,   6,  2,  82,  3,  27,  7,  56,  8,  48,  9,  36,  0,  95],
[0,  36,  5,  15,  8,  41,  9,  78,  3,  76,  6,  84,  4,  30,  7,  76,  2,  36,  1,   8],
[5,  88,  2,  81,  3,  13,  6,  82,  4,  54,  7,  13,  8,  29,  9,  40,  1,  78,  0,  75],
[9,  88,  4,  54,  6,  64,  7,  32,  0,  52,  2,   6,  8,  54,  5,  82,  3,   6,  1,  26],
]

def parse_jobs(jobs):
    parsed = []
    for ji, j in enumerate(jobs):
        job = []
        for i in range(len(j)/2):
            job.append(['o_%d_%d'%(ji,i), [j[i*2]], 0, j[i*2+1]])
        parsed.append(job)
    return parsed

#####################################################
# The example jobs defined above are
# jobs4 - defined at the top of the file
jobs3 = parse_jobs(j3)
jobs10x10 = parse_jobs(j10x10)
jobs10x3 = parse_jobs(j10x3)
#####################################################

class Jobs:
    def __init__(self, jobs):
        self.jobs = []
        for job in jobs:
            self.jobs.append(Job(job))

    def __iter__(self):
        return self.jobs.__iter__()

    def __repr__(self):
        result = ''
        for i in range(len(self.jobs)):
            result += 'Job ' + str(i + 1) + '\n'
            result += str(self.jobs[i])
            result += '\n'
        return result

class Job:
    def __init__(self, job):
        self.operations = []
        for operation in job:
            self.operations.append(Operation(operation[0], operation[1], operation[2], operation[3]))

    def __contains__(self, op):
        for operation in self.operations:
            if operation == op:
                return True
        return False

    def __iter__(self):
        return self.operations.__iter__()

    def __repr__(self):
        return '\n'.join([str(operation) for operation in self.operations])

class Operation:
    def __init__(self, name, resources, start, duration):
        self.name = name
        self.resources = tuple(resources)
        self.start = start
        self.duration = duration

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<%s,%s,%d,%d>' % (self.name, str(list(self.resources)), self.start, self.duration)

    def __hash__(self):
        return self.name.__hash__()

def generate_CSP(jobs, deadline):
    """ From CSP class in csp.py
        vars        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
                    """
    csp_vars = []
    csp_domains = {}
    csp_neighbors = {}

    for job in jobs:
        operation_in_job = []
        for operation in job:
            csp_vars.append(operation)
            if operation not in csp_neighbors:
                csp_neighbors[operation] = []
            for tmp_op in operation_in_job:
                if tmp_op not in csp_neighbors:
                    csp_neighbors[tmp_op] = []
                csp_neighbors[tmp_op].append(operation)
                csp_neighbors[operation].append(tmp_op)
            operation_in_job.append(operation)

    for job1 in jobs:
        for operation1 in job1:
            for job2 in jobs:
                for operation2 in job2:
                    if operation1 == operation2:
                        continue
                    if (set(operation1.resources) & set(operation2.resources)):
                        csp_neighbors[operation1].append(operation2)
                        csp_neighbors[operation2].append(operation1)

    for operation in csp_vars:
        csp_domains[operation] = range(deadline + 1)

    def csp_constraints(A, a, B, b):
        # Check deadline
        if a + A.duration > deadline or b + B.duration > deadline:
            return False
        # Check if neighbors
        for job in jobs:
            pos_A = None
            pos_B = None
            for operation in job:
                if (operation) == A:
                    pos_A = job.operations.index(operation)
                if (operation) == B:
                    pos_B = job.operations.index(operation)
            if pos_A == None or pos_B == None:
                continue
            if A < B:
                if a + A.duration > b:
                    return False
            else:
                if b + B.duration > a:
                    return False
            break
        # Check if same resource
        if (set(A.resources) & set(B.resources)):
            if set(range(a, a + A.duration)) & set(range(b, b + B.duration)):
                return False
        return True

    return CSP(csp_vars, csp_domains, csp_neighbors, csp_constraints)

def print_search_result(result):
    if result == None:
        print 'No results found'
        print ''
        return
    assert(type(result) == dict)
    time_list = set()
    for time in result.values():
        time_list.add(time)
    time_list = list(time_list)
    time_list.sort()
    for time in time_list:
        print 'Time %d' % time
        for item in result:
            if result[item] == time:
                print item
        print ''

if __name__ == '__main__':
    jobs_to_test = [(jobs4, 15), (jobs3, 31), (jobs10x3, 58)]
    for jobs in jobs_to_test:
        j = Jobs(jobs[0])
        print j
        print_search_result(backtracking_search(generate_CSP(j, jobs[1]), select_unassigned_variable = mrv, order_domain_values = lcv, inference = forward_checking))
