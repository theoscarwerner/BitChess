from pieces.piece import Piece
from precomputations.king import precomputed_moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "K", 7)

    def get_valid_moves(self, from_square, gamestate):
        # TODO: filter checks
        unfiltered_moves = precomputed_moves[from_square.square_index]
        moves = unfiltered_moves & (~gamestate.board_position[self.color])
        return moves

