import heapq
from helpers import *
import copy
import time as timer
def move(loc, dir):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]
# swaps postions o_loc and n_loc in og_state
# Return a new state of the swapped positions
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
    for i in range(1,width**2):
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
    return n1['h_val'] + n1['cost'] < n2['h_val'] + n2['cost']

class Astar(object):
    """The high-level search of CBS."""

    def __init__(self, goal):
        self.goal = goal
        self.name = "A Star"
        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost']+node['h_val'], self.num_of_generated, node))
        # print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, id, node = heapq.heappop(self.open_list)
        # print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, state, start_loc):
        
        self.start_time = timer.time()
        size = len(state)
        closed_list = dict()
        root = {'loc': start_loc,'parent': None,'state': state,'h_val': compute_heuristic_matt(state,self.goal),'cost': 0}
        self.push_node(root)
        closed_list[(root['loc'],matrix_to_int(state))] = root
        while len(self.open_list) > 0:
            curr = self.pop_node()
            # check if goal state
            if curr['state'] == self.goal:
                self.CPU_time = timer.time() - self.start_time
                return get_path(curr)
            for dir in range(4):
                child_loc = move(curr['loc'], dir)
                if child_loc[0] < 0 or child_loc[1] < 0 or child_loc[0] >= size or child_loc[1] >= size:
                    continue
                new_state = get_new_state(curr['loc'], child_loc, curr['state'])
                child = {'loc': child_loc,
                         'parent': curr,
                         'state': new_state,
                         'h_val': compute_heuristic_matt(new_state,self.goal),
                         'cost': curr['cost'] + 1}
                if (child['loc'],matrix_to_int(child['state'])) in closed_list:
                    existing_node = closed_list[(child['loc'],matrix_to_int(child['state']))]
                    if compare_nodes(child, existing_node):
                        closed_list[(child['loc'],matrix_to_int(child['state']))] = child
                        self.push_node(child)
                else:
                    closed_list[(child['loc'],matrix_to_int(child['state']))] = child
                    self.push_node(child)
        return None

class idastar(object):
    """The high-level search of CBS."""

    def __init__(self, goal):
        self.goal = goal
        self.name = "IDAStar"
        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0
        self.thresholds = dict()

        # compute heuristics for the low-level search

    def push_node(self, lst, node):
        heapq.heappush(lst, (node['h_val'], self.num_of_generated, node))
        # print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self, lst):
        _, id, node = heapq.heappop(lst)
        # print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node
    def find_solution(self, state, start_loc):
        self.start_time = timer.time()
        threshold = compute_heuristic_matt(state,self.goal)
        root = {'loc': start_loc,'parent': None,'state': state,'h_val': compute_heuristic_matt(state,self.goal),'cost': 0}
        f_values = [threshold]
        while threshold <= 100:
            stack = []
            closed_list = dict()
            self.push_node(stack,root)
            closed_list[matrix_to_int(root['state'])] = root
            threshold = min(f_values)
            f_values = []
            while len(stack) > 0:
                _, _, node = stack.pop()
                self.num_of_expanded += 1
                f = node['cost'] + node['h_val']
                # check if f is larger than threshold, dont explore if greater than
                if f > threshold:
                    continue
                # check if state is goal state
                if node['state'] == self.goal:
                    self.CPU_time = timer.time() - self.start_time
                    self.thresholds[threshold] = [self.num_of_generated,self.num_of_expanded]
                    return get_path(node)
                child_nodes = self.nextnodes(node)
                for child in child_nodes[::-1]:
                    child_n = child[2]
                    f_val = child_n['cost'] + child_n['h_val']
                    if f_val > threshold:
                        f_values.append(f_val)
                        self.num_of_generated -= 1
                        continue
                    if matrix_to_int(child_n['state']) in closed_list:
                        continue
                    closed_list[matrix_to_int(child_n['state'])] = child_n
                    stack.append(child)
            self.thresholds[threshold] = [self.num_of_generated,self.num_of_expanded]
            
    def find_solution1(self, state, start_loc):
        threshold = compute_heuristic_matt(state,self.goal)
        root = {'loc': start_loc,'parent': None,'state': state,'h_val': compute_heuristic_matt(state,self.goal),'cost': 0}
        self.num_of_generated += 1
        print('Threshhold',threshold)
        while(1):
            node, f = self.search(root,0,threshold)
            print("New Bound", f)
            # check if found
            if node != None:
                return node
            # if f is infinity, then no solution
            if f == float('inf'):
                return None
            # adjust threshold
            threshold = f
    def search(self,node, g, threshold):
        f = g + node['h_val']
        if f > threshold:
            return None, f
        # Check if goal state
        if node['state'] == self.goal:
            return node, -1
        minimun = float('inf')
        list_nodes = self.nextnodes(node)
        for tempnode in list_nodes:
            # Get node from the list of nodes (sorted by h_val)
            tempnode = self.pop_node(list_nodes)
            # Do recurse on tempnode
            newNode, val = self.search(tempnode, tempnode['cost'],threshold)
            # Check if the goal state was found
            if newNode != None:
                return newNode, -1
            # otherwise set new bound
            if val < minimun:
                minimun = val
        return None, minimun
    def nextnodes(self,node):
        nodes = []
        size = len(node['state'])
        # try 4 possible swaps
        for dir in range(4):
            child_loc = move(node['loc'], dir)
            # make sure child_loc is a valid location
            if child_loc[0] < 0 or child_loc[1] < 0 or child_loc[0] >= size or child_loc[1] >= size:
                    continue
            new_state = get_new_state(node['loc'], child_loc, node['state'])
            child = {'loc': child_loc,
                     'parent': node,
                     'state': new_state,
                     'h_val': compute_heuristic_matt(new_state,self.goal),
                     'cost': node['cost'] + 1}
            self.push_node(nodes,child)
        return nodes