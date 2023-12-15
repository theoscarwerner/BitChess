from pieces.piece import Piece
from precomputations.knight import precomputed_moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "N", 4)

    def get_valid_moves(self, from_square, gamestate):
        unfiltered_moves = precomputed_moves[from_square.square_index]
        moves = unfiltered_moves & (~gamestate.board_position[self.color])
        return moves
