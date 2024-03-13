"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
operations = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if board == initial_state():
        # print("X's turn")
        return X
    else:

        # Count the number of X and O on the board
        x_count = 0
        o_count = 0
        for row in board:
            for cell in row:
                if cell == X:
                    x_count += 1
                elif cell == O:
                    o_count += 1
        
        # Logic that x always goes first, hence x value is always greater than o
        if x_count > o_count:
            # print("O's turn")
            return O
        else:
            # print("X's turn")
            return X
        
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Iterate through the board and find all the empty cells
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    try:
        i, j = action

        # using deepcopy to make a copy of the board (DO NOT USE shallow copy due to 2 dimensional list)
        newboard = copy.deepcopy(board)
        newboard[i][j] = player(board)
        return newboard
    except Exception as e:
        print(e)

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows of 3
    for rows in board:
        if rows[0] == rows[1] == rows[2]:
            return rows[0]
        
    
    # Check columns of 3
    for cols in range(3):
        if board[0][cols] == board[1][cols] == board[2][cols]:
            return board[0][cols]
            
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    # If no winner
    else:
        return None

                
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or not any(EMPTY in sublist for sublist in board):
        return True
    else:
        return False
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        # print(type(1))
        return int(1)
    elif winner(board) == O:
        # print(type(-1))
        return int(-1)
    else:
        # print(type(0))
        return int(0)
    
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Define the max and min functions, both functions will call each other recursively
    # Alpha = max value, Beta = min value
    # https://www.youtube.com/watch?v=N98F8HYEDCk

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            global operations
            operations += 1

            # Call the min function, and find the maximum value as v
            v = max(v, min_value(result(board, action), alpha, beta))

            # Compare the value of v with alpha(maximum value from previous branch), and update alpha if v is greater
            alpha = max(alpha, v)

            # If alpha is greater than or equal to beta(minimum value from previous branch), break the loop, stop searching the down the branch
            if alpha >= beta:
                break
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            global operations
            operations += 1
            # Call the max function, and find the minimum value as v
            v = min(v, max_value(result(board, action), alpha, beta))

            # Compare the value of v with beta(minimum value from previous branch), and update beta if v is smaller
            beta = min(beta, v)

            # If alpha is greater than or equal to beta(minimum value from previous branch), break the loop, stop searching the down the branch
            if alpha >= beta:
                break
        return v

    if terminal(board):
        return None

    else:


        choice = []
        alpha = -math.inf
        beta = math.inf

        # If the board is not in initial state, use the minimax algorithm to find the best move
        if player(board) == X:
            val = []
            action = []
            for act in actions(board):
                val.append(max_value(result(board, act), alpha, beta))
                action.append(act)
            choice.append(action[val.index(max(val))])
            
        
        # If the board is not in initial state, use the minimax algorithm to find the best move
        elif player(board) == O:
            val = []
            action = []
            for act in actions(board):
                val.append(min_value(result(board, act), alpha, beta))
                action.append(act)
            choice.append(action[val.index(min(val))])
        global operations
        print("Total operations: ", operations)
        operations = 0
        return choice[0]    
    
    raise NotImplementedError
