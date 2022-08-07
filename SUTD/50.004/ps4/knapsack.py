import sys

def knapsack(items, maxweight):


    bestValueTable = [[0] * (maxweight + 1)
                  for i in xrange(len(items) + 1)]
    itemsToUse = []

    ############## WRITE YOUR CODE HERE #####################
    ############## You can also write your only code without using this file #####################

    itemsToUseTable = [[[]] * (maxweight + 1) for i in xrange(len(items) + 1)]
    
    for i in xrange(1, len(items) + 1):
        for j in xrange(1, maxweight + 1):
            if(j - items[i - 1][1] < 0):
                a = 0
            else:
                a = items[i - 1][0] + bestValueTable[i - 1][j - items[i - 1][1]]
            
            b = bestValueTable[i - 1][j]
            
            if(a > b):
                bestValueTable[i][j] = a
                itemsToUseTable[i][j] = itemsToUseTable[i - 1][j - items[i - 1][1]][:]
                itemsToUseTable[i][j].append(items[i - 1])
            else:
                bestValueTable[i][j] = b
                itemsToUseTable[i][j] = itemsToUseTable[i - 1][j][:]
                
    itemsToUse = itemsToUseTable[len(items)][maxweight][:]

    return bestValueTable[len(items)][maxweight], itemsToUse


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: knapsack.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()

    maxweight = int(lines[0])
    items = [map(int, line.split()) for line in lines[1:]]

    bestTotalValue, itemsToUse = knapsack(items, maxweight)

    print('Best possible total value: {0}'.format(bestTotalValue))
    print('Items:')
    for value, weight in itemsToUse:
        print('Value: {0}, Weight: {1}'.format(value, weight))
