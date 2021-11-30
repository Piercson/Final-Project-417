import heapq
from helpers import *
import copy
def move(loc, dir):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]

def get_new_state(o_loc, n_loc, og_state):
    new_state = copy.deepcopy(og_state)
    temp = new_state[o_loc[0]][o_loc[1]]
    new_state[o_loc[0]][o_loc[1]] = new_state[n_loc[0]][n_loc[1]]
    new_state[n_loc[0]][n_loc[1]] = temp
    return new_state

def compute_heuristic(state, goal_state):
    g = 0
    for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == goal_state[i][j]:
                    g += 1
    return len(state) ** 2 - g

def compute_heuristic_matt(state,goal_state):
    goal = dict()
    curr = dict()
    width = len(state)
    for i in range(0,width):
        for j in range(0,width):
            goal[goal_state[i][j]] = (i,j)
            curr[state[i][j]] = (i,j)
    sum_arr = []
    for i in range(0,width**2):
        g = goal[i]
        s = curr[i]
        sum_arr.append(abs(g[0]-s[0]) + abs(g[1]-s[1]))
    return sum(sum_arr)
            
def get_path(goal_node):
    path = []
    curr = goal_node
    while curr is not None:
        path.append(curr['state'])
        curr = curr['parent']
    path.reverse()
    return path

def compare_nodes(n1, n2):
    """Return true is n1 is better than n2."""
    return n1['g_val'] + n1['cost'] < n2['g_val'] + n2['cost']

class Astar(object):
    """The high-level search of CBS."""

    def __init__(self, goal):
        self.goal = goal

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost']+node['g_val'], self.num_of_generated, node))
        # print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, id, node = heapq.heappop(self.open_list)
        # print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, state, start_loc):
        
        #self.start_time = timer.time()
        closed_list = dict()
        root = {'loc': start_loc,'parent': None,'state': state,'g_val': compute_heuristic_matt(state,self.goal),'cost': 0}
        self.push_node(root)
        closed_list[(root['loc'],matrix_to_int(state))] = root
        while len(self.open_list) > 0:
            curr = self.pop_node()
            # check if goal state
            if curr['state'] == self.goal:
                return get_path(curr)
            for dir in range(4):
                child_loc = move(curr['loc'], dir)
                try:
                    curr['state'][child_loc[0]][child_loc[1]]
                except IndexError:
                    continue
                new_state = get_new_state(curr['loc'], child_loc, curr['state'])
                child = {'loc': child_loc,
                         'parent': curr,
                         'state': new_state,
                         'g_val': compute_heuristic_matt(new_state,self.goal),
                         'cost': curr['cost'] + 1}
                if (child['loc'],matrix_to_int(child['state'])) in closed_list:
                    existing_node = closed_list[(child['loc'],matrix_to_int(child['state']))]
                    if compare_nodes(child, existing_node):
                        closed_list[(child['loc'],matrix_to_int(child['state']))] = child
                        self.push_node(child)
                else:
                    closed_list[(child['loc'],matrix_to_int(child['state']))] = child
                    self.push_node(child)
        print('END',len(self.open_list))
        return None
        