import maze
import mazeIO
import sys
#the deque class supports pops from both ends
from collections import deque 

###A class for solving mazes###

class MazeSolver:

    #Initializes the solver with the maze to solve
    #The maze class contains (see maze.py):
        # 1) matrix: the matrix of characters ('W', 'O', 'B', or 'E') 
        #            representing the maze
        # 2) start: the starting square as [row, column]
        # 3) end: the ending square as [row, column]
    def __init__(self, maze):

        self.maze = maze

    #Solves a maze.
    #search_type can be either DFS or BFS,
    #depending on whether you want the maze solved
    #using depth first search or breadth first search,
    #respectively.
    #
    #Returns a path through the maze as a list of [row, column]
    #squares where path[0] = maze.start and
    #path[len(path)-1] = maze.end
    #For every square i, path[i] should be adjacent to
    #path[i+1] and maze.matrix[i] should not be 'W'
    #
    #Also returns all the nodes expanded as a [row, column]
    #list.  These need not be in any particular order and
    #should include the nodes on the path.

    def solve_maze(self, search_type):
        
        if (search_type != "DFS" and search_type != "BFS"):
            print "Invalid search type"
            return [], []
        
        if (self.maze.start == []):
            print "Maze does not have starting square"
            return [], []

        if (self.maze.end == []):
            print "Maze does not have ending square"
            return [], []
        
        path = []
        expanded = []

        #######################################
        ############YOUR CODE HERE#############
        #######################################
        
        if(search_type == 'DFS'): # Depth First Search
            visited = [[False for j in self.maze.matrix[0]] for i in self.maze.matrix]
            stack = deque()
            stack.append((self.maze.start[0], self.maze.start[1]))
            visited[self.maze.start[0]][self.maze.start[1]] = True # Starting point: visited
            succeeded = False
            #print 'visit:' , stack[-1][0] , stack[-1][1]    #debug
            expanded.append([self.maze.start[0], self.maze.start[1]])
            
            while(stack):
                x = stack[-1][0]
                y = stack[-1][1]
                #print 'visit:' , stack[-1][0] , stack[-1][1]    #debug
                expanded.append([x, y])
                if(x == self.maze.end[0] and y == self.maze.end[1]):
                    succeeded = True
                    break
                
                #Down
                if(x+1 < len(self.maze.matrix)):
                    if(self.maze.matrix[x+1][y] != 'W' and visited[x+1][y] == False):
                        stack.append((x+1, y))
                        visited[x+1][y] = True
                        continue
                
                #Right
                if(y+1 < len(self.maze.matrix[0])):
                    if(self.maze.matrix[x][y+1] != 'W' and visited[x][y+1] == False):
                        stack.append((x, y+1))
                        visited[x][y+1] = True
                        continue
                        
                #Up
                if(x+1 < len(self.maze.matrix)):
                    if(self.maze.matrix[x-1][y] != 'W' and visited[x-1][y] == False):
                        stack.append((x-1, y))
                        visited[x-1][y] = True
                        continue
                
                #Left
                if(y+1 < len(self.maze.matrix[0])):
                    if(self.maze.matrix[x][y-1] != 'W' and visited[x][y-1] == False):
                        stack.append((x, y-1))
                        visited[x][y-1] = True
                        continue
                        
                #Searched
                stack.pop()
                
            if(succeeded):
                for i in stack:
                    path.append([i[0], i[1]])
            else:
                path = []
            
        else: # Breadth First Search
            visited = [[False for j in self.maze.matrix[0]] for i in self.maze.matrix]
            previous = [[None for j in self.maze.matrix[0]] for i in self.maze.matrix]
            queue = deque()
            queue.append((self.maze.start[0], self.maze.start[1]))
            visited[self.maze.start[0]][self.maze.start[1]] = True # Starting point: visited
            succeeded = False
            #print 'visit:' , queue[0][0] , queue[0][1]    #debug
            expanded.append([self.maze.start[0], self.maze.start[1]])
            
            while(queue):
                x = queue[0][0]
                y = queue[0][1]
                #print 'visit:' , queue[0][0] , queue[0][1]    #debug
                expanded.append([x, y])
                if(x == self.maze.end[0] and y == self.maze.end[1]):
                    succeeded = True
                    break
                
                #Down
                if(x+1 < len(self.maze.matrix)):
                    if(self.maze.matrix[x+1][y] != 'W' and visited[x+1][y] == False):
                        queue.append((x+1, y))
                        visited[x+1][y] = True
                        previous[x+1][y] = (x, y)
                
                #Right
                if(y+1 < len(self.maze.matrix[0])):
                    if(self.maze.matrix[x][y+1] != 'W' and visited[x][y+1] == False):
                        queue.append((x, y+1))
                        visited[x][y+1] = True
                        previous[x][y+1] = (x, y)
                        
                #Up
                if(x+1 < len(self.maze.matrix)):
                    if(self.maze.matrix[x-1][y] != 'W' and visited[x-1][y] == False):
                        queue.append((x-1, y))
                        visited[x-1][y] = True
                        previous[x-1][y] = (x, y)
                
                #Left
                if(y+1 < len(self.maze.matrix[0])):
                    if(self.maze.matrix[x][y-1] != 'W' and visited[x][y-1] == False):
                        queue.append((x, y-1))
                        visited[x][y-1] = True
                        previous[x][y-1] = (x, y)

                queue.popleft()
                #print queue    #debug
                
            if(succeeded):
                i = (self.maze.end[0], self.maze.end[1])
                path.append([i[0], i[1]])
                i = previous[i[0]][i[1]]
                
                while(i != None):                
                    path.append([i[0], i[1]])
                    i = previous[i[0]][i[1]]
                
                path.reverse()
            else:
                path = []
        

        return path, expanded

#This main function will allow you to test your maze solver
#by printing your solution to a ppm image file or ascii text file.
#
#Usage: maze_solver input_filename output_filename <image scaling>
#
#You must specify the input file name and the output file name. 
#The input should be a .ppm or .txt file in the form output by
#the mazeIO class.  See test_maze.ppm and many_paths.txt for examples.
#
#You also need to specify a search type:
#BFS: solves the maze using breadth first search
#DFS: solves the maze using depth first search
#
#For small mazes, a one-to-one
#correspondence between maze squares and pixels will be too small to see
#(ie a 10x10 maze gives an image of 10x10 pixels)
#so the ppm image is scaled when written out.  If you are trying to
#read in a scaled ppm image, you MUST specify image scaling to be
#the correct scaling or you will get a very strange looking solution.
#For example, the scaling used to print out test_maze.ppm was 6 so
#to solve test_maze.ppm using breadth first search and write it out to
#test_path.ppm you would use:
#
#python maze_solver_skeleton.py test_maze.ppm test_path.ppm BFS 6
#
#If you read in an image, the same scaling will be used to output the
#image so in the example test_path.ppm will also be scaled by a factor
#of 6.  The actual maze is 50x50 so both ppm images are 300x300 pixels.
#
#You may read in a maze as a text file and output it as an image file or
#vice-versa.  If you read a maze in as a text file, you can specify a
#scaling just for the output file.

def main(argv):

    if (len(argv) < 4):
        print "Usage: maze_solver input_file output_file search-type <image scaling>"
        return
    infilename = argv[1]
    innameparts = infilename.split('.')
    if (len(innameparts) != 2 or (innameparts[1] != "ppm" \
                                  and innameparts[1] != "txt")):
        print "Must enter an input file name ending in .ppm or .txt"
        return
    outfilename = argv[2]
    outnameparts = outfilename.split('.')
    if (len(outnameparts) != 2 or (outnameparts[1] != "ppm" \
                                   and outnameparts[1] != "txt")):
        print "Must enter an output file name ending in .ppm or .txt"
        return
    if (argv[3] != "DFS" and argv[3] != "BFS"):
        print "Please enter valid search type.  Choose one of: BFS, DFS"
        return
    searchtype = argv[3]
    scaling = 1
    if (len(argv) > 4):
        try:
            scaling = int(argv[4])
        except:
            scaling = 1
    if (scaling <= 0):
        scaling = 1
    if (innameparts[1] == "ppm"):
        maze = mazeIO.ppmIO.read_maze_from_ppm(infilename, scaling)
    else:
        maze = mazeIO.asciiIO.read_maze_from_ascii(infilename)
    solver = MazeSolver(maze)
    path, expanded = solver.solve_maze(searchtype)
    print "Length of path:", len(path), \
        "\nNumber of nodes expanded: ", len(expanded)
    if (outnameparts[1] == "ppm"):
        mazeIO.ppmIO.write_visited_to_ppm(outfilename, maze, expanded, path, scaling)
    else:
        mazeIO.asciiIO.write_visited_to_ascii(outfilename, maze, expanded, path)

if __name__ == "__main__":
    main(sys.argv)

