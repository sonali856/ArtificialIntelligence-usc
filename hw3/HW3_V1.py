import numpy
import copy

class Unit:

    def __init__(self,x,y,prev_utility,direction):

        self.left_neighbour = (x,y) if y==0 else (x,y-1)
        self.right_neighbour = (x,y) if y ==size_grid else (x,y+1)
        self.up_neighbour = (x,y) if x ==0 else(x-1,y)
        self.down_neighbour =(x,y) if x==size_grid else(x+1,y)
        self.current_utility = curr_utility
        self.prev_utility = prev_utility
        self.direction = direction
        self.unit_position = (x,y)


    def set_direction(self,direction):
        self.direction = direction


def inputFile():
    #inputting the file
    file_input = open("inputNew.txt","r")

    size_grid = int(file_input.readline().rstrip())
    no_of_cars = int(file_input.readline().rstrip())
    no_of_obstacles = int(file_input.readline().rstrip())

    #making a list of tuples for obstacles
    board = [[-1] * size_grid for x in xrange(size_grid)]
    obstacles_coordinates = list()
    car_coordinates_start = list()
    car_coordinates_final = list()
    car_combined_coordinates = list()



    #taking obstacles coordinates
    for i in xrange(no_of_obstacles):
        y,x = file_input.readline().split(",")
        obstacles_coordinates.append((int(x),int(y)))
        board[int(x)][int(y)]= board[int(x)][int(y)] - int(100)



    #taking start coordinates of car path
    for i in xrange(no_of_cars):
        y_start,x_start = file_input.readline().split(",")
        car_coordinates_start.append((int(x_start),int(y_start)))

    #taking final coordinates of car path
    for i in xrange(no_of_cars):
        y_final,x_final = file_input.readline().split(",")
        car_coordinates_final.append((int(x_final), int(y_final)))
        car_combined_coordinates.append((car_coordinates_start[i],car_coordinates_final[i]))


    file_input.close()


    return board,size_grid,car_combined_coordinates,no_of_cars


def show_grid_with_utility(grid):
    for row in xrange(size_grid):
        grid_row = ""
        for col in xrange(size_grid):
            if grid[row][col] ==0:
                x = 'U'
            if grid[row][col] ==1:
                x = 'L'
            if grid[row][col] ==3:
                x = 'R'
            if grid[row][col] ==2:
                x = 'D'
            grid_row += str(x) + " | "
        print grid_row
    print ""

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


def make_direction_array(direction_array,max_array):

    for i in xrange(size_grid):
        for j in xrange(size_grid):

            up, down, left, right = get_neighbours(i, j, size_grid)

            max_value = max_array




def make_board_with_rewards(reward_board,prev_max_values_board,direction_array,max_array,is_target,target_coordinates):

    iterations_left = True

    while iterations_left:

        iterations_left = False

        # accessing the full board
        for i in xrange(size_grid):
            for j in xrange(size_grid):

                if i == target_coordinates[0] and j == target_coordinates[1]:
                    is_target = True
                else:
                    is_target = False


                up,down,left,right = get_neighbours(i,j,size_grid)


                up_value = 0.9*0.7*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]] +\
                             + 0.9*0.1*prev_max_values_board[right[0]][right[1]]

                down_value = 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.7*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]]+\
                             + 0.9*0.1*prev_max_values_board[right[0]][right[1]]

                left_value = 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.7*prev_max_values_board[left[0]][left[1]]+\
                             +0.9*0.1*prev_max_values_board[right[0]][right[1]]

                right_value = 0.9*0.1*prev_max_values_board[up[0]][up[1]] +\
                             + 0.9*0.1*prev_max_values_board[down[0]][down[1]] +\
                             + 0.9*0.1*prev_max_values_board[left[0]][left[1]] +\
                             + 0.9*0.7*prev_max_values_board[right[0]][right[1]]


                max_value,direction = calculate_max(up_value,down_value,left_value,right_value)

               # max_value *= 0.9
                max_value +=reward_board[i][j]


                #to check for terminating condition, if optimality is in 0.1 range
                if (not is_target and abs((max_value - prev_max_values_board[i][j])/ prev_max_values_board[i][j]) > 0.01):
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


    max_values_board[car_combined_coordinates[i][1][0]][car_combined_coordinates[i][1][1]] = 100

    #print("Direction Array "+" ".join(str(direction_array)))
    print(" Car - "+str(i))
    show_grid_with_utility(direction_array)



    # simulation
    result = 0.0
    car_start_coordinates = car_combined_coordinates[i][0]
    car_end_coordinates = car_combined_coordinates[i][1]

    for x in xrange(10):
        numpy.random.seed(x)
        swerve = numpy.random.random_sample(1000000)
        k = 0
        utility_value = 0
        path = ""
        position = car_start_coordinates

        while position != car_end_coordinates:
           next_move = direction_array[position[0]][position[1]]
           path +=str(position)+"|"
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

        print (path+"\n")

        result += (utility_value+100)# doubt


    result /= 10

    result_output_file += str((int(numpy.floor(result))))+"\n"



output_file  = open("output.txt","w");
output_file.write(result_output_file)


#for each car , make copy of board make changes to utility value according to the board, next find directions to the board


