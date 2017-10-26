#!/usr/bin/env python
import sys
import numpy as np
import heapq

GOAL = np.array(
                [[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12],
                 [13, 14, 15, 0]]
                )

MAX_STEP = 3

def read_file(argv):
    def process_line(line):
        line = line.strip()
        return [int(s) for s in line.split()]
    
    # sanity
    assert(len(argv) == 2)
    # data, d[row][col] = number
    data = []
    
    # process line by line
    with open(argv[1], 'rU') as f:
        for line in f:
            temp = process_line(line)
            data.append(temp)

    return data

def A_star_search(data):
    init_state = convert_state(data)
    
    # A* search
    if is_goal(init_state.board):
        return init_state
    
    # queue-> fringe
    queue = init_queue()
    visited = init_vist()
    insert(queue, init_state, 0)

    # repeat search
    while not_empty(queue):
        state = next_queue(queue)
        record(visited, state)
        
        if is_goal(state.board):
            return state

        for succ in successor(state):
            if not_see(visited, succ):
                if not_in_queue(queue, succ):
                    insert(queue, succ, cost_f(succ))
    
    return "FAILURE"

class State:
    """
       A class for state, including
       move info, how previou state move to current state
       board info, two dim array (row,col)
    """
    def __init__(self, board):
        self.board = board
        self.prev = None
        self.move = None
        self.cost = 0

def init_result():
    return []

def convert_state(data):
    state = State(np.array(data))
    return state

def init_queue():
    return []

def init_vist():
    return []

def record(visited, state):
    visited.append(state.board)

def next_queue(queue):
    h, state = heapq.heappop(queue)
    return state

def not_empty(queue):
    return len(queue) > 0

def insert(queue, ele, h):
    heapq.heappush(queue, (h, ele))

def not_see(visited, succ):
    for board in visited:
        if np.array_equal(board, succ.board):
            return False
    return True

def not_in_queue(queue, succ):
    for old in queue:
        if np.array_equal(old[1].board, succ.board):
            return False
    return True

def update_result(state):
    result = init_result()
    while state.move is not None:
        result.append(state.move)
        state = state.prev
    result.reverse()
    return result

def is_goal(board):
    return np.array_equal(board, GOAL)

def successor(state):
    """
        successor function,
        one, two, or three tiles may be slid
        left, right, up or down in a single move
    """
    def update(prev, succ, board, move):
        if board is not None:
            state = State(board)
            state.move = move
            state.prev = prev
            state.cost = prev.cost + 1
            succ.append(state)
        return
    
    def move_info(direct, step, pos):
        row_col = -1
        if direct == "L" or direct == "R":
            row_col = int(pos[0])
        else:
            row_col = int(pos[1])
        return direct + str(step) + str(row_col+1)
    
    def valid(pos, direct, shape, step):
        row, col = shape
        if direct == "R":
            return pos[1] - step >= 0
        elif direct == "L":
            return pos[1] + step < col
        elif direct == "D":
            return pos[0] - step >= 0
        elif direct == "U":
            return pos[0] + step < row
        return False

    def swap(board, direct, pos):
        row, col = pos
        if direct == "R":
            board[row,col], board[row,col-1] = board[row,col-1], board[row,col]
        elif direct == "L":
            board[row,col], board[row,col+1] = board[row,col+1], board[row,col]
        elif direct == "D":
            board[row,col], board[row-1,col] = board[row-1,col], board[row,col]
        else:
            board[row,col], board[row+1,col] = board[row+1,col], board[row,col]

    def move_board(board, direct, step):
        if step == 0:
            return board

        pos = np.where(board == 0)
        swap(board, direct, pos)

        return move_board(board, direct, step-1)
    
    # param
    succ = []
    pos = np.where(state.board == 0)
    shape = np.shape(state.board)
    direct_set = ["L", "R", "U", "D"]

    # search board
    for step in range(1, MAX_STEP+1):
        for direct in direct_set:
            if valid(pos, direct, shape, step):
                cp_board = copy(state.board)
                update(
                       state,
                       succ,
                       move_board(cp_board, direct, step),
                       move_info(direct, step, pos)
                       )

    return succ

def copy(board):
    return np.copy(board)

def cost_f(state):
    # f(n) = g(n) + h(n)
    return state.cost + heurstic(state)

def heurstic(state):
    # Number of tiles that are
    # not in the final position.
    # divied by 3
    miss_placed = 0
    board = state.board
    for index, x in np.ndenumerate(GOAL):
        if board[index] == 0 or x == 0:
            continue
        if board[index] != x:
            miss_placed += 1
    return miss_placed/MAX_STEP

def display(result):
    path = update_result(result)
    for m in path:
        print m,
    print
    return

# ###########################
# read in data
data = read_file(sys.argv)

# process data
results = A_star_search(data)

# display movement
display(results)
