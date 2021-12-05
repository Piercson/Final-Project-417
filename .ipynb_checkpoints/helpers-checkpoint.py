import numpy as np
from random import randint
import copy
from solvers import move, get_new_state
# BAD STATE
# 0,6,5,4,3,1,8,2,7
def get_random_state(goal_state,num_swaps):
    new_state = copy.deepcopy(goal_state)
    loc_0 = get_location(new_state,0)
    size = len(goal_state)
    for i in range(num_swaps):
        while(1):
            new_loc = move(loc_0,randint(0, 3))
            if new_loc[0] < 0 or new_loc[1] < 0 or new_loc[0] >= size or new_loc[1] >= size:
                continue
            new_state = get_new_state(loc_0, new_loc, new_state)
            loc_0 = new_loc
            break
    return new_state

def arr_to_matrix(arr,m_width):
    M = []
    for i in range(m_width):
        l_b = m_width * i
        u_b = m_width * (i+1)
        M.append(arr[l_b:u_b])
    return M

def matrix_to_int(M):
    flat = np.array(M).flatten()
    x = ""
    for num in flat:
        x += (str(num))
    return int(x)
def get_location(M,value):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == value:
                return (i,j)
            
def pretty_print(matrix):
    print("_______")
    for row in matrix:
        for entry in row:
            print(entry, " ",end="")
        print("")
    print("_______")