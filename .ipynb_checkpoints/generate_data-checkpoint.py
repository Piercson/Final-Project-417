from solvers import *
from helpers import get_location
import pandas as pd
import random
import copy

def get_random_state(goal_state,num_swaps):
    new_state = copy.deepcopy(goal_state)
    loc_0 = get_location(new_state,0)
    size = len(goal_state)
    for i in range(num_swaps):
        while(1):
            new_loc = move(loc_0,random.randint(0, 3))
            if new_loc[0] < 0 or new_loc[1] < 0 or new_loc[0] >= size or new_loc[1] >= size:
                continue
            new_state = get_new_state(loc_0, new_loc, new_state)
            loc_0 = new_loc
            break
    return new_state

def get_data(solvers,num_states,num_shuffles,goal_state):
    data = pd.DataFrame(
        columns=['name','expanded','generated','sol_length','time','state'])
    goal = int_to_matrix(goal_state)
    lst_states = []
    i = 0
    while len(lst_states) < num_states:
        random.seed(i)
        state = get_random_state(goal,num_shuffles)
        int_state = matrix_to_int(state)
        if int_state in lst_states:
            continue
        lst_states.append(int_state)
        for solver_type in solvers:
            solver = solver_type(goal)
            sol = solver.find_solution(state,get_location(state,0))
            expanded = solver.num_of_expanded
            generated = solver.num_of_generated
            length = len(sol)
            time = solver.CPU_time
            row = pd.DataFrame([[
                solver.name,
                expanded,
                generated,
                length,
                time,
                int_state]],
                columns=['name','expanded','generated','sol_length','time','state'])
            data = pd.concat([data,row])
        i+=1
    return data