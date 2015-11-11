import maze

class ppmIO:

    @staticmethod
    def __get_raster(maze, scaling):
        
        #'W' always indicates black square
        #'S' or 'O' indicates a white square
        #'B' indicates start and 'E' indicates end
        
        raster = []
        for row in maze.matrix:
            rasterrow = []
            for entry in row:
                if (entry == 'W'):
                    pixel = chr(0) + chr(0) + chr(0)
                elif (entry == 'E'):
                    pixel = chr(0) + chr(255) + chr(0)
                elif (entry == 'B'):
                    pixel = chr(0) + chr(0) + chr(255)
                else:
                    pixel = chr(255) + chr(255) + chr(255)
                for i in range(scaling):
                    rasterrow.append(pixel)
            for i in range(scaling):
                raster.append(rasterrow)
        return raster

    @staticmethod
    def __add_points_to_raster(raster, maze, points, color, scaling):

        for point in points:
            if (maze.matrix[point[0]][point[1]] == 'W' or \
                maze.matrix[point[0]][point[1]] == 'B' or \
                maze.matrix[point[0]][point[1]] == 'E'):
                continue
            #overwrite all these pixels with the new color
            for i in range(point[0]*scaling, (point[0]+1)*scaling):
                for j in range(point[1]*scaling, (point[1]+1)*scaling):
                    raster[i][j] = color

    @staticmethod
    def __write_raster(filename, raster, maze, scaling):
        outfile = open(filename, 'wb')

        #write the PPM header (this is ASCII)
        #P6 is PPM "magic number", followed by rows, columns, 
        #and maximum pixel value
        outfile.write("P6\n" + str(maze.cols*scaling) + " " \
                      + str(maze.rows*scaling) + "\n" \
                      + str(255) + "\n")
        for row in raster:
            for pixel in row:
                outfile.write(pixel)
        outfile.close()

    @staticmethod
    def write_maze_to_ppm(filename, maze, scaling=1): 
        raster = ppmIO.__get_raster(maze, scaling)
        ppmIO.__write_raster(filename, raster, maze, scaling)

    @staticmethod
    def write_path_to_ppm(filename, maze, path, scaling=1):
        raster = ppmIO.__get_raster(maze, scaling)
        red = chr(255) + chr(0) + chr(0)
        ppmIO.__add_points_to_raster(raster, maze, path, red, scaling)
        ppmIO.__write_raster(filename, raster, maze, scaling)
    
    @staticmethod
    def write_visited_to_ppm(filename, maze, visited, path, scaling=1):
        raster = ppmIO.__get_raster(maze, scaling)
        purple = chr(255) + chr(0) + chr(255)
        ppmIO.__add_points_to_raster(raster, maze, visited, purple, scaling)
        red = chr(255) + chr(0) + chr(0)
        ppmIO.__add_points_to_raster(raster, maze, path, red, scaling)
        ppmIO.__write_raster(filename, raster, maze, scaling)

            
    @staticmethod
    def read_maze_from_ppm(filename, scaling=1):
        infile = open(filename, 'rb')
        
        #read in the header information
        numstrings = 0
        header = []
        while (numstrings < 4):
            line = infile.readline()
            splits = line.split()
            numstrings += len(splits)
            header.extend(splits)
        ncols = int(header[1])/scaling
        nrows = int(header[2])/scaling
        colors = int(header[3])

        #this is the raster in binary
        raster = infile.read()
        infile.close()

        matrix = []
        pixel = 0
        row = 0
        col = 0
        currrow = []
        start = []
        end = []
        while (pixel < len(raster)):
            rval = ord(raster[pixel])
            pixel += 1
            gval = ord(raster[pixel])
            pixel += 1
            bval = ord(raster[pixel])
            pixel += 1
            if (rval > 0 or bval > 0 or gval > 0):
                if (bval > 0 and (gval == 0 and rval == 0)):
                    #starting point
                    currrow.append('B')
                    start = [row, col]
                elif (gval > 0 and (bval == 0 and rval == 0)):
                    currrow.append('E')
                    end = [row, col]
                else:
                    currrow.append('O')
            else:
                currrow.append('W')
            pixel += 3*(scaling-1)
            col += 1
            if (col == ncols):
                matrix.append(currrow)
                row += 1
                currrow = []
                pixel += 3*scaling*ncols*(scaling-1)
                col = 0

        return maze.Maze(matrix, start, end)

        

class asciiIO:
    
    @staticmethod
    def write_maze_to_ascii(filename, maze):
        
        outfile = open(filename, 'w')
        
        for row in maze.matrix:
            for entry in row:
                outfile.write(entry + " ")
            outfile.write("\n")
        outfile.close()
        
    @staticmethod
    def write_path_to_ascii(filename, maze, path):
        oufile = open(filename, 'w')
        rows = 0
        cols = 0
        for row in maze.matrix:
            for entry in row:
                
                if ([rows, cols] in path and (entry != 'W' and \
                                              entry != 'B' and \
                                              entry != 'E')):
                    outfile.write("X ")
                else:
                    outfile.write(entry + " ")
                cols += 1
            rows += 1
            outfile.write("\n")

        outfile.close()

    @staticmethod
    def write_visited_to_ascii(filename, maze, visited, path):
        outfile = open(filename, 'w')
        rows = 0
        cols = 0
        for row in maze.matrix:
            for entry in row:
                if ([rows, cols] in visited and (entry != 'W' and \
                                                 entry != 'B' and \
                                                 entry != 'E')):
                    if ([rows, cols] in path):
                        outfile.write("X ")
                    else:
                        outfile.write("V ")
                else:
                    if (entry == 'S' or entry == 'O'):
                        outfile.write("O ")
                    else:
                        outfile.write(entry + " ")
                cols += 1
            rows += 1
            cols = 0
            outfile.write("\n")

        outfile.close()
        


    @staticmethod
    def read_maze_from_ascii(filename):
        
        infile = open(filename, 'r')

        matrix = []
        start = []
        end = []
        for line in infile:
            row = line.split()
            col = -1
            for entry in row:
                col += 1
                if (entry == 'W' or entry == 'O'):
                    continue
                if (entry == 'B'):
                    start = [len(matrix), col]
                elif (entry == 'E'):
                    end = [len(matrix), col]
                else:
                    #anything else is interpreted as an open square
                    row[col] = 'O'
            matrix.append(row)

        return maze.Maze(matrix, start, end)

