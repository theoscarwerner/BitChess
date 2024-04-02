from pieces.piece import Piece
from precomputations.knight import precomputed_moves


class Knight(Piece):
    def __init__(self, color):
        self.idx = 4
        self.color = color

    def get_valid_moves(self, square, gamestate):
        unfiltered_moves = precomputed_moves[square.square_index]
        moves = unfiltered_moves & (~gamestate.board[self.color])
        return moves
