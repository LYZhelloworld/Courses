import maze as maze_class
import mazeIO
import random
import sys

###A class for creating mazes###

class MazeCreator:

    #Constructs a maze creator, which
    #just stores the size of the maze
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols


    #You will return a maze object, maze, from this function such that:
    # 1) maze.matrix is size rows X cols
    # 2) maze.end = end and maze.matrix[end[0]][end[1]] = 'E'
    # 3) maze.start = some square you pick and 
    #    maze.matrix[maze.start[0]][maze.start[1]] = 'B'
    # 4) There is an open path from start to end, marked out by 'O's
    #    and the maze is an interesting maze created using DFS
    
    #Input: end: the goal square as [row, column]
    def create_maze(self, end):

        #this creates a rows X cols matrix of all walls
        matrix = [['W' for i in range(self.cols)] \
                   for j in range(self.rows)]        
        
        #this creates a new maze (see maze.py)
        #the maze class stores:
        # 1) the matrix we have just created
        # 2) the starting square, which is the empty list right now
        # 3) the ending square, which was passed into the function
        #you can set the starting square using
        # maze.start = start
        
        maze = maze_class.Maze(matrix, [], end)

        ##########################################
        ############YOUR CODE HERE################
        ##########################################
        
        maze.matrix[end[0]][end[1]] = 'E'
        
        # Due to the problem of stack overflow, we need to implement recursion with code
        recur = []
        recur.append([end[0], end[1]]) # randomDirections, isScanned, x, y
        
        while(recur):
            #print recur    #debug
            #print '\n'.join(['\t'.join(__row) for __row in maze.matrix])   #debug
            randomDirections = []
            if(recur[-1][0]+2 < self.rows):
                if(maze.matrix[recur[-1][0]+2][recur[-1][1]] == 'W'):
                    randomDirections.append(0) # Down
            if(recur[-1][1]+2 < self.cols):
                if(maze.matrix[recur[-1][0]][recur[-1][1]+2] == 'W'):
                    randomDirections.append(1) # Right
            if(recur[-1][0]-2 >= 0):
                if(maze.matrix[recur[-1][0]-2][recur[-1][1]] == 'W'):
                    randomDirections.append(2) # Up
            if(recur[-1][1]-2 >= 0):
                if(maze.matrix[recur[-1][0]][recur[-1][1]-2] == 'W'):
                    randomDirections.append(3) # Left
            
            random.shuffle(randomDirections)
            
            #print recur    #debug
            #print '\n'.join(['\t'.join(__row) for __row in maze.matrix])    #debug
            if(randomDirections):
                i = randomDirections.pop()
                if(i == 0): # Down
                    maze.matrix[recur[-1][0]+1][recur[-1][1]] = 'O'
                    maze.matrix[recur[-1][0]+2][recur[-1][1]] = 'O'
                    #__dfs_search(self, maze.matrix, x+2, y)
                    recur.append([recur[-1][0]+2, recur[-1][1]])
                    continue
                elif(i == 1): # Right
                    maze.matrix[recur[-1][0]][recur[-1][1]+1] = 'O'
                    maze.matrix[recur[-1][0]][recur[-1][1]+2] = 'O'
                    #__dfs_search(self, maze.matrix, x, y+2)
                    recur.append([recur[-1][0], recur[-1][1]+2])
                    continue
                elif(i == 2): # Up
                    maze.matrix[recur[-1][0]-1][recur[-1][1]] = 'O'
                    maze.matrix[recur[-1][0]-2][recur[-1][1]] = 'O'
                    #__dfs_search(self, maze.matrix, x-2, y)
                    recur.append([recur[-1][0]-2, recur[-1][1]])
                    continue
                elif(i == 3): # Left
                    maze.matrix[recur[-1][0]][recur[-1][1]-1] = 'O'
                    maze.matrix[recur[-1][0]][recur[-1][1]-2] = 'O'
                    #__dfs_search(self, maze.matrix, x, y-2)
                    recur.append([recur[-1][0], recur[-1][1]-2])
                    continue
            else:
                recur.pop()
                continue
        
        #__dfs_search(self, maze.matrix, end[0], end[1])
        
        startPoint = []
        # Choose a starting point
        for i in range(len(maze.matrix)):
            for j in range(len(maze.matrix[0])):
                if(maze.matrix[i][j] == 'O'):
                    startPoint.append((i, j))
        random.shuffle(startPoint)
        maze.matrix[startPoint[0][0]][startPoint[0][1]] = 'B'
        
        return maze
        
    

#This main function will allow you to test your maze creator
#by printing your maze to a ppm image file or ascii text file.
#
#Usage: maze_creator rows cols output_filename <image scaling>
#
#You must specify the size of the maze (rows X cols) and the
#output file name.  This name should end in .ppm for a ppm image
#and .txt for an ascii file.  
#
#If you have a small maze, a one-to-one
#correspondence between maze squares and pixels will be too small to see
#(ie a 10x10 maze gives an image of 10x10 pixels)
#so the optional argument image scaling allows you to set the number of
#pixels per maze square so that each maze square is actually scaling X scaling
#pixels.  Generally, images of 300 x 300 to 600 x 600 pixels 
#are easiest to look at so for a maze of size 10x10, a scaling of 30-60
#is appropriate.

def main(argv):
    if (len(argv) < 4):
        print "Usage: maze_creator rows cols output_filename <image scaling>"
        return

    rows = int(argv[1])
    cols = int(argv[2])
    nameparts = argv[3].split('.')
    if (len(nameparts) != 2 or \
        (nameparts[1] != "txt" and nameparts[1] != "ppm")):
        print "You must specify either ASCII output (.txt filename) or PPM output (.ppm filename)"
        return
    creator = MazeCreator(rows, cols)
    maze = creator.create_maze([random.randint(1, rows-2), \
                                random.randint(1, cols-2)])
    if (nameparts[1] == "txt"):
        mazeIO.asciiIO.write_maze_to_ascii(argv[3], maze)
    else:
        scaling = 1
        if (argv > 4):
            try:
                scaling = int(argv[4])
            except:
                scaling = 1
        if (scaling <= 1):
            scaling = 1
        mazeIO.ppmIO.write_maze_to_ppm(argv[3], maze, scaling)

if __name__ == "__main__":
    main(sys.argv)
