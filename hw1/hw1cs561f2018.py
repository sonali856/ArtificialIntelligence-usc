globalMax = -999

def sortCoordinates(coordinatesOfScooters):

    for i in xrange(len(coordinatesOfScooters)):
        x,y = coordinatesOfScooters[i]
        frequencyBoard[x][y]+=1
    for x in xrange(len(frequencyBoard)):
        for y in xrange(len(frequencyBoard[x])):
            completeFrequencyList.append((x,y,frequencyBoard[x][y]))
    completeFrequencyList.sort(key=lambda x: x[2],reverse=True)



def calculateMax(board, frequencyBoard):
    localMax = 0
    for x in xrange(len(board)):
        for y in xrange(len(board)):
            if(board[x][y]==1):
                localMax +=frequencyBoard[x][y]

    return localMax


def calculateNetMax(completeFrequencyList,i,noOfOfficers):
    sum = 0
    while(noOfOfficers!=0 and i<len(completeFrequencyList)):
        x,y,v = completeFrequencyList[i]
        sum +=v
        noOfOfficers-=1
        i = i+1
    return sum


def solveNqueens(completeFrequencyList, boardSize, noOfOfficers, board,i):
     global globalMax
     flag = False
     if(noOfOfficers == 0):
        localMax = calculateMax(board, frequencyBoard)
        if(localMax>=globalMax):
            globalMax = localMax
        return True
     if i>=len(completeFrequencyList):
        return True


     while i<len(completeFrequencyList):
        x,y,v = completeFrequencyList[i]
        if allowedPosition(x,y,board,boardSize):
            board[x][y]=1
            localMax = calculateMax(board,frequencyBoard)+calculateNetMax(completeFrequencyList,i+1,noOfOfficers-1)
            if globalMax<localMax:
                flag = solveNqueens(completeFrequencyList,boardSize,noOfOfficers-1,board,i+1)
            else:
                board[x][y] = 0
                return True
            board[x][y] = 0
        i = i+1
     return flag


#function for checking safe
def allowedPosition(row,col,board,boardSize):
    for x in xrange(boardSize):
        if board[x][col]==1:
            return False

    for y in xrange(boardSize):
        if board[row][y]==1:
            return False

    for i,j in zip(xrange(row,-1,-1), xrange(col,-1,-1)):
        if board[i][j] ==1:
            return False

    for i,j in zip(xrange(row,boardSize,1),xrange(col,boardSize,1)):
        if board[i][j]==1:
            return False

    for i,j in zip(xrange(row,-1,-1),xrange(col,boardSize,1)):
        if board[i][j]==1:
            return False

    for i,j in zip(xrange(row,boardSize,1),xrange(col,-1,-1)):
        if board[i][j]==1:
            return False

    return True



#inputting file
inputFile = open("input1.txt","r")
boardSize = int(inputFile.readline())
noOfOfficers = totalNoOfOfficers = int(inputFile.readline())
noOfScooters = int(inputFile.readline())
noOfCoordinates = noOfScooters*12
coordinatesOfScooters = list()
frequencyBoard = [[0 for x in xrange(boardSize)] for y in xrange(boardSize)]
frequencyList = list(())
completeFrequencyList = list(())
for i in xrange(noOfCoordinates):
    x,y = inputFile.readline().rstrip().split(",")
    coordinatesOfScooters.append((int(x),int(y)))

inputFile.close()

sortCoordinates(coordinatesOfScooters)

if noOfScooters == 0:
    outputFile = open("output.txt", "w")
    outputFile.write(str(0))
    outputFile.close()
else:
    for i in xrange(len(completeFrequencyList)):
        board = [[0 for x in xrange(boardSize)] for y in xrange(boardSize)]
        solveNqueens(completeFrequencyList,boardSize,noOfOfficers,board,i)

    outputFile = open("output.txt","w")
    outputFile.write(str(globalMax))
    outputFile.close()


