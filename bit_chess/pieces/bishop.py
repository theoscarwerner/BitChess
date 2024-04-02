from pieces.piece import Piece
from constants import square_index_to_bishop_diagonals
from precomputations.bishop import precomputed_moves


class Bishop(Piece):
    def __init__(self, color):
        self.color = color
        self.idx = 5

    def get_valid_moves(self, square, gamestate):
        # Get moves if board was empty
        unfiltered_moves = square_index_to_bishop_diagonals[square.square_index]
        # Get pieces that block it's path
        blocker_bits = unfiltered_moves & gamestate.board[-1]
        # get available moves from precomputation
        moves = precomputed_moves[(square.bits, blocker_bits)]
        # Remove moves that capture a piece of the same color
        valid_moves = moves & ~gamestate.board[self.color]
        return valid_moves

