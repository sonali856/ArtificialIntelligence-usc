import collections
globalMax = -999


def sortCoordinates(coordinatesOfScooters):
    counts = collections.Counter(coordinatesOfScooters)
    global frequencyList
    frequencyList = counts.most_common()
    print frequencyList
    for x in range(len(frequencyList)):
        k,v = frequencyList[x]
        x,y = k
        frequencyBoard[int(x)][int(y)] = int(v)


def calculateMax(board, frequencyBoard):
    localMax = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if(board[x][y]==1):
                localMax +=frequencyBoard[x][y]

    return localMax


def solveNqueens(frequencyList, boardSize, noOfOfficers, board, col):
     global globalMax
     flag = False
     if(noOfOfficers == 0 ):
        localMax = 0
        #print (board)
        # for x in range(boardSize):
        #     for y in range(boardSize):
        #         if(board[x][y]==1):
        #             localMax +=frequencyBoard[x][y]
        localMax = calculateMax(board, frequencyBoard)
        if(localMax>=globalMax):
            globalMax = localMax

     if col>=boardSize :
        return True


     for row in range(boardSize):
            if allowedPosition(row,col,board,boardSize):
                board[row][col]=1
                flag = solveNqueens(frequencyList,boardSize,noOfOfficers-1,board,col+1) or flag
                board[row][col]=0


     return flag


#function for checking safe
def allowedPosition(row,col,board,boardSize):

    for y in range(boardSize):
        if board[row][y] == 1:
            return False
    for i,j in zip(range(row,-1,-1), range(col,-1,-1)):
        if board[i][j] ==1:
            return False
    for i,j in zip(range(row,boardSize,1),range(col,-1,-1)):
        if board[i][j]==1:
            return False
    return True




#inputting file
inputFile = open("input3.txt","r")
boardSize = int(inputFile.readline())
noOfOfficers = int(inputFile.readline())
noOfScooters = int(inputFile.readline())
noOfCoordinates = noOfScooters*12

coordinatesOfScooters = list()
frequencyBoard = [[0 for x in range(boardSize)] for y in range(boardSize)]
frequencyList = list(())
board = [[0 for x in range(boardSize)] for y in range(boardSize)]
for i in range(noOfCoordinates):
    x,y = inputFile.readline().rstrip().split(",")
    coordinatesOfScooters.append((x,y))

sortCoordinates(coordinatesOfScooters)

for col in range(boardSize):
    solveNqueens(frequencyList,boardSize,noOfOfficers,board,col)



print (boardSize)
print (noOfOfficers)
print (noOfScooters)
print frequencyList
print frequencyBoard
print (globalMax)
