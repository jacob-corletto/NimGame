from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3, 1]):
        self.initial = self.State(to_move='MAX', utility=0, board=board, moves=self.compute_moves(board))

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        """Return the resulting state after a move."""
        new_board = state.board.copy()
        row, count = move
        new_board[row] -= count
        next_player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        new_moves = self.compute_moves(new_board)
        return self.State(to_move=next_player, utility=self.compute_utility(new_board, next_player), board=new_board, moves=new_moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'MAX' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left."""
        result = all(count == 0 for count in state.board)
        return result

    def display(self, state):
        board = state.board
        print("board:", board)

    def compute_moves(self, board):
        """Compute all possible moves given the current board state."""
        moves = []
        for row in range(len(board)):
            for count in range(1, board[row] + 1):
                moves.append((row, count))
        return moves

    def compute_utility(self, board, player):
        """Compute the utility of the current board state."""
        if self.terminal_test(self.State(to_move=player, utility=0, board=board, moves=[])): #if this is true, 
            # return -1 if player == 'MAX' else 1
            if player == 'MAX':
                return 1
            else:
                return -1
        return 0

    class State:
        def __init__(self, to_move, utility, board, moves):
            self.to_move = to_move
            self.utility = utility
            self.board = board
            self.moves = moves

if __name__ == "__main__":
    nim = GameOfNim(board=[7, 5, 3, 1])  # Creating the game instance
    #print(nim.initial.board)
    #print(nim.initial.moves)

    state = nim.initial
    nim.display(state)
    
    #new_state = nim.result(nim.initial, (1, 3))
    #nim.display(new_state)
    
    while nim.terminal_test(state) == False:
        if state.to_move == 'MAX':
            move = alpha_beta_player(nim, state)
            print(move)
            state = nim.result(state, move)
            nim.display(state)
        else:
            print("current board state:", state.board)
            move = query_player(nim, state)
            print(move)
            state = nim.result(state, move)
            nim.display(state)
    
    
    # utility = nim.play_game(alpha_beta_player, query_player)  # computer moves first
    utility = nim.compute_utility(state.board,state.to_move)
    if utility < 0:
         print("MIN won the game")
    else:
         print("MAX won the game")