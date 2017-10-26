#!/usr/bin/python
import sys
import signal
from board import *
from maxminimizer import *

WHITE_PLAYER = 0
BLACK_PLAYER = 1
WHITE_WIN = 2
BLACK_WIN = 3
NO_ONE_WIN = 4
MAX_VALUE = float("inf")
MIN_VALUE = -float("inf")

def alpha_beta_search(who_player, input):
    def successor_max(player, board, alpha, beta):
        def possible_move():
            possible = []
            for chess in board.iter_chess(player):
                for new_pos in board.iter_move(chess):
                    old_pos = (chess.posX, chess.posY)
                    possible.append((new_pos, old_pos))
            return possible
    
        succ = []
        for move in possible_move():
            new_pos, old_pos = move
            string = board.predict(old_pos, new_pos)
            succ_board = Board(string) # copy
            
            temp = Maximizer(succ_board, MIN_VALUE, alpha, beta)
            succ.append((temp, move))
        return succ

    def successor_min(player, board, alpha, beta):
        def possible_move():
            possible = []
            for chess in board.iter_chess(player):
                for new_pos in board.iter_move(chess):
                    old_pos = (chess.posX, chess.posY)
                    possible.append((new_pos, old_pos))
            return possible
        
        succ = []
        for move in possible_move():
            new_pos, old_pos = move
            string = board.predict(old_pos, new_pos)
            succ_board = Board(string) # copy

            temp = Minimizer(succ_board, MAX_VALUE, alpha, beta)
            succ.append((temp, move))
        return succ

    def max_f(root, current_player, alpha, beta, depth):
        board = root.board
        if board.win == BLACK_WIN or board.win == WHITE_WIN:
            return root
        
        opponent = switch_player(current_player)
        for (succ, move) in successor_min(current_player, board, alpha, beta):
            # check if the end of game
            if succ.board.win == WHITE_WIN:
                if current_player == WHITE_PLAYER:
                    succ.value = MAX_VALUE
                else:
                    succ.value = MIN_VALUE
            elif succ.board.win == BLACK_WIN:
                if current_player == BLACK_WIN:
                    succ.value = MAX_VALUE
                else:
                    succ.value = MIN_VALUE
            # iterative depth search
            elif depth > 0:
                succ = min_f(succ, opponent, alpha, beta, depth-1)
            else:
                succ.value = succ.board.get_score(who_player)
            # update value and alpha value
            if succ.value > root.value:
                root.best = (succ.board.string, move)
            root.max_score(succ.value)
            if root.need_prune():
                return root
            root.max_alpha()
        return root
            
    def min_f(root, current_player, alpha, beta, depth):
        board = root.board
        opponent = switch_player(current_player)
        for (succ, move) in successor_max(current_player, board, alpha, beta):
            if succ.board.win == WHITE_WIN:
                if current_player == WHITE_PLAYER:
                    succ.value = MAX_VALUE
                else:
                    succ.value = MIN_VALUE
            elif succ.board.win == BLACK_WIN:
                if current_player == BLACK_WIN:
                    succ.value = MAX_VALUE
                else:
                    succ.value = MIN_VALUE
            elif depth > 0:
                succ = max_f(succ, opponent, alpha, beta, depth-1)
            else:
                succ.value = succ.board.get_score(who_player)
            if succ.value < root.value:
                root.best = (succ.board.string, move)
            root.min_score(succ.value)
            if root.need_prune():
                return root
            root.min_beta()
        return root

    print "Thinking! Please wait..."
    # check if the end of game
    board = Board(input)
    if board.win == WHITE_WIN:
        if who_player == WHITE_PLAYER:
            print "YOU WIN!"
            print board.string
        else:
            print "YOU LOSE!"
            print board.string
        return
    elif board.win == BLACK_WIN:
        if who_player == BLACK_PLAYER:
            print "YOU WIN!"
            print board.string
        else:
            print "YOU LOSE!"
            print board.string
        return

    # DFS search with alpha-beta pruning
    depth = 0
    while True:
        #for depth in range(MAX_DEPTH):
        depth += 1
        root = Maximizer(board, MIN_VALUE, MIN_VALUE, MAX_VALUE)
        root = max_f(root, who_player, MIN_VALUE, MAX_VALUE, depth)
        # display the result
        string, move = root.best
        new_pos, old_pos = move
        output = ("Hmm, I'd recommend moving the "
                  + root.board.string[convert_to_idx(old_pos)]
                  + " at row " + str(old_pos[1]) + " column " + str(old_pos[0])
                  + " to row " + str(new_pos[1]) + " column " + str(new_pos[0])
                  + ".")
        print output
        print "New board:"
        print string
    return



###########################################
#  call
assert(len(sys.argv)) == 4
program, who_plays, inputs, time_out = sys.argv
if who_plays == 'w':
    who_plays = WHITE_PLAYER
elif who_plays == 'b':
    who_plays = BLACK_PLAYER
########################
# Time Out func 
#https://stackoverflow.com/questions/492519/timeout-on-a-function-call
#https://stackoverflow.com/questions/11901328/how-to-timeout-function-in-python-timeout-less-than-a-second

def handler(signum, frame):
    raise TimeoutError()
signal.signal(signal.SIGALRM, handler)
signal.setitimer(signal.ITIMER_REAL, int(time_out))
try:
    alpha_beta_search(who_plays, inputs)
except:
    #print "TIME OUT!"
    time_out = 0
finally:
    signal.alarm(0)





