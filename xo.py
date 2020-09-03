import copy
import random as rand

num_of_states = 0
num_of_calls = 0

class State:
    """
    State is a 3D matrix which is the tic-tac-toe board
    v: the value of that state
    turn: determines whose turn is it on that state
    row, col, page are for matrix iteration
    other variables are for visualization;
    credit of them and the function __str__() is for https://github.com/adamdevigili/3D-Tic-Tac-Toe

    """
    def __init__(self):
        self.v = 0
        self.turn = 0
        # ========================================================================
        self.row = 4
        self.col = 1
        self.page = 16
        self.grid_size = 4
        self.grid_data = ['-' for i in range(pow(self.grid_size, 3))]
        self.grid_size_squared = pow(self.grid_size, 2)
        self.direction_edges = {}
        self.direction_edges['U'] = range(self.grid_size_squared)
        self.direction_edges['D'] = range(self.grid_size_squared * (self.grid_size - 1), self.grid_size_squared * self.grid_size)
        self.direction_edges['R'] = [i * self.grid_size + self.grid_size - 1 for i in range(self.grid_size_squared)]
        self.direction_edges['L'] = [i * self.grid_size for i in range(self.grid_size_squared)]
        self.direction_edges['F'] = [i * self.grid_size_squared + j + self.grid_size_squared - self.grid_size for i in range(self.grid_size) for j in range(self.grid_size)]
        self.direction_edges['B'] = [i * self.grid_size_squared + j for i in range(self.grid_size) for j in range(self.grid_size)]
        self.direction_edges[' '] = []
    def __str__(self):
        k = 0
        grid_range = range(self.grid_size)
        grid_output = []
        for j in grid_range:
            row_top = ' ' * (self.grid_size * 2 + 1) + '_' * (self.grid_size * 4)
            if j:
                row_top = '|' + row_top[:self.grid_size * 2 - 1] + '|' + '_' * (self.grid_size * 2) + '|' + '_' * \
                          (self.grid_size * 2 - 1) + '|'
            grid_output.append(row_top)
            for i in grid_range:
                row_display = ' ' * (self.grid_size * 2 - i * 2) + '/' + ''.join\
                        ((' ' + str(self.grid_data[k + x]).ljust(1) + ' /') for x in grid_range)
                k += self.grid_size
                row_bottom = ' ' * (self.grid_size * 2 - i * 2 - 1) + '/' + '___/' * self.grid_size
                if j != grid_range[-1]:
                    row_display += ' ' * (i * 2) + '|'
                    row_bottom += ' ' * (i * 2 + 1) + '|'
                if j:
                    row_display = row_display[:self.grid_size * 4 + 1] + '|' + row_display[self.grid_size * 4 + 2:]
                    row_bottom = row_bottom[:self.grid_size * 4 + 1] + '|' + row_bottom[self.grid_size * 4 + 2:]
                    row_display = '|' + row_display[1:]
                    row_bottom = '|' + row_bottom[1:]
                grid_output += [row_display, row_bottom]
        return '\n'.join(grid_output)

    def printboard(self):
        """
        prints the matrix
        """
        print(self)

    def set_v(self, val):
        """
        assigns value of state
        """
        self.v = val
        return
    def set_turn(self, val):
        """
        assigns turn player in state
        """
        self.turn = val
        return
    def set_value(self, i, j, k, val):
        """
        sets the value = val in the requested cell
        """
        self.grid_data[i * self.row + j * self.col + k * self.page] = val
        return

    def get_v(self):
        """
        :return: value of state
        """
        return self.v
    def get_turn(self):
        """
        :return: turn in the state
        """
        return self.turn
    def get_value(self, i, j, k):
        """
        :param i: row
        :param j: column
        :param k: page
        :return: value[i][j][k]
        """
        return self.grid_data[i * self.row + j * self.col + k * self.page]

def win_or_loss(current, val):
    """
    :param current: state
    :param val: turn
    :return: bool
    if win -> return true
    """
    i = 0
    j = 0
    for k in range(0, current.grid_size):
        for i in range(0, 4):
            if current.get_value(i, j, k) == val and current.get_value(i, j + 1, k) == val and \
                    current.get_value(i, j + 2, k) == val and current.get_value(i, j + 3, k) == val:
                #print("i, j, k: ", i, j, k)
                #print("1")
                return True
        if current.get_value(j, j, k) == val and current.get_value(j + 1, j + 1, k) == val and \
                current.get_value(j + 2, j + 2, k) == val and current.get_value(j + 3, j + 3, k) == val:
            #print("i, j, k: ", i, j, k)
            #print("2")
            return True
        if current.get_value(j + 3, j, k) == val and current.get_value(j + 2, j + 1, k) == val and \
                current.get_value(j + 1, j + 2, k) == val and current.get_value(j, j + 3, k) == val:
            #print("i, j, k: ", i, j, k)
            #print("3")
            return True
    k = 0
    for i in range(0, current.grid_size):
        for j in range(0, 4):
            if current.get_value(i, j, k) == val and current.get_value(i, j, k + 1) == val and \
                    current.get_value(i, j, k + 2) == val and current.get_value(i, j, k + 3) == val:
                #print("i, j, k: ", i, j, k)
                #print("4")
                return True
        if current.get_value(i, k, k) == val and current.get_value(i, k + 1, k + 1) == val and \
                current.get_value(i, k + 2, k + 2) == val and current.get_value(i, k + 3, k + 3) == val:
            #print("i, j, k: ", i, j, k)
            #print("5")
            return True
        if current.get_value(i, k + 3, k) == val and current.get_value(i, k + 2, k + 1) == val and \
                current.get_value(i, k + 1, k + 2) == val and current.get_value(i, k, k + 3) == val:
            #print("i, j, k: ", i, j, k)
            #print("6")
            return True
    i = 0
    for j in range(0, current.grid_size):
        for k in range(0, 4):
            if current.get_value(i, j, k) == val and current.get_value(i + 1, j, k) == val and \
                    current.get_value(i + 2, j, k) == val and current.get_value(i + 3, j, k) == val:
                #print("i, j, k: ", i, j, k)
                #print("7")
                return True
        if current.get_value(i, j, i) == val and current.get_value(i + 1, j, i + 1) == val and \
                current.get_value(i + 2, j, i + 2) == val and current.get_value(i + 3, j, i + 3) == val:
            #print("i, j, k: ", i, j, k)
            #print("8")
            return True
        if current.get_value(i + 3, j, i) == val and current.get_value(i + 2, j, i + 1) == val and \
                current.get_value(i + 1, j, i + 2) == val and current.get_value(i, j, i + 3) == val:
            #print("i, j, k: ", i, j, k)
            #print("9")
            return True
    i = 0
    j = 0
    k = 0
    if current.get_value(i, j, k) == val and current.get_value(i + 1, j + 1, k + 1) == val and \
            current.get_value(i + 2, j + 2, k + 2) == val and current.get_value(i + 3, j + 3, k + 3) == val:
        #print("i, j, k: ", i, j, k)
        #print("10")
        return True
    if current.get_value(i, j, k + 3) == val and current.get_value(i + 1, j + 1, k + 2) == val and \
            current.get_value(i + 2, j + 2, k + 1) == val and current.get_value(i + 3, j + 3, k) == val:
        #print("i, j, k: ", i, j, k)
        #print("11")
        return True
    if current.get_value(i, j + 3, k + 3) == val and current.get_value(i + 1, j + 2, k + 2) == val and \
            current.get_value(i + 2, j + 1, k + 1) == val and current.get_value(i + 3, j, k) == val:
        #print("i, j, k: ", i, j, k)
        #print("12")
        return True
    if current.get_value(i, j + 3, k) == val and current.get_value(i + 1, j + 2, k + 1) == val and \
            current.get_value(i + 2, j + 1, k + 2) == val and current.get_value(i + 3, j, k + 3) == val:
        #print("i, j, k: ", i, j, k)
        #print("13")
        return True
    return False
def game_draw(current):
    """
    fullness of game board
    :param current: state
    :return: bool
    if draw --> return true
    """
    for i in range(0, current.grid_size):
        for j in range(0, current.grid_size):
            for k in range(0, current.grid_size):
                if current.get_value(i, j, k) == '-':
                    return False
    return True
def terminal(current, turn):
    """
    :return: true if game ends
    """
    # win or loss
    if win_or_loss(current, turn):
        return True
    # draw
    if game_draw(current):
        return True
    return False
def utility(current, turn):
    """
    :return: 1 for winning,-1 for losing, 0 for draw
    """
    if win_or_loss(current, turn):
        if current.get_turn() == 'X':
            if turn == 'X':
                return 10
            else:
                return -10

        if current.get_turn() == 'O':
            if turn == 'O':
                return 10
            else:
                return -10
    if game_draw(current):
        return 0
def successor(current, turn):
    """
    :return: generated states from current state
    """
    # turn is either 1 or 2
    next_array = []
    new_state = State()
    for i in range(0, current.grid_size):
        for j in range(0, current.grid_size):
            for k in range(0, current.grid_size):
                if current.get_value(i, j, k) == '-':
                    new_state = copy.deepcopy(current)
                    new_state.set_value(i, j, k, turn)
                    next_array.append(new_state)
    global num_of_states
    num_of_states = num_of_states + len(next_array)
    return next_array

def get_heuristic(current, turn):
    """
    :return: heuristic value for current
    """
    h1 = heuristic(current, 'X', 'O')
    h2 = heuristic(current, 'O', 'X')
    if turn == 'X':
        h = h2 - h1
        #h = h1 - h2
    if turn == 'O':
        h = h1 - h2
        #h = h2 - h1
    return h
def heuristic(current, val1, val2):
    """
    :param current:
    :param val1: player
    :param val2: player's opponent
    :return: heuristic value
    """
    j = 0
    score = 0
    for k in range(0, current.grid_size):
        for i in range(0, 4):
            if current.get_value(i, j, k) != val2 and current.get_value(i, j + 1, k) != val2 and \
                    current.get_value(i, j + 2, k) != val2 and current.get_value(i, j + 3, k) != val2:
                if current.get_value(i, j, k) == val1:
                    score += 0.25
                if current.get_value(i, j + 1, k) == val1:
                    score += 0.25
                if current.get_value(i, j + 2, k) == val1:
                    score += 0.25
                if current.get_value(i, j + 3, k) == val1:
                    score += 0.25

        if current.get_value(j, j, k) != val2 and current.get_value(j + 1, j + 1, k) != val2 and \
                current.get_value(j + 2, j + 2, k) != val2 and current.get_value(j + 3, j + 3, k) != val2:
            if current.get_value(i, j, k) == val1:
                score += 0.25
            if current.get_value(j + 1, j + 1, k) == val1:
                score += 0.25
            if current.get_value(j + 2, j + 2, k) == val1:
                score += 0.25
            if current.get_value(j + 3, j + 3, k) == val1:
                score += 0.25

        if current.get_value(j + 3, j, k) != val2 and current.get_value(j + 2, j + 1, k) != val2 and \
                current.get_value(j + 1, j + 2, k) != val2 and current.get_value(j, j + 3, k) != val2:
            if current.get_value(j + 3, j, k) == val1:
                score += 0.25
            if current.get_value(j + 2, j + 1, k) == val1:
                score += 0.25
            if current.get_value(j + 1, j + 2, k) == val1:
                score += 0.25
            if current.get_value(j, j + 3, k) == val1:
                score += 0.25

    k = 0
    for i in range(0, current.grid_size):
        for j in range(0, 4):
            if current.get_value(i, j, k) != val2 and current.get_value(i, j, k + 1) != val2 and \
                    current.get_value(i, j, k + 2) != val2 and current.get_value(i, j, k + 3) != val2:
                if current.get_value(i, j, k) == val1:
                    score += 0.25
                if current.get_value(i, j, k + 1) == val1:
                    score += 0.25
                if current.get_value(i, j, k + 2) == val1:
                    score += 0.25
                if current.get_value(i, j, k + 3) == val1:
                    score += 0.25

        if current.get_value(i, k, k) != val2 and current.get_value(i, k + 1, k + 1) != val2 and \
                current.get_value(i, k + 2, k + 2) != val2 and current.get_value(i, k + 3, k + 3) != val2:
            if current.get_value(i, k, k) == val1:
                score += 0.25
            if current.get_value(i, k + 1, k + 1) == val1:
                score += 0.25
            if current.get_value(i, k + 2, k + 2) == val1:
                score += 0.25
            if current.get_value(i, k + 3, k + 3) == val1:
                score += 0.25

        if current.get_value(i, k + 3, k) != val2 and current.get_value(i, k + 2, k + 1) != val2 and \
                current.get_value(i, k + 1, k + 2) != val2 and current.get_value(i, k, k + 3) != val2:
            if current.get_value(i, k + 3, k) == val1:
                score += 0.25
            if current.get_value(i, k + 2, k + 1) == val1:
                score += 0.25
            if current.get_value(i, k + 1, k + 2) == val1:
                score += 0.25
            if current.get_value(i, k, k + 3) == val1:
                score += 0.25

    i = 0
    for j in range(0, current.grid_size):
        for k in range(0, 4):
            if current.get_value(i, j, k) != val2 and current.get_value(i + 1, j, k) != val2 and \
                    current.get_value(i + 2, j, k) != val2 and current.get_value(i + 3, j, k) != val2:
                if current.get_value(i, j, k) == val1:
                    score += 0.25
                if current.get_value(i + 1, j, k) == val1:
                    score += 0.25
                if current.get_value(i + 2, j, k) == val1:
                    score += 0.25
                if current.get_value(i + 3, j, k) == val2:
                    score += 0.25

        if current.get_value(i, j, i) != val2 and current.get_value(i + 1, j, i + 1) != val2 and \
                current.get_value(i + 2, j, i + 2) != val2 and current.get_value(i + 3, j, i + 3) != val2:
            if current.get_value(i, j, i) == val1:
                score += 0.25
            if current.get_value(i + 1, j, i + 1) == val1:
                score += 0.25
            if current.get_value(i + 2, j, i + 2) == val1:
                score += 0.25
            if current.get_value(i + 3, j, i + 3) == val1:
                score += 0.25

        if current.get_value(i + 3, j, i) != val2 and current.get_value(i + 2, j, i + 1) != val2 and \
                current.get_value(i + 1, j, i + 2) != val2 and current.get_value(i, j, i + 3) != val2:
            if current.get_value(i + 3, j, i) == val1:
                score += 0.25
            if current.get_value(i + 2, j, i + 1) == val1:
                score += 0.25
            if current.get_value(i + 1, j, i + 2) == val1:
                score += 0.25
            if current.get_value(i, j, i + 3) == val1:
                score += 0.25

    i = 0
    j = 0
    k = 0
    if current.get_value(i, j, k) != val2 and current.get_value(i + 1, j + 1, k + 1) != val2 and \
            current.get_value(i + 2, j + 2, k + 2) != val2 and current.get_value(i + 3, j + 3, k + 3) != val2:
        if current.get_value(i, j, k) == val1:
            score += 0.25
        if current.get_value(i + 1, j + 1, k + 1) == val1:
            score += 0.25
        if current.get_value(i + 2, j + 2, k + 2) == val1:
            score += 0.25
        if current.get_value(i + 3, j + 3, k + 3) == val1:
            score += 0.25

    if current.get_value(i, j, k + 3) != val2 and current.get_value(i + 1, j + 1, k + 2) != val2 and \
            current.get_value(i + 2, j + 2, k + 1) != val2 and current.get_value(i + 3, j + 3, k) != val2:
        if current.get_value(i, j, k + 3) == val1:
            score += 0.25
        if current.get_value(i + 1, j + 1, k + 2) == val1:
            score += 0.25
        if current.get_value(i + 2, j + 2, k + 1) == val1:
            score += 0.25
        if current.get_value(i + 3, j + 3, k) == val1:
            score += 0.25

    if current.get_value(i, j + 3, k + 3) != val2 and current.get_value(i + 1, j + 2, k + 2) != val2 and \
            current.get_value(i + 2, j + 1, k + 1) != val2 and current.get_value(i + 3, j, k) != val2:
        if current.get_value(i, j + 3, k + 3) == val1:
            score += 0.25
        if current.get_value(i + 1, j + 2, k + 2) == val1:
            score += 0.25
        if current.get_value(i + 2, j + 1, k + 1) == val1:
            score += 0.25
        if current.get_value(i + 3, j, k) == val1:
            score += 0.25

    if current.get_value(i, j + 3, k) != val2 and current.get_value(i + 1, j + 2, k + 1) != val2 and \
            current.get_value(i + 2, j + 1, k + 2) != val2 and current.get_value(i + 3, j, k + 3) != val2:
        if current.get_value(i, j + 3, k) == val1:
            score += 0.25
        if current.get_value(i + 1, j + 2, k + 1) == val1:
            score += 0.25
        if current.get_value(i + 2, j + 1, k + 2) == val1:
            score += 0.25
        if current.get_value(i + 3, j, k + 3) == val1:
            score += 0.25
    return score

#1
def minimax(current, turn):
    print("Waiting for Computer...")
    # turn X - computer 1
    # turn O - human / computer 2
    temp = []; max_score = -99; j = 0
    v, temp = max_value(current, turn)
    for i in range(len(temp)):
        if temp[i].get_v() >= max_score:
            max_score = temp[i].get_v()
            j = i
    return temp[j]
def max_value(current, turn):
    global num_of_calls
    if terminal(current, turn):
        #print("max-value -> utility: ", utility(current, turn))
        return utility(current, turn), []
    else:
        if turn == 'X':
            #print("max-value -> current state: ")
            #current.printboard()
            v = -999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = min_value(actions[i], 'X')
                actions[i].set_v(v_new)
                v = max(v, v_new)

            return v, actions
        if turn == 'O':
            v = -999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = min_value(actions[i], 'O')
                actions[i].set_v(v_new)
                v = max(v, v_new)

            return v, actions
def min_value(current, turn):
    global num_of_calls
    if terminal(current, turn):
        #print("min-value -> utility: ", utility(current, turn))
        return utility(current, turn)
    else:
        temp =[]
        if turn == 'X':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = max_value(actions[i], 'O')
                v = min(v, v_new)

            return v
        if turn == 'O':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp =  max_value(actions[i], 'X')
                v = min(v, v_new)

            return v

def alpha_beta(current, turn):
    print("Waiting for Computer...")
    # turn X - computer 1
    # turn O - human / computer 2
    temp = []; max_score = -99; j = 0
    v, temp = ab_max_value(current, turn, -999999, 999999)
    for i in range(len(temp)):
        if temp[i].get_v() >= max_score:
            max_score = temp[i].get_v()
            j = i
    return temp[j]
def ab_max_value(current, turn, alpha, beta):
    global num_of_calls
    if terminal(current, turn):
        #print("max-value -> utility: ", utility(current, turn))
        return utility(current, turn), []
    else:
        if turn == 'X':
            #print("max-value -> current state: ")
            #current.printboard()
            v = -999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = ab_min_value(actions[i], 'X', alpha, beta)
                #print("max-value -> v: ", v)
                actions[i].set_v(v_new)
                v = max(v, v_new)

                if v >= beta:
                    return v, actions
                else:
                    alpha = max(alpha, v)

            return v, actions
        if turn == 'O':
            v = -999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = ab_min_value(actions[i], 'O', alpha, beta)
                #print("max-value v: ", v)
                actions[i].set_v(v_new)
                v = max(v, v_new)

                if v >= beta:
                    return v, actions
                else:
                    alpha = max(alpha, v)

            return v, actions
def ab_min_value(current, turn, alpha, beta):
    global num_of_calls
    if terminal(current, turn):
        #print("min-value -> utility: ", utility(current, turn))
        return utility(current, turn)
    else:
        temp = []
        if turn == 'X':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = ab_max_value(actions[i], 'O', alpha, beta)
                v = min(v, v_new)
                #print("min-value -> v: ", v)

                if v <= alpha:
                    return v
                else:
                    beta = min(beta, v)

            return v
        if turn == 'O':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = ab_max_value(actions[i], 'X', alpha, beta)
                v = min(v, v_new)
                #print("min-value -> v: ", v)

                if v <= alpha:
                    return v
                else:
                    beta = min(beta, v)

            return v

#2
def minimax_depth_limited(current, turn, depth):
    print("Waiting for Computer...")
    # turn X - computer 1
    # turn O - human / computer 2
    temp = []; max_score = -99999; j = 0
    v, temp = max_value_dl(current, turn, depth + 1)
    for i in range(len(temp)):
        if temp[i].get_v() > max_score:
            max_score = temp[i].get_v()
            j = i
    return temp[j]
def max_value_dl(current, turn, depth):
    global num_of_calls
    if depth == 4:
        if terminal(current, turn):
            return utility(current, turn), []
        else:
            return get_heuristic(current, turn), []
    else:
        if turn == 'X':
            #print("max-value -> current state: ")
            #current.printboard()
            v = -999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = min_value_dl(actions[i], 'X', depth + 1)
                actions[i].set_v(v_new)
                v = max(v, v_new)

            return v, actions
        if turn == 'O':
            v = -999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = min_value_dl(actions[i], 'O', depth + 1)
                actions[i].set_v(v_new)
                v = max(v, v_new)

            return v, actions
def min_value_dl(current, turn, depth):
    global num_of_calls
    if depth == 4:
        if terminal(current, turn):
            return utility(current, turn), []
        else:
            return get_heuristic(current, turn), []
    else:
        temp = []
        if turn == 'X':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = max_value_dl(actions[i], 'O', depth + 1)
                v = min(v, v_new)

            return v
        if turn == 'O':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = max_value_dl(actions[i], 'X', depth + 1)
                v = min(v, v_new)

            return v

def alpha_beta_depth_limited(current, turn, depth):
    print("Waiting for Computer...")
    # turn X - computer 1
    # turn O - human / computer 2
    temp = []; max_score = -99999; j = 0
    v, temp = ab_max_value_dl(current, turn, -999999, 999999, depth + 1)
    for i in range(len(temp)):
        if temp[i].get_v() > max_score:
            max_score = temp[i].get_v()
            #print("h = ", temp[i].get_v())
            j = i
    #print("h chosen = ", temp[j].get_v())
    return temp[j]
def ab_max_value_dl(current, turn, alpha, beta, depth):
    global num_of_calls
    if depth == 4:
        if terminal(current, turn):
            return utility(current, turn), []
        else:
            return get_heuristic(current, turn), []
    else:
        if turn == 'X':
            #print("max-value -> current state: ")
            #current.printboard()
            v = -999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = ab_min_value_dl(actions[i], 'X', alpha, beta, depth + 1)
                #print("max-value -> v: ", v)
                actions[i].set_v(v_new)
                v = max(v, v_new)

                if v >= beta:
                    return v, actions
                else:
                    alpha = max(alpha, v)

            return v, actions
        if turn == 'O':
            v = -999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("max-value -> chosen successor: ")
                #actions[i].printboard()
                v_new = ab_min_value_dl(actions[i], 'O', alpha, beta, depth + 1)
                #print("max-value v: ", v)
                actions[i].set_v(v_new)
                v = max(v, v_new)

                if v >= beta:
                    return v, actions
                else:
                    alpha = max(alpha, v)

            return v, actions
def ab_min_value_dl(current, turn, alpha, beta, depth):
    global num_of_calls
    if depth == 4:
        if terminal(current, turn):
            return utility(current, turn)
        else:
            return get_heuristic(current, turn)
    else:
        temp = []
        if turn == 'X':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'O')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = ab_max_value_dl(actions[i], 'O', alpha, beta, depth + 1)
                v = min(v, v_new)
                #print("min-value -> v: ", v)

                if v <= alpha:
                    return v
                else:
                    beta = min(beta, v)

            return v
        if turn == 'O':
            #print("min-value -> current state: ")
            #current.printboard()
            v = 999999
            actions = successor(current, 'X')
            num_of_calls = num_of_calls + 1
            for i in range(len(actions)):
                #print("min-value -> chosen successor: ")
                #actions[i].printboard()
                v_new, temp = ab_max_value_dl(actions[i], 'X', alpha, beta, depth + 1)
                v = min(v, v_new)
                #print("min-value -> v: ", v)

                if v <= alpha:
                    return v
                else:
                    beta = min(beta, v)

            return v

def is_valid(current, x, y, z):
    # check whether the user inputs are wrong or not
    if x < 0 or x > 3: return False
    if y < 0 or y > 3: return False
    if z < 0 or z > 3: return False
    if current.get_value(x, y, z) == 'X' or current.get_value(x, y, z) == 'O':
        return False
    return True
def random(current):
    x = rand.randrange(0, 4, 1)  # random number from 0 to 4(not itself) increasing by 1 step
    y = rand.randrange(0, 4, 1)
    z = rand.randrange(0, 4, 1)
    if current.get_value(x, y, z) != '-':
        while current.get_value(x, y, z) != '-':
            x = rand.randrange(0, 4, 1)
            y = rand.randrange(0, 4, 1)
            z = rand.randrange(0, 4, 1)

    #print("x,y,z: ", x, ", ", y, ", ", z)
    current.set_value(x, y, z, current.get_turn())

def play1(current, first_move):
    # first_move = 1 -> computer 1 starts (X)
    # first_move = 2 -> computer 2 starts (O)
    count_random_plays = 0
    while True:
        # game end
        if game_draw(current):
            print("It's a tie! No one Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states/num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'X':
            print("Computer 1 Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'O':
            print("Computer 1 Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        # player o win
        if terminal(current, 'O') == True and current.get_turn() == 'O':
            print("Computer 2 Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'O') == True and current.get_turn() == 'X':
            print("Computer 2 Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if first_move == 1:
            # computer 1 move
            print("Computer 1 Turn")
            if count_random_plays <= 1:
                random(current)
                count_random_plays += 1
                print("Computer 1 Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer 1 Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'X'):
                print("Computer 1 Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # computer 2 move
            print("Computer 2 Turn")
            if count_random_plays <= 1:
                random(current)
                count_random_plays += 1
                print("Computer 2 Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer 2 Moved")
            current.set_turn('X')
            current.printboard()
            print(" ")

        if first_move == 2:
            # computer 2 move
            print("Computer 2 Turn")
            if count_random_plays <= -1:
                random(current)
                count_random_plays += 1
                print("Computer 2 Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth=0)
                print("Computer 2 Moved")
            current.set_turn('X')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'O'):  # win_or_loss = True
                print("Computer 2 Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # computer 1 move
            print("Computer 1 Turn")
            if count_random_plays <= -1:
                random(current)
                count_random_plays += 1
                print("Computer 1 Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer 1 Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")
def play2(current, first_move):
    # first_move = 1 -> computer starts (X)
    # first_move = 2 -> random starts (O)
    count_random_plays = 0
    while True:
        # game end
        if game_draw(current):
            print("It's a tie! No one Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'X':
            print("Computer Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'O':
            print("Computer Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        # player o win
        if terminal(current, 'O') == True and current.get_turn() == 'O':
            print("Player O Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'O') == True and current.get_turn() == 'X':
            print("Player O Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if first_move == 1:
            # computer move
            print("Computer Turn")
            if count_random_plays <= 1:
                random(current)
                count_random_plays += 1
                print("Computer Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'X'):
                print("Computer Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # random move
            print("Random Turn")
            random(current)
            print("Random Moved")

            current.set_turn('X')
            current.printboard()
            print(" ")

        if first_move == 2:
            # human move
            print("\nRandom Turn")
            random(current)
            print("Random Moved")

            current.set_turn('X')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'O'):  # win_or_loss = True
                print("Random Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # computer move
            print("Computer Turn")
            if count_random_plays <= -1:
                random(current)
                count_random_plays += 1
                print("Computer Moved")
            else:
                # current = minimax(current, current.get_turn())
                # current = alpha_beta(current, current.get_turn())
                # current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")
def play3(current, first_move):
    # first_move = 1 -> computer starts (X)
    # first_move = 2 -> human starts (O)
    count_random_plays = 0
    while True:
        # game end
        if game_draw(current):
            print("It's a tie! No one Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'X':
            print("Computer Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'X') == True and current.get_turn() == 'O':
            print("Computer Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        # player o win
        if terminal(current, 'O') == True and current.get_turn() == 'O':
            print("Player O Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return
        if terminal(current, 'O') == True and current.get_turn() == 'X':
            print("Player O Won!")
            print("All Number of Created Successors: ", num_of_states)
            print("Average Number of Successors: ", num_of_states / num_of_calls)
            return

        if first_move == 1:
            # computer move
            print("Computer Turn")
            if count_random_plays <= 1:
                random(current)
                count_random_plays += 1
                print("Computer Moved")
            else:
                #current = minimax(current, current.get_turn())
                #current = alpha_beta(current, current.get_turn())
                #current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'X'):
                print("Computer Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # human move
            print("Your Turn")
            x, y, z = eval(input("Enter your x,y,z value: (x: row, y: column, z: page) -> "))
            while not is_valid(current, x, y, z):
                print("Wrong Coordinates")
                x, y, z = eval(input("Enter your x,y,z value: (x: row, y: column, z: page) -> "))

            current.set_value(x, y, z, 'O')
            current.set_turn('X')
            current.printboard()
            print(" ")

        if first_move == 2:
            # human move
            print("Your Turn")
            x, y, z = eval(input("Enter your x,y,z value: (x: row, y: column, z: page) -> "))
            while not is_valid(current, x, y, z): # is_valid == False
                print("Wrong Coordinates")
                x, y, z = eval(input("Enter your x,y,z value: (x: row, y: column, z: page) -> "))

            current.set_value(x, y, z, 'O')
            current.set_turn('X')
            current.printboard()
            print(" ")

            if win_or_loss(current, 'O'): # win_or_loss = True
                print("Player O Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return
            if game_draw(current):
                print("It's a tie! No one Won!")
                print("All Number of Created Successors: ", num_of_states)
                print("Average Number of Successors: ", num_of_states / num_of_calls)
                return

            # computer move
            print("Computer Turn")
            if count_random_plays <= 1:
                random(current)
                count_random_plays += 1
                print("Computer Moved")
            else:
                #current = minimax(current, current.get_turn())
                #current = alpha_beta(current, current.get_turn())
                #current = minimax_depth_limited(current, current.get_turn(), depth = 0)
                current = alpha_beta_depth_limited(current, current.get_turn(), depth = 0)
                print("Computer Moved")
            current.set_turn('O')
            current.printboard()
            print(" ")

def main():
    game = State()

    print("1. Computer against Computer")
    print("2. Computer against Random")
    print("3. Computer against Human")

    choice = eval(input("\nChoose one Please: "))
    if choice == 1:
        turn_number = eval(input("Who to play first: 1.Computer number 1(X)   2.Computer number 2(O) -> "))
        print(" ")
        if turn_number == 1:
            game.set_turn('X')
            play1(game, 1)
        if turn_number == 2:
            game.set_turn('O')
            play1(game, 2)
    if choice == 2:
        turn_number = eval(input("Who to play first: 1.Computer(X)   2.Random(O) -> "))
        print(" ")
        if turn_number == 1:
            game.set_turn('X')
            play2(game, 1)
        if turn_number == 2:
            game.set_turn('O')
            play2(game, 2)
    if choice == 3:
        turn_number = eval(input("Who to play first: 1.Computer(X)   2.You(O) -> "))
        print(" ")
        if turn_number == 1:
            game.set_turn('X')
            play3(game, 1)
        if turn_number == 2:
            game.set_turn('O')
            play3(game, 2)

main()
