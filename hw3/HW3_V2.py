import numpy
import copy

class Unit:

    def __init__(self,x,y):

        self.left_neighbour = (x,y) if y == 0 else (x,y-1)
        self.right_neighbour = (x,y) if y ==size_grid-1 else (x,y+1)
        self.up_neighbour = (x,y) if x ==0 else(x-1,y)
        self.down_neighbour =(x,y) if x==size_grid-1 else(x+1,y)
        self.curr_utility = 0
        self.prev_utility = -1
        self.direction = -1
        self.unit_position = (x,y)


    def set_direction(self,direction):
        self.direction = direction

    def __str__(self):
        return "Cell " + str(self.unit_position) + "\n\tU = " + str(self.current_utility) + "\n\tprev_U = " \
               + str(self.prev_utility) + "\n\tdir = " + str(self.direction)


def inputFile():
    #inputting the file

    file_input = open("input.txt","r")

    global size_grid
    size_grid= int(file_input.readline().rstrip())
    no_of_cars = int(file_input.readline().rstrip())
    no_of_obstacles = int(file_input.readline().rstrip())

    #making a list of tuples for obstacles
    #board = [[-1] * size_grid for x in xrange(size_grid)]
    board = [[Unit(y,x) for x in xrange(size_grid)] for y in xrange(size_grid)]
    obstacles_coordinates = list()
    car_coordinates_start = list()
    car_coordinates_final = list()
    car_combined_coordinates = list()



    #taking obstacles coordinates
    for i in xrange(no_of_obstacles):
        y,x = file_input.readline().split(",")
        obstacles_coordinates.append((int(x),int(y)))
        board[int(x)][int(y)].prev_utility-= int(100)

    print ()
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



def make_board_with_rewards(car_board,reward_board,target_coordinates):

    iterations_left = True

    while iterations_left:

        iterations_left = False
        delta = 0.0

        for i in xrange(size_grid):
            for j in xrange(size_grid):
                car_board[i][j].prev_utility = car_board[i][j].curr_utility

        car_board[target_coordinates[0]][target_coordinates[1]].prev_utility = 99

        # accessing the full board
        for i in xrange(size_grid):
            for j in xrange(size_grid):

                if i == target_coordinates[0] and j == target_coordinates[1]:
                    is_target = True
                else:
                    is_target = False

                up = car_board[i][j].up_neighbour
                down = car_board[i][j].down_neighbour
                left = car_board[i][j].left_neighbour
                right = car_board[i][j].right_neighbour

                up_value = 0.7*car_board[up[0]][up[1]].prev_utility +\
                             + 0.1*car_board[down[0]][down[1]].prev_utility + \
                            +0.1 * car_board[right[0]][right[1]].prev_utility+\
                             + 0.1*car_board[left[0]][left[1]].prev_utility

                down_value = 0.1*car_board[up[0]][up[1]].prev_utility +\
                             + 0.7*car_board[down[0]][down[1]].prev_utility + \
                             + 0.1 * car_board[right[0]][right[1]].prev_utility+\
                             + 0.1*car_board[left[0]][left[1]].prev_utility

                left_value = 0.1*car_board[up[0]][up[1]].prev_utility +\
                             + 0.1*car_board[down[0]][down[1]].prev_utility + \
                             + 0.1 * car_board[right[0]][right[1]].prev_utility+\
                             + 0.7*car_board[left[0]][left[1]].prev_utility

                right_value = 0.1*car_board[up[0]][up[1]].prev_utility +\
                             + 0.1*car_board[down[0]][down[1]].prev_utility + \
                              + 0.7 * car_board[right[0]][right[1]].prev_utility+\
                             + 0.1*car_board[left[0]][left[1]].prev_utility



                max_value = max(up_value,down_value,left_value,right_value)

                max_value *= 0.9
                max_value +=reward_board[i][j].prev_utility


                #to check for terminating condition, if optimality is in 0.1 range
                if (not is_target and abs((max_value - car_board[i][j].prev_utility)) > delta):
                    delta = abs(max_value-car_board[i][j].prev_utility)

                #updating max array and direction array
                car_board[i][j].curr_utility = max_value


        if(delta>(0.1*(1.0-0.9)/0.9)):
            iterations_left = True



    for i in xrange(size_grid):
        for j in xrange(size_grid):

            up = car_board[i][j].up_neighbour
            down = car_board[i][j].down_neighbour
            left = car_board[i][j].left_neighbour
            right = car_board[i][j].right_neighbour

            max_value = car_board[up[0]][up[1]].prev_utility
            direction = 0

            if car_board[down[0]][down[1]].prev_utility > max_value:
                max_value = car_board[down[0]][down[1]].prev_utility
                direction = 2

            if car_board[right[0]][right[1]].prev_utility > max_value:
                max_value = car_board[right[0]][right[1]].prev_utility
                direction = 3

            if car_board[left[0]][left[1]].prev_utility > max_value:
                max_value = car_board[left[0]][left[1]].prev_utility
                direction = 1

            car_board[i][j].direction = direction
                #up  - 0
                #down - 2
                #left - 1
                #right - 3

    return car_board


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

    #Calling value iteration
    final_car_board = make_board_with_rewards(unique_car_board,
                                              board,
                                              car_combined_coordinates[i][1])

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
           next_move = final_car_board[position[0]][position[1]].direction
           path +=str(position)+"|"
           if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        next_move = turn_right(turn_right(next_move))
                    else:
                        next_move = turn_right(next_move)
                else:
                    next_move = turn_left(next_move)

           up = final_car_board[position[0]][position[1]].up_neighbour
           down = final_car_board[position[0]][position[1]].down_neighbour
           left = final_car_board[position[0]][position[1]].left_neighbour
           right = final_car_board[position[0]][position[1]].right_neighbour

           if next_move == 0:
                position = up
           elif next_move == 1:
                position = left
           elif next_move == 2:
                position = down
           elif next_move == 3:
                position = right

           utility_value += board[position[0]][position[1]].prev_utility
           k += 1


        result += (utility_value+100)

    result /= 10

    result_output_file += str((int(numpy.floor(result))))+"\n"

output_file  = open("output.txt","w");
output_file.write(result_output_file)


