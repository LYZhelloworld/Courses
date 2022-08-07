import random
import math
import drawing as dw
from search import *

class Robot:
    def __init__(self, radius, ranges):
        # initialize radius and ranges for x and y
        self.radius = radius
        self.ranges = ranges

    def sample(self):
        # returns robot loc, an (x,y) tuple
        return (random.uniform(self.ranges[0][0], self.ranges[0][1]), random.uniform(self.ranges[1][0], self.ranges[1][1]))

    def collides(self, loc, obstacles):
        # returns True if there is a collision with any of the obstacles when the robot stands at loc
        # No intersection: d >= R+r
        # obstacle[0]: coordinates, obstacle[1]: radius
        return any([((obstacle[0][0]-loc[0])**2 + (obstacle[0][1]-loc[1])**2) < (obstacle[1]+self.radius) ** 2 for obstacle in obstacles])

    def connect(self, loc1, loc2, maxDist=0.01):
        # returns a list of locs (list of (x,y) tuples) along the line between loc1 and loc2
        # assume distance = d, and length of line segment = D
        # D/d = (y2-y1)/(y-y1) = (x2-x1)/(x-x1)
        # y = (y2-y1)(d/D)+y1, x = (x2-x1)(d/D)+x1
        d = maxDist
        result = []
        D = math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)
        while d <= D:
            result.append(((loc2[0] - loc1[0]) * d / D + loc1[0], (loc2[1] - loc1[1]) * d / D + loc1[1]))
            d += maxDist
        return result

    def draw(self, p):
        if not window: return
        (x,y) = p
        window.drawOval((x - self.radius, y - self.radius), (x + self.radius, y + self.radius), color='blue')
        window.update()

class PRM:
    def __init__(self, robot, obstacles):
        # your code here
        self.robot = robot
        self.obstacles = obstacles
        self.samples = []

    def addSample(self, sample):
        # add a candidate sample (a loc) to the list of samples if the robot at that loc would not collide with any obstacle.
        if not self.robot.collides(sample, self.obstacles):
            self.samples.append(sample)
            return True
        return False

    def addRandomSamples(self, n=100):
        # add n samples
        for i in range(n):
            loc = self.robot.sample()
            while not self.addSample(loc):
                loc = self.robot.sample()

    def validStep(self, loc1, loc2):
        # checks whether all the locs that connect loc1 to loc2 are free of collisions.
        points = self.robot.connect(loc1, loc2)
        return not any([self.robot.collides(loc, self.obstacles) for loc in points])

    def findPath(self, start, goal, k=20):
       # returns a list of locs, i.e. (x,y) tuples corresponding to robot positions, starting at start and ending at goal.
        self.addSample(start)
        self.addSample(goal)
        for i in range(k):
            print 'Attempt', i
            self.addRandomSamples()
            self.draw()
            # search for a path, draw it and return it if one is found;
            # the path should be a list of locs.
            graph = dict()
            for loc1 in self.samples:
                for loc2 in self.samples:
                    if loc1 == loc2:
                        continue
                    if self.validStep(loc1, loc2):
                        if not graph.get(loc1):
                            graph[loc1] = {}
                        graph[loc1][loc2] = math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)
            n = graph_search(GraphProblem(start, goal, Graph(graph)), FIFOQueue())
            if n == None:
                continue
            while n != None:
                self.robot.draw(n.state)
                n = n.parent
            return True
        return False

    def draw(self):
        # draw obstacles, robot, and samples
        if not window: return
        window.clear()
        for (opx, opy), orad in self.obstacles:
            window.drawOval((opx - orad, opy - orad), (opx + orad, opy + orad), color='black')
            for (x,y) in self.samples:
                window.drawPoint(x, y, 'red')
        window.update()

try:
    window
except:
    window = None

def testPRM ():
    global window
    if not window:
        window = makeSimpleWindow(10, 10, 500, 'PRM')
    robot = Robot(0.5, ((0.5, 9.5), (0.5, 9.5)))
    prm = PRM(robot, [((3.0, 3.0), 1.0), ((6.0, 6.0), 2.0), ((6.5, 1.9), 1.0), ((2.0, 6.0), 2.0)])
    prm.draw()
    return prm.findPath((0.6, 0.6), (8.0, 8.0))

def makeSimpleWindow(dx, dy, windowWidth, title):
    return dw.DrawingWindow(windowWidth, windowWidth, 0, max(dx, dy), 0, max(dx, dy), title)

if __name__ == '__main__':
    testPRM()