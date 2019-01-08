import collections
import time
globalMax = -999


def sortCoordinates(coordinatesOfScooters):
    counts = collections.Counter(coordinatesOfScooters)
    global frequencyList,completeFrequencyList
    frequencyList = counts.most_common()
    print frequencyList
    for x in range(len(frequencyList)):
        k,v = frequencyList[x]
        x,y = k
        frequencyBoard[x][y] = v
    for x in range(len(frequencyBoard)):
        for y in range(len(frequencyBoard[x])):
            completeFrequencyList.append((x,y,frequencyBoard[x][y]))
    completeFrequencyList.sort(key=lambda x: x[2],reverse=True)



def calculateMax(board, frequencyBoard):
    localMax = 0
    for x in range(len(board)):
        for y in range(len(board)):
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


def solveNqueens(completeFrequencyList, boardSize, noOfOfficers, totalNoOfOfficers, board,i):
     global globalMax
     flag = False
     if(noOfOfficers == 0):
        for i in range(boardSize):
            print(board[i])
        localMax = calculateMax(board, frequencyBoard)
        if(localMax>=globalMax):
            globalMax = localMax
        print localMax
        return True
     if i>=len(completeFrequencyList):
        return True


     while i<len(completeFrequencyList):
        x,y,v = completeFrequencyList[i]
        if allowedPosition(x,y,board,boardSize):
            board[x][y]=1
            localMax = calculateMax(board,frequencyBoard)+calculateNetMax(completeFrequencyList,i+1,noOfOfficers-1)
            if globalMax<localMax:
                print globalMax
                flag = solveNqueens(completeFrequencyList,boardSize,noOfOfficers-1,totalNoOfOfficers,board,i+1)
            else:
                board[x][y] = 0
                return True
            board[x][y] = 0
        i = i+1
     return flag


#function for checking safe
def allowedPosition(row,col,board,boardSize):
    for x in range(boardSize):
        if board[x][col]==1:
            return False

    for y in range(boardSize):
        if board[row][y]==1:
            return False

    for i,j in zip(range(row,-1,-1), range(col,-1,-1)):
        if board[i][j] ==1:
            return False

    for i,j in zip(range(row,boardSize,1),range(col,boardSize,1)):
        if board[i][j]==1:
            return False

    for i,j in zip(range(row,-1,-1),range(col,boardSize,1)):
        if board[i][j]==1:
            return False

    for i,j in zip(range(row,boardSize,1),range(col,-1,-1)):
        if board[i][j]==1:
            return False

    return True


start = time.time()
#inputting file
inputFile = open("input1.txt","r")
boardSize = int(inputFile.readline())
noOfOfficers = totalNoOfOfficers = int(inputFile.readline())
noOfScooters = int(inputFile.readline())
noOfCoordinates = noOfScooters*12
coordinatesOfScooters = list()
frequencyBoard = [[0 for x in range(boardSize)] for y in range(boardSize)]
frequencyList = list(())
completeFrequencyList = list(())
for i in range(noOfCoordinates):
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
    print globalMax
    outputFile.close()


print (boardSize)
print (noOfOfficers)
print (noOfScooters)
print frequencyList
print frequencyBoard
print (globalMax)

end = time.time()

print end-start
