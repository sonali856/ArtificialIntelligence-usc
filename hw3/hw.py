import copy

import numpy as np


def turn_left(str):
    if str == 'n':
        return 'w'
    if str == 'w':
        return 's'
    if str == 's':
        return 'e'
    if str == 'e':
        return 'n'


def turn_right(str):
    if str == 'n':
        return 'e'
    if str == 'e':
        return 's'
    if str == 's':
        return 'w'
    if str == 'w':
        return 'n'


infile = open('input/input1.txt', 'r')
read1 = infile.read()
infile.close()
lines = read1.split('\n')
outfile = open('output.txt', 'w')
x = 0
no = int(lines[x])
orig = [[-1.0]*no for h3 in range(0,no)]
grid = [[0.0]*no for h2 in range(0,no)]
dir = [['N']*no for k in range(0,no)]

x += 1
c = int(lines[x])
x += 1
o = int(lines[x])
x += 1
for i in range(x,o+x):
    strr = lines[i].split(',')
    xx = int(strr[0])
    yy = int(strr[1])
    orig[xx][yy]=-101.0
    x+=1

basic = copy.deepcopy(grid)
prev = copy.deepcopy(grid)

for car in range(x,x+c):
    print('car',car-x)
    strr1 = lines[car].split(',')
    strr2 = lines[car+c].split(',')
    xx = int(strr1[0])
    yy = int(strr1[1])
    x2 = int(strr2[0])
    y2 = int(strr2[1])
    orig[x2][y2] = 99.0
    # print(prev,grid,orig)
    flag = 1
    while flag:
        delta = 0.0
        flag = 0
        prev = copy.deepcopy(grid)
        # print(prev, grid, orig)
        for i in range(0, no):
            for j in range(0, no):
                s = 0.0
                n = 0.0
                e = 0.0
                w = 0.0

                # else: consider the same block again
                if i != 0:
                    s = grid[i - 1][j]
                else:
                    s = grid[i][j]
                if j != 0:
                    w = grid[i][j - 1]
                else:
                    w = grid[i][j]
                if j < no - 1:
                    e = grid[i][j + 1]
                else:
                    e = grid[i][j]
                if i < no - 1:
                    n = grid[i + 1][j]
                else:
                    n = grid[i][j]
                # calculate the value considering each side as the best decision
                n1 = n * 0.7 + (s + e + w) * 0.1
                s1 = s * 0.7 + (n + e + w) * 0.1
                e1 = e * 0.7 + (s + n + w) * 0.1
                w1 = w * 0.7 + (s + e + n) * 0.1
                maxx = max(n1, s1, e1, w1)
                # grid: current grid initial value: 0
                # prev: prev grid initial value: 0
                # orig: reward grid initial value: -1,-101(no destination till now)

                if i!=x2 or j!=y2:
                    grid[i][j] = orig[i][j] + 0.9 * maxx
                if abs((grid[i][j] - prev[i][j])) > delta:
                    delta = abs((grid[i][j] - prev[i][j]))
        if delta > float(0.1 * (1 - 0.9)) / 0.9:
            flag = 1
#  DIRECTION

    #
    # for i in range(0,no):
    #     print(grid[i])
    for i in range(0,no):
        for j in range(0,no):
            if i==x2 and j==y2:
                dir[i][j]='g'
                continue
            maxx = float('-inf')
            if i!=0 and maxx<prev[i-1][j]:
                maxx = prev[i-1][j]
                dir[i][j] = 'n'
            if i < no - 1 and maxx<prev[i+1][j]:
                maxx = prev[i+1][j]
                dir[i][j] = 's'
            if j < no - 1 and maxx<prev[i][j+1]:
                maxx = prev[i][j + 1]
                dir[i][j] = 'e'
            if j != 0 and maxx<prev[i][j-1]:
                maxx = prev[i][j - 1]
                dir[i][j] = 'w'

    # for i in range(0,no):
    #     print(dir[i])

    maxx = float('-inf')
    result=0
    for m in range(0,10):
        # print('sim',m)
        posx = xx
        posy = yy
        np.random.seed(m)
        swerve = np.random.random_sample(1000000)
        k = 0
        ans = 0
        if posx==x2 and posy==y2:
            ans = 100
        while posx!=x2 or posy!=y2:
            move = dir[posx][posy]
            # print('init',posx,posy,move,k,swerve[k])
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_left(turn_left(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            k += 1
            # print('later',move)
            if move=='s':
                if posx!=no-1:
                    posx+=1
                # print('(1,0)')
            elif move=='n':
                if posx!=0:
                    posx-=1
                # print('(-1,0)')
            elif move=='w':
                if posy!=0:
                    posy-=1
                # print('(0,-1)')
            else:
                if posy!=no-1:
                    posy+=1
                # print('(0,1)')
            ans+=orig[posx][posy]
        result+=ans
    print('fin', np.floor(result/10))
    outfile.write(str(int(np.floor(result/10))))
    if car!=x+c-1:
        outfile.write("\n")

    # for j in range(10):
    #     pos = cars[i]
    #     np.random.seed(j + 1)
    #     swerve = np.random.random_sample(1000000)
    #     k = 0
    #     while pos != ends[i]:
    #         move = policies[i][pos]
    #         if swerve[k] > 0.7:
    #             if swerve[k] > 0.8:
    #                 if swerve[k] > 0.9:
    #                     move = turn_left(turn_left(move))
    #                 else:
    #                     move = turn_left(move)
    #             else:
    #                 move = turn_right(move)
    #             k += 1


    grid = copy.deepcopy(basic)
    orig[x2][y2] = -1
    # value iteration


