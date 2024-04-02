import numpy as np
import time

import pieces
from square import Square, iter_squares
from utils import pp_bits
from precomputations.significant_bits import get_significant_bits


# Rooks to updated castle rights; used in Gamestate.update(). If from-square is rook and is in
# this dict then rook is moving from starting-square and castle rights lost
rook_castle_map = {
    np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000): np.uint8(0b0111),
    np.uint64(0b0000000100000000000000000000000000000000000000000000000000000000): np.uint8(0b1011),
    np.uint64(0b0000000000000000000000000000000000000000000000000000000010000000): np.uint8(0b1101),
    np.uint64(0b0000000000000000000000000000000000000000000000000000000000000001): np.uint8(0b1110),
}

# Retrieved by color; remove castle for color if king moves
king_update_bits = [
    np.uint8(0b0011),
    np.uint8(0b1100),
]


class GameState():
    def __init__(self, board=None, castle_rights=None):

        # Black and white are tactically placed in index 0 and 1, as I use 0 and 1 to represent
        # colors black and white in piece classes. This way we can retrieve the same color just by
        # Accessing the array with color as the idx, which is also encoded as an attribute in piece
        # classes
        if board is None:
            self.board = [
                np.uint64(0b1111111111111111000000000000000000000000000000000000000000000000),  # black
                np.uint64(0b0000000000000000000000000000000000000000000000001111111111111111),  # white
                np.uint64(0b0000000011111111000000000000000000000000000000001111111100000000),  # pawns
                np.uint64(0b1000000100000000000000000000000000000000000000000000000010000001),  # rooks
                np.uint64(0b0100001000000000000000000000000000000000000000000000000001000010),  # knight
                np.uint64(0b0010010000000000000000000000000000000000000000000000000000100100),  # bishop
                np.uint64(0b0001000000000000000000000000000000000000000000000000000000010000),  # queens
                np.uint64(0b0000100000000000000000000000000000000000000000000000000000001000),  # kings
                np.uint64(0b1111111111111111000000000000000000000000000000001111111111111111),  # pieces
            ]
        else:
            self.board = board
        #  bq  bk  wq  wk
        # | x | x | x | x |
        # | 1 | 1 | 1 | 1 |
        # E.g bq = black queenside; flip bit to zero if castle rights lost
        if castle_rights is None:
            self.castle_rights = np.uint8(0b1111)
        else:
            self.castle_rights = castle_rights

        self.in_check = [False, False]

    def update(self,
               piece: pieces.Piece,
               from_square: Square,
               to_square: Square) -> None:

        color = piece.color

        self._handle_castling(from_square, to_square, color)

        captured_piece = self.get_piece_at(to_square)

        not_from_square = ~from_square.bits
        # Updating piece specific bitboard
        self.board[piece.idx] = (
            self.board[piece.idx] & not_from_square) | to_square.bits

        # Updating all pieces bit-board
        self.board[8] = (self.board[8] & not_from_square) | to_square.bits

        # Updating color bit-board
        self.board[color] = (
            self.board[color] & not_from_square) | to_square.bits

        # If we're capturing a piece, we also update the bit-boards of the other
        # color and the bit-board for the type of captured piece.
        if captured_piece:
            # Updating other color
            self.board[color ^ 1] = self.board[color ^ 1] & ~to_square.bits

            # If the captured piece and moved piece are the same type, we don't need
            # to update anything because the bitboard was already updated earlier
            if not piece.is_same_type(captured_piece):
                self.board[captured_piece.idx] = self.board[captured_piece.idx] & ~to_square.bits


    def _handle_castling(self, from_square, to_square, color):
        """Updates Castle-rights if a rook or king is moved, and pre-emptively
           moves rook as well when castling.
            This can be made more efficient as right now these checks are made even after
            castle rights are lost. """

        castle_update_bits = rook_castle_map.get(from_square.bits)
        # If a rook moves castle rights are lost at that corner
        if (rook_castle_map.get(from_square.bits) # Walrus operator
            and (from_square.bits & self.board[3] != 0)): # Piece being moves is rook
            self.castle_rights &= castle_update_bits

        # Piece being moved is king
        # Update castle rights for king
        if from_square.bits & self.board[7] != 0:
            self.castle_rights &= king_update_bits[color]

            # If the move is an actual castling move
            # This only happens at most twice per game so efficiency isn't that important.
            # Below we just update bitboards for rooks
            if abs(from_square.square_index - to_square.square_index) == 2:
                rook_move_from, rook_move_to = {
                    2: (np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000),
                        np.uint64(0b0001000000000000000000000000000000000000000000000000000000000000)),
                    6: (np.uint64(0b0000000100000000000000000000000000000000000000000000000000000000),
                        np.uint64(0b0000010000000000000000000000000000000000000000000000000000000000)),
                    58: (np.uint64(0b0000000000000000000000000000000000000000000000000000000010000000),
                         np.uint64(0b0000000000000000000000000000000000000000000000000000000000010000)),
                    62: (np.uint64(0b0000000000000000000000000000000000000000000000000000000000000001),
                         np.uint64(0b0000000000000000000000000000000000000000000000000000000000000100)),
                }[to_square.square_index]
                self.board[3] = (
                    self.board[3] & ~rook_move_from) | rook_move_to
                self.board[8] = (  # Update pieces
                    self.board[8] & ~rook_move_from) | rook_move_to
                self.board[color] = (  # Update color
                    self.board[color] & ~rook_move_from) | rook_move_to

    def black(self) -> np.uint64:
        return self.board[0]

    def white(self) -> np.uint64:
        return self.board[1]

    def pawns(self) -> np.uint64:
        return self.board[2]

    def rooks(self) -> np.uint64:
        return self.board[3]

    def knights(self) -> np.uint64:
        return self.board[4]

    def bishops(self) -> np.uint64:
        return self.board[5]

    def get_queens(self) -> np.uint64:
        return self.board[6]

    def kings(self) -> np.uint64:
        return self.board[7]

    def pieces(self) -> np.uint64:
        return self.board[8]

    def get_piece_at(self, square: Square):
        # Pre-empively return if there is not piece
        if (square.bits & self.board[8]) == 0:
            # There is no piece on the square
            return 0
        elif square.bits & self.board[2]:
            return pieces.Pawn(color=self.get_square_color(square))
        elif square.bits & self.board[3]:
            return pieces.Rook(color=self.get_square_color(square))
        elif square.bits & self.board[4]:
            return pieces.Knight(color=self.get_square_color(square))
        elif square.bits & self.board[5]:
            return pieces.Bishop(color=self.get_square_color(square))
        elif square.bits & self.board[6]:
            return pieces.Queen(color=self.get_square_color(square))
        elif square.bits & self.board[7]:
            return pieces.King(color=self.get_square_color(square))
        else:
            raise ValueError("""Something is terribly wrong with this Square..
                                There is neither a piece nor nothing on it.""")

    def get_square_color(self, square: Square):
        """Returns 0 (black) if the given square has a black piece,
           and 1 if given square has a white piece on it."""
        return int(bool(square.bits & self.board[1]))
        if square.bits & self.board[0]:
            return 0
        elif square.bits & self.board[1]:
            return 1
        else:
            raise ValueError("Got Square without a piece on it")

    def iter_all_pieces(self, color):
        piece_order = [pieces.Pawn, pieces.Rook, pieces.Knight,
                 pieces.Bishop, pieces.Queen, pieces.King]

        for Piece, bitboard in zip(piece_order, self.board[2: 8]):
            for i in get_significant_bits(bitboard & self.board[color]):
                square = Square(shift=i)
                yield Piece(color), square


    def generate_moves(self, color):
        # print("This is board color")
        # print(pp_bits(self.board[color]))
        for piece, square in self.iter_all_pieces(color):
        # for i in get_significant_bits(self.board[color]):
        #     square = Square(shift=i)
        #     piece = self.get_piece_at(square)
            moves_bitboard = piece.get_valid_moves(square, self)
            moves = get_significant_bits(moves_bitboard)

    def copy(self, board, castle_rights):
        return GameState(board=board, castle_rights=castle_rights)


