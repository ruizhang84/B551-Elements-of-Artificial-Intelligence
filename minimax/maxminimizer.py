# python code for minimizer
# reference to AI course and lectur notes from 
# UC Berkeley CS188 Intro to AI -- Course Material
# http://ai.berkeley.edu/lecture_videos.html
MAX_VALUE = float("inf")
MIN_VALUE = -float("inf")

class Node:
    """
       a class for handle basic info 
       of minimizer node.
       value: the score of minimizer
       alpha: best already explored along 
              path to root for maxmizer
       beta: best already explored along
              path to root for minimizer
    """
    def __init__(self, board, score, alpha, beta):
        self.value = score
        self.alpha = alpha
        self.beta = beta
        # extra info for search
        self.board = board
        self.best = None
    
    def update_alpha(self, alpha):
        self.alpha = alpha
        return
    
    def update_beta(self, beta):
        self.beta = beta
        return
    
    def update_score(self, score):
        self.value = score 
        return

class Maximizer(Node):
    """
        a class to handle the maximizer
        inheritant from Node class
        for each successor
            v = max(v, successor's v)
            if v >= beta
                prune and return
            alpha = max(alpha, v)
    """
    def need_prune(self):
        return self.value >= self.beta
        
    def max_score(self, score):
        self.value = max(self.value, score)
        return
    
    def max_alpha(self):
        self.alpha = max(self.alpha, self.value)
        return


class Minimizer(Node):
    """
        a class to handle the maximizer
        inheritant from Node class
        for each successor
            v = min(v, successor's v)
            if v <= alpha
                prune and return
            alpha = max(alpha, v)
    """
    def need_prune(self):
        return self.value <= self.alpha

    def min_score(self, score):
        self.value = min(self.value, score)
        return
        
    def min_beta(self):
        self.beta = min(self.beta, self.value)
        return

#def max_value(states, alpha, beta):
#    root = Maximizer(MIN_VALUE, alpha, beta)
#    for successor in states:
#        root.max_score(successor.value)
#        if root.need_prune:
#            return root
#        root.max_alpha()
#    return root
    
#def min_value(states, alpha, beta):
#    root = Minimizer(MIN_VALUE, alpha, beta)
#    for successor in states:
#        root.min_score(successor.value)
#        if root.need_prune:
#            return root
#        root.min_beta()
#    return root





    
    
    
