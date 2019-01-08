import numpy
import copy

DEBUG = True
def dPrintf(arg):
    if DEBUG:
        print str(arg)

def inputFile():
    #inputting the file
    file_input = open("input2.txt","r")

    size_grid = int(file_input.readline().rstrip())
    no_of_cars = int(file_input.readline().rstrip())
    no_of_obstacles = int(file_input.readline().rstrip())

    #making a list of tuples for obstacles
    board = [[-1] * size_grid for x in xrange(size_grid)]
    obstacles_coordinates = list()
    car_coordinates_start = list()
    car_coordinates_final = list()
    car_combined_coordinates = list()

    dPrintf("SIZE OF GRID "+str(size_grid))
    dPrintf("NO OF CARS "+str(no_of_cars))
    dPrintf("NO OF OBSTACLES "+str(no_of_obstacles))

    #taking obstacles coordinates
    for i in xrange(no_of_obstacles):
        y,x = file_input.readline().split(",")
        obstacles_coordinates.append((int(x),int(y)))
        board[int(x)][int(y)]= board[int(x)][int(y)] - int(100)

    dPrintf("OBSTACLES COORDINATES "+" ".join(str(obstacles_coordinates)))

    #taking start coordinates of car path
    for i in xrange(no_of_cars):
        y_start,x_start = file_input.readline().split(",")
        car_coordinates_start.append((int(x_start),int(y_start)))

    dPrintf("CAR COORDINATES START"+" ".join(str(car_coordinates_start)))
    #taking final coordinates of car path
    for i in xrange(no_of_cars):
        y_final,x_final = file_input.readline().split(",")
        car_coordinates_final.append((int(x_final), int(y_final)))
        car_combined_coordinates.append((car_coordinates_start[i],car_coordinates_final[i]))

    dPrintf("CAR COORDINATES FINAL"+" ".join(str(car_coordinates_final)))

    file_input.close()

    dPrintf("CAR COORDINATES "+" ".join(str(car_combined_coordinates)))

    #printing board
    dPrintf("BOARD UTILITIES WITH OBSTACLES" + " ".join(str(board)))

    return board,size_grid,car_combined_coordinates,no_of_cars




#calculates the max value of all the utilities
def calculate_max(up_value,down_value,left_value,right_value):

    #UP DOWN RIGHT LEFT
    max = up_value
    direction = 0

    if(down_value>max):
        max = down_value
        direction = 2

    if (right_value > max):
        max = right_value
        direction = 3

    if(left_value>max):
        max = left_value
        direction = 1


    return max,direction


def get_neighbours(i,j,size_grid):

    if i-1>=0 and j>=0:
        up = (i-1,j)
    else:
        up = (i,j)

    if i+1<size_grid and j<size_grid:
        down = (i+1,j)
    else:
        down = (i,j)

    if j-1>=0 and i>=0:
        left = (i,j-1)
    else:
        left = (i,j)

    if j+1<size_grid and i<size_grid:
        right = (i,j+1)
    else:
        right = (i,j)

    return up,down,left,right


def make_board_with_rewards(reward_board,prev_max_values_board,direction_array,max_array,is_target,target_coordinates):

    iterations_left = True

    while iterations_left:

        iterations_left = False

        dPrintf("Prev Board")
        dPrintf(" ".join(str(prev_max_values_board)))
        # accessing the full board
        for i in xrange(size_grid):
            for j in xrange(size_grid):

                dPrintf(str(i == target_coordinates[0] )+str(j == target_coordinates[1]))

                if i == target_coordinates[0] and j == target_coordinates[1]:
                    is_target = True
                else:
                    is_target = False


                up,down,left,right = get_neighbours(i,j,size_grid)
                dPrintf("i j "+str(i)+str(j))
                dPrintf(" Up "+str(up)+" Down "+str(down)+"Left "+str(left)+"Right "+str(right))
                dPrintf(" Reward board")
                dPrintf(" ".join(str(reward_board)))

                up_value = reward_board[i][j] + 0.9*0.7*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]] +\
                             + 0.9*0.1*prev_max_values_board[right[0]][right[1]]

                down_value = reward_board[i][j] + 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.7*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]]+\
                             + 0.9*0.1*prev_max_values_board[right[0]][right[1]]

                left_value = reward_board[i][j] + 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.7*prev_max_values_board[left[0]][left[1]]+\
                             + 0.9*0.1*prev_max_values_board[right[0]][right[1]]

                right_value = reward_board[i][j] + 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]] +\
                             + 0.9*0.7*prev_max_values_board[right[0]][right[1]]

                dPrintf("Values  up "+str(up_value)+" down "+str(down_value)+" left "+str(left_value)+" right "+str(right_value))

                max_value,direction = calculate_max(up_value,down_value,left_value,right_value)

                dPrintf(" max "+str(max_value)+" direction"+str(direction))

                #to check for terminating condition, if optimality is in 0.1 range
                if (not is_target and abs((max_value - prev_max_values_board[i][j])/ prev_max_values_board[i][j]) > 0.1):
                    iterations_left = True


                #updating max array and direction array
                max_array[i][j] = max_value
                direction_array[i][j] = direction




                #up  - 0
                #down - 2
                #left - 1
                #right - 3


        for i in xrange(size_grid):
            for j in xrange(size_grid):
                prev_max_values_board[i][j] = max_array[i][j]
                if i == target_coordinates[0] and j == target_coordinates[1]:
                    prev_max_values_board[i][j] = 100

        dPrintf("Direction Array *********************" + " ".join(str(direction_array)))


    return direction_array,max_array


def turn_left(direction):
    return (direction+1)%4

def turn_right(direction):
    return (direction+3)%4


board,size_grid,car_combined_coordinates,no_of_cars = inputFile()

result_output_file = ""


for i in xrange(no_of_cars):

    #making board
    unique_car_board = copy.deepcopy(board)
    direction_array = [[0] * size_grid for x in xrange(size_grid)]
    max_array = [[0] * size_grid for x in xrange(size_grid)]
    prev_max_values_board = copy.deepcopy(unique_car_board)

    #Calling value iteration
    direction_array,max_values_board = make_board_with_rewards(unique_car_board,
                                                               prev_max_values_board,
                                                               direction_array,
                                                               max_array,
                                                               True,
                                                               car_combined_coordinates[i][1])

    dPrintf(" Car with start "+str(car_combined_coordinates[i][0])+" end "+str(car_combined_coordinates[i][1]))
    dPrintf(" Direction Board " + " ".join(str(direction_array)))

    max_values_board[car_combined_coordinates[i][1][0]][car_combined_coordinates[i][1][1]] = 100

    dPrintf(" Max Values" + " ".join(str(max_values_board)))

    # simulation
    result = 0.0
    path_taken = ""
    car_start_coordinates = car_combined_coordinates[i][0]
    car_end_coordinates = car_combined_coordinates[i][1]

    for x in xrange(10):
        numpy.random.seed(x)
        swerve = numpy.random.random_sample(1000000)
        k = 0
        utility_value = 0
        position = car_start_coordinates
        dPrintf("Position car is at start " +str(position))
        dPrintf("Board" + " ".join(str(board)))


        while position != car_end_coordinates:
            dPrintf("Position of car" + str(position))
           # dPrintf(" Finding next move at "+str(position[0])+" "+str(position[1]))
            next_move = direction_array[position[0]][position[1]]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        next_move = turn_left(turn_left(next_move))
                    else:
                        next_move = turn_right(next_move)
                else:
                    next_move = turn_left(next_move)

            up, down, left, right = get_neighbours(position[0],position[1],size_grid)

            if next_move == 0:
                position = up
            elif next_move == 1:
                position = left
            elif next_move == 2:
                position = down
            elif next_move == 3:
                position = right

            utility_value += board[position[0]][position[1]]
            k += 1



            path_taken = "(" + str(position[0]) + "," + str(position[1]) + ")||"

        dPrintf(" Utility Value = " + str(utility_value+100))
        result += (utility_value+100)# doubt



    dPrintf("Path Taken"+str(path_taken))
    result /= 10

    result_output_file += str((int(numpy.floor(result))))+"\n"


dPrintf(" Result "+result_output_file)

output_file  = open("output.txt","w");
output_file.write(result_output_file)


#for each car , make copy of board make changes to utility value according to the board, next find directions to the board




