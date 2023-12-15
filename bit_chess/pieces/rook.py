from pieces.piece import Piece
from utils.bit_manipulation import get_cross_bitboard
from precomputations.rook import precomputed_moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "R", 3)

    def get_valid_moves(self, from_square, gamestate):
        # Get moves if board was empty
        unfiltered_moves = get_cross_bitboard(from_square)
        # Get pieces that block it's path
        blocker_bits = unfiltered_moves & gamestate.pieces()
        # get available moves from precomputation
        moves = precomputed_moves[(from_square.bits, blocker_bits)]
        # Remove moves that capture a piece of the same color
        valid_moves = moves & ~gamestate.board_position[self.color]
        return valid_moves