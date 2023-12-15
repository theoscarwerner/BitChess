import numpy as np
import pieces
from utils import pp_bits
from constants import range_grid
from square import Square


def iter_squares():
    for i in range(64):
        yield Square(shift=i)


def flip(bit):
    return bit ^ 1


class GameState():
    def __init__(self, board_position=None, castle_rights=None):

        # Black and white are tactically placed in index 0 and 1, as I use 0 and 1 to represent
        # black and white in piece classes. This way we can retrieve the same color just by
        # Accessing the array with color as the idx, which is also encoded as an attribute in piece
        # classes
        if board_position is None:
            self.board_position = [
                np.uint64(0b1111111111111111000000000000000000000000000000000000000000000000),  # black
                np.uint64(0b0000000000000000000000000000000000010000000000001111111111111111),  # white
                np.uint64(0b0000000011111111000000000000000000000000000000001111111100000000),  # pawns
                np.uint64(0b1000000100000000000000000000000000010000000000000000000010000001),  # rooks
                np.uint64(0b0100001000000000000000000000000000000000000000000000000001000010),  # knight
                np.uint64(0b0010010000000000000000000000000000000000000000000000000000100100),  # bishop
                np.uint64(0b0001000000000000000000000000000000000000000000000000000000010000),  # queens
                np.uint64(0b0000100000000000000000000000000000000000000000000000000000001000),  # kings
                np.uint64(0b1111111111111111000000000000000000010000000000001111111111111111),  # pieces
            ]
        else:
            self.board_position = board_position
        #  bq  bk  wq  wk
        # | x | x | x | x |
        # E.g bq = black queenside; flip bit to zero if castle rights lost
        if castle_rights is None:
            self.castle_rights = np.uint8(1111)
        else:
            self.castle_rights = castle_rights

    def update(self,
               piece: pieces.Piece,
               from_square: Square,
               to_square: Square) -> None:

        captured_piece = self.get_piece_at(to_square)

        from_square_mask = ~from_square.bits
        # Updating piece specific bitboard
        self.board_position[piece.idx] = (
            self.board_position[piece.idx] & from_square_mask) | to_square.bits

        # print("This piece type")
        # pp_bits(self.board_position[piece.idx])

        # Updating all pieces bit-board
        self.board_position[8] = (self.pieces() & from_square_mask) | to_square.bits

        # print("All Pieces")
        # pp_bits(self.pieces())

        # Updating color bit-board
        self.board_position[piece.color] = (
            self.board_position[piece.color] & from_square_mask) | to_square.bits
        # print("Color")
        # pp_bits(self.board_position[piece.color])

        # If we're capturing a piece, we also update the bit-boards of the other
        # color and the bit-board for the type of captured piece.
        if captured_piece:
            # Updating other color
            self.board_position[piece.color ^ 1] = (
                self.board_position[piece.color ^ 1] & ~to_square.bits)

            # print("Other color")
            # pp_bits(self.board_position[piece.color ^ 1])

            # If the captured piece and moved piece are the same type, we don't need
            # to update anything because the bitboard was already updated earlier
            # print("Captured piece before")
            # pp_bits(self.board_position[captured_piece.idx])
            if not piece.is_same_type(captured_piece):
                self.board_position[captured_piece.idx] = (
                    self.board_position[captured_piece.idx] & ~to_square.bits)

            # print("Captured piece after")
            # pp_bits(self.board_position[captured_piece.idx])

        # Updating other color bit-board

    def black(self) -> None:
        return self.board_position[0]

    def white(self) -> None:
        return self.board_position[1]

    def pawns(self) -> None:
        return self.board_position[2]

    def rooks(self) -> None:
        return self.board_position[3]

    def knights(self) -> None:
        return self.board_position[4]

    def bishops(self) -> None:
        return self.board_position[5]

    def queens(self) -> None:
        return self.board_position[6]

    def kings(self) -> None:
        return self.board_position[7]

    def pieces(self) -> None:
        return self.board_position[8]

    def get_piece_at(self, square: Square):
        if (square.bits & self.pieces()) == 0:
            return 0
        elif square.bits & self.pawns():
            return pieces.Pawn(color=self.get_square_color(square))
        elif square.bits & self.rooks():
            return pieces.Rook(color=self.get_square_color(square))
        elif square.bits & self.knights():
            return pieces.Knight(color=self.get_square_color(square))
        elif square.bits & self.bishops():
            return pieces.Bishop(color=self.get_square_color(square))
        elif square.bits & self.kings():
            return pieces.King(color=self.get_square_color(square))
        elif square.bits & self.queens():
            return pieces.Queen(color=self.get_square_color(square))

    def get_square_color(self, square: Square):
        if square.bits & self.black():
            return 0
        elif square.bits & self.white():
            return 1
        else:
            raise ValueError("Got Square without a piece on it")
