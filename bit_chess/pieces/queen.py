from pieces.piece import Piece
from precomputations.rook import precomputed_moves as precomputed_moves_rook
from precomputations.bishop import precomputed_moves as precomputed_moves_bishop
from utils.bit_manipulation import get_cross_bitboard
from constants import square_index_to_bishop_diagonals


class Queen(Piece):
    def __init__(self, color):
        self.color = color
        self.idx = 6

    def get_valid_moves(self, square, gamestate):
        # Rook
        unfiltered_moves = get_cross_bitboard(square)
        blocker_bits = unfiltered_moves & gamestate.board[8]
        moves_rook = precomputed_moves_rook[(square.bits, blocker_bits)]
        # Bishop
        unfiltered_moves = square_index_to_bishop_diagonals[square.square_index]
        blocker_bits = unfiltered_moves & gamestate.board[8]
        moves_bishop = precomputed_moves_bishop[(square.bits, blocker_bits)]
        return (moves_rook | moves_bishop) & (~gamestate.board[self.color])