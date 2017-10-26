#!/usr/bin/python
import sys

# configurations of game
WHITE_PLAYER = 0
BLACK_PLAYER = 1
WHITE_WIN = 2
BLACK_WIN = 3
NO_ONE_WIN = 4
BOARD_LENGTH = 8
BOARD_WIDTH = 8
UP = -1
DOWN = 1

##############################
### CHESSS PIECES
class Pieces:
    """
        a class to handle chess piece
        including position and belong to which player
    """
    def __init__(self, pos, player, letter):
        self.posX = pos[0]
        self.posY = pos[1]
        self.player = player
        self.letter = letter

    def move_to(self, pos):
        self.posX = pos[0]
        self.poxY = pos[1]
        return

    # chess can move to new position (succesor)
    # 'L' shaped (in 4 direction),  horizontally (in 2 direction)
    # vertically (in 2 direction), and diagnolly (in 4 direction)
    def succ_horizon_1(self):
        return []
    
    def succ_horizon_2(self):
        return []
    
    def succ_vertical_1(self):
        return []
    
    def succ_vertical_2(self):
        return []
    
    def succ_diagnol_1(self):
        return []

    def succ_diagnol_2(self):
        return []

    def succ_diagnol_3(self):
        return []

    def succ_diagnol_4(self):
        return []

    def succ_L(self):
        return []


def out_boardX(posX):
    return posX >= BOARD_WIDTH or posX < 0

def out_boardY(posY):
    return posY >= BOARD_LENGTH or posY < 0

class Parakeet(Pieces):
    """
        A Parakeet may move one square forward,
        if no other piece is on that square.
        Or, a Parakeet may
        move one square forward diagonally
    """
    def is_promote(self):
        # check if reached the end of board
        if self.player == WHITE_PLAYER:
            if self.posY == BOARD_LENGTH-1:
                return True
        elif self.player == BLACK_PLAYER:
            if self.posY == 0:
                return True
        return False
    
    def succ_vertical_1(self):
        direct = UP
        if self.player == WHITE_PLAYER:
            direct = DOWN
        if out_boardY(self.posY + direct):
            return []
        return [(self.posX, self.posY+direct)]
    
    def succ_diagnol_1(self):
        direct = UP
        if self.player == WHITE_PLAYER:
            direct = DOWN
        if out_boardX(self.posX-1) or out_boardY(self.posY + direct):
            return []
        return [(self.posX-1, self.posY+direct)]
        
    def succ_diagnol_2(self):
        direct = UP
        if self.player == WHITE_PLAYER:
            direct = DOWN
        if out_boardX(self.posX+1) or out_boardY(self.posY + direct):
            return []
        return [(self.posX+1, self.posY+direct)]


class Robin(Pieces):
    """
       A Robin may move any number of squares
       either horizontally or vertically
    """
    def succ_horizon_1(self):
        return [(posX, self.posY) for posX in reversed(range(self.posX))]
    
    def succ_horizon_2(self):
        return [(posX, self.posY)
                for posX in range(self.posX+1, BOARD_WIDTH)]
    
    def succ_vertical_1(self):
        return [(self.posX, posY) for posY in reversed(range(self.posY))]

    def succ_vertical_2(self):
        return [(self.posX, posY)
                for posY in range(self.posY+1, BOARD_LENGTH)]

class Blue_jay(Pieces):
    """
        moves along diagonal
        flight paths instead of horizontal or vertical ones.
    """
    def succ_diagnol_1(self):
        pos = []
        for i in range(self.posY):
            if i == 0:
                continue
            if out_boardX(self.posX-i) or out_boardY(self.posY-i):
                break
            pos.append((self.posX-i, self.posY-i))
        return pos
    
    def succ_diagnol_2(self):
        pos = []
        for i in range(self.posY):
            if i == 0:
                continue
            if out_boardX(self.posX+i) or out_boardY(self.posY-i):
                break
            pos.append((self.posX+i, self.posY-i))
        return pos
    
    def succ_diagnol_3(self):
        pos = []
        for i in range(BOARD_LENGTH-self.posY-1):
            if i == 0:
                continue
            if out_boardX(self.posX-i) or out_boardY(self.posY+i):
                break
            pos.append((self.posX-i, self.posY+i))
        return pos
    
    def succ_diagnol_4(self):
        pos = []
        for i in range(BOARD_LENGTH-self.posY-1):
            if i == 0:
                continue
            if out_boardX(self.posX+i) or out_boardY(self.posY+i):
                break
            pos.append((self.posX+i, self.posY+i))
        return pos

class Quetzal(Pieces):
    """
        A Quetzal is a combination of a Robin and a Blue jay
    """
    def succ_horizon_1(self):
        return [(posX, self.posY) for posX in reversed(range(self.posX))]
    
    def succ_horizon_2(self):
        return [(posX, self.posY)
                for posX in range(self.posX+1, BOARD_WIDTH)]
    
    def succ_vertical_1(self):
        return [(self.posX, posY) for posY in reversed(range(self.posY))]
    
    def succ_vertical_2(self):
        return [(self.posX, posY)
                for posY in range(self.posY+1, BOARD_LENGTH)]
    
    def succ_diagnol_1(self):
        pos = []
        for i in range(self.posY):
            if i == 0:
                continue
            if out_boardX(self.posX-i) or out_boardY(self.posY-i):
                break
            pos.append((self.posX-i, self.posY-i))
        return pos
    
    def succ_diagnol_2(self):
        pos = []
        for i in range(self.posY):
            if i == 0:
                continue
            if out_boardX(self.posX+i) or out_boardY(self.posY-i):
                break
            pos.append((self.posX+i, self.posY-i))
        return pos
    
    def succ_diagnol_3(self):
        pos = []
        for i in range(BOARD_LENGTH-self.posY-1):
            if i == 0:
                continue
            if out_boardX(self.posX-i) or out_boardY(self.posY+i):
                break
            pos.append((self.posX-i, self.posY+i))
        return pos
    
    def succ_diagnol_4(self):
        pos = []
        for i in range(BOARD_LENGTH-self.posY-1):
            if i == 0:
                continue
            if out_boardX(self.posX+i) or out_boardY(self.posY+i):
                break
            pos.append((self.posX+i, self.posY+i))
        return pos

class Kingfisher(Pieces):
    """
        Kingfishermay move one square
        in any direction, horizontally or vertically
    """
    def succ_horizon_1(self):
        if out_boardX(self.posX-1):
            return []
        return [(self.posX-1, self.posY)]
    
    def succ_horizon_2(self):
        if out_boardX(self.posX+1):
            return []
        return [(self.posX+1, self.posY)]
    
    def succ_vertical_1(self):
        if out_boardY(self.posY-1):
            return []
        return [(self.posX, self.posY-1)]
    
    def succ_vertical_2(self):
        if out_boardY(self.posY+1):
            return[]
        return [(self.posX, self.posY+1)]
    
    def succ_diagnol_1(self):
        if out_boardX(self.posX-1) or out_boardY(self.posY-1):
            return []
        return [(self.posX-1, self.posY-1)]
    
    def succ_diagnol_2(self):
        if out_boardX(self.posX+1) or out_boardY(self.posY-1):
           return []
        return [(self.posX+1, self.posY-1)]
    
    def succ_diagnol_3(self):
        if out_boardX(self.posX-1) or out_boardY(self.posY+1):
            return []
        return [(self.posX-1, self.posY+1)]
    
    def succ_diagnol_4(self):
        if out_boardX(self.posX+1) or out_boardY(self.posY+1):
            return []
        return [(self.posX+1, self.posY+1)]

class Nighthawk(Pieces):
    """
        A Nighthawk moves in L shaped patterns on the board,
        either two squares to the left or right followed
        by one square forward or backward, or one square left
        or right followed by two squares forward or
        backward.
    """
    def succ_L(self):
        pos = []
        if not out_boardX(self.posX+1) and not out_boardY(self.posY+2):
            pos.append((self.posX+1, self.posY+2))
        if not out_boardX(self.posX-1) and not out_boardY(self.posY+2):
            pos.append((self.posX-1, self.posY+2))
        if not out_boardX(self.posX+1) and not out_boardY(self.posY-2):
            pos.append((self.posX+1, self.posY-2))
        if not out_boardX(self.posX-1) and not out_boardY(self.posY-2):
            pos.append((self.posX-1, self.posY-2))
        if not out_boardX(self.posX+2) and not out_boardY(self.posY+1):
            pos.append((self.posX+2, self.posY+1))
        if not out_boardX(self.posX+2) and not out_boardY(self.posY-1):
            pos.append((self.posX+2, self.posY-1))
        if not out_boardX(self.posX-2) and not out_boardY(self.posY+1):
            pos.append((self.posX-2, self.posY+1))
        if not out_boardX(self.posX-2) and not out_boardY(self.posY-1):
            pos.append((self.posX-2, self.posY-1))
        return pos


def decode_letter(letter, pos):
    chess = None
    player = -1
    if letter == 'R':
        chess = Robin(pos, WHITE_PLAYER, 'R')
        player = WHITE_PLAYER
    elif letter == 'r':
        chess = Robin(pos, BLACK_PLAYER, 'r')
        player = BLACK_PLAYER
    elif letter == 'P':
        chess = Parakeet(pos, WHITE_PLAYER, 'P')
        if chess.is_promote():
            chess = Quetzal(pos, WHITE_PLAYER, 'Q')
        player = WHITE_PLAYER
    elif letter == 'p':
        chess = Parakeet(pos, BLACK_PLAYER, 'p')
        if chess.is_promote():
            chess = Quetzal(pos, BLACK_PLAYER, 'q')
        player = BLACK_PLAYER
    elif letter == 'N':
        chess = Nighthawk(pos, WHITE_PLAYER, 'N')
        player = WHITE_PLAYER
    elif letter == 'n':
        chess = Nighthawk(pos, BLACK_PLAYER, 'n')
        player = BLACK_PLAYER
    elif letter == 'Q':
        chess = Quetzal(pos, WHITE_PLAYER, 'Q')
        player = WHITE_PLAYER
    elif letter == 'q':
        chess = Quetzal(pos, BLACK_PLAYER, 'q')
        player = BLACK_PLAYER
    elif letter == 'K':
        chess = Kingfisher(pos, WHITE_PLAYER, 'K')
        player = WHITE_PLAYER
    elif letter == 'k':
        chess = Kingfisher(pos, BLACK_PLAYER, 'k')
        player = BLACK_PLAYER
    elif letter == 'B':
        chess = Blue_jay(pos, WHITE_PLAYER, 'B')
        player = WHITE_PLAYER
    elif letter == 'b':
        chess = Blue_jay(pos, BLACK_PLAYER, 'b')
        player = BLACK_PLAYER
    return (chess, player)

def convert_to_pos(indx_string):
    return (indx_string%BOARD_WIDTH, indx_string/BOARD_WIDTH)

def convert_to_idx(pos):
    posX, posY = pos
    return posY * BOARD_WIDTH + posX

def which_player(letter):
    if letter in 'RPNQKB':
        return WHITE_PLAYER
    elif letter in 'rpnqkb':
        return BLACK_PLAYER
    return -1

def switch_player(player):
    if player == WHITE_PLAYER:
        return BLACK_PLAYER
    return WHITE_PLAYER

##################################
# CHESS board
class Board:
    """
        A class to handle the chess board information
        including chess pos, possible move, and score
    """
    def __init__(self, string):
        self.white_chess = {}
        self.black_chess = {}
        self.string = string
        self.win = NO_ONE_WIN
        
        # check if it is end of game
        if 'K' in string and 'k' not in string:
            self.win = WHITE_WIN
        elif 'k' in string and 'K' not in string:
            self.win = BLACK_WIN
        # string to chess
        else:
            for i in range(BOARD_WIDTH):
                for j in range(BOARD_LENGTH):
                    chess, player = decode_letter(string[convert_to_idx((i, j))],
                                              (i,j))
                    if player == WHITE_PLAYER:
                        self.white_chess[(i, j)] = chess
                    elif player == BLACK_PLAYER:
                        self.black_chess[(i, j)] = chess

    def predict(self, old_pos, new_pos):
        """
            predict the string of next movement given a move
        """
        idx = convert_to_idx(old_pos)
        letter = self.string[idx]
        string = self.string[:idx] + '.' + self.string[idx+1:]
        idx = convert_to_idx(new_pos)
        return string[:idx] + letter + string[idx+1:]

    def find_chess(self, pos, player):
        if player == WHITE_PLAYER:
            if pos in self.white_chess:
                return self.white_chess[pos]
        elif player == BLACK_PLAYER:
            if pos in self.black_chess:
                return self.black_chess[pos]
        return False

    # enumerate all chess of player
    def iter_chess(self, player):
        iter = []
        if player == WHITE_PLAYER:
            for chess in self.white_chess:
                iter.append(self.white_chess[chess])
        elif player == BLACK_PLAYER:
            for chess in self.black_chess:
                iter.append(self.black_chess[chess])
        return iter

    # check if board occupied by itself
    def is_occupied(self, pos, player):
        if player == WHITE_PLAYER:
            return pos in self.white_chess
        elif player == BLACK_PLAYER:
            return pos in self.black_chess
            
    # check if board taken by opponent
    def is_taken(self,pos, player):
        if player == WHITE_PLAYER:
            return pos in self.black_chess
        elif player == BLACK_PLAYER:
            return pos in self.white_chess

    # iteration over all the possible moves
    # given a chess and stop as soon as space is taken or occupied
    # return all possible positions
    def iter_move(self, chess):
        iter = []
        player = chess.player
        for succ in chess.succ_horizon_1():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_horizon_2():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_vertical_1():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_vertical_2():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_diagnol_1():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_diagnol_2():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_diagnol_3():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_diagnol_4():
            if self.is_occupied(succ, player):
                break
            if self.is_taken(succ, player):
                iter.append(succ) # can eat piecies
                break
            iter.append(succ)
        for succ in chess.succ_L():
            if self.is_occupied(succ, player):
                continue
            iter.append(succ)
        return iter

    # the core function to evaluation board score
    def get_score(self, player):
        # check the power of each pieces
        def herustic_power(score):
            def evl_chess(letter):
                if letter == 'Q' or letter == 'q':
                    return 20
                elif letter == 'K' or letter == 'k':
                    return 8
                elif letter == 'R' or letter == 'r':
                    return 10
                elif letter =='B' or letter == 'b':
                    return 10
                elif letter == 'P' or letter == 'p':
                    return 1
                else:
                    return 0

            if player == WHITE_PLAYER:
                for pos in self.white_chess:
                    score += evl_chess(self.white_chess[pos].letter)
                for pos in self.black_chess:
                    score -= evl_chess(self.black_chess[pos].letter)
            elif player == BLACK_PLAYER:
                for pos in self.white_chess:
                    score -= eval_chess(self.white_chess[pos].letter)
                for pos in self.black_chess:
                    score += eval_chess(self.white_chess[pos].letter)

            return score
        # check the control space
        def herustic_space(score):
            def control_space(current_player):
                space = set()
                for chess in self.iter_chess(current_player):
                    for new_pos in self.iter_move(chess):
                        space.add(new_pos)
                return len(space)
            if player == WHITE_PLAYER:
                score += control_space(WHITE_PLAYER)
                score -= control_space(BLACK_PLAYER)
            elif player == BLACK_PLAYER:
                score += control_space(BLACK_PLAYER)
                score -= control_space(WHITE_PLAYER)
            return score
        return herustic_power(0) + herustic_space(1)
        
        
