import numpy as np
import pieces
from utils.utils import pp_bits
from constants import range_grid


RANK_8 = np.uint64(0b1111111100000000000000000000000000000000000000000000000000000000)
RANK_7 = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
RANK_6 = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
RANK_5 = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
RANK_4 = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
RANK_3 = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
RANK_2 = np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
RANK_1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
FILE_A = np.uint64(0b1000000010000000100000001000000010000000100000001000000010000000)
FILE_B = np.uint64(0b0100000001000000010000000100000001000000010000000100000001000000)
FILE_C = np.uint64(0b0010000000100000001000000010000000100000001000000010000000100000)
FILE_D = np.uint64(0b0001000000010000000100000001000000010000000100000001000000010000)
FILE_E = np.uint64(0b0000100000001000000010000000100000001000000010000000100000001000)
FILE_F = np.uint64(0b0000010000000100000001000000010000000100000001000000010000000100)
FILE_G = np.uint64(0b0000001000000010000000100000001000000010000000100000001000000010)
FILE_H = np.uint64(0b0000000100000001000000010000000100000001000000010000000100000001)


class Square():
    def __init__(self,
                 shift: int | None = None,
                 index: tuple | None = None):
        """
        Compute the bitstring marking just one square. One of shift/index must be passed.

        If shift will generate bit-string according to square indicated below.

            8 |  0  1  2  3  4  5  6  7
            7 |  8  9 10 11 12 13 14 15
            6 | 16 17 18 19 20 21 22 23
            5 | 24 25 26 27 28 29 30 31
            4 | 32 33 34 35 36 37 38 39
            3 | 40 41 42 43 44 45 46 47
            2 | 48 49 50 51 52 53 54 55
            1 | 56 57 58 59 60 61 62 63
               -----------------------
                a  b  c  d  e  f  g  h

        if index it finds the bit-string corresponding to the coordinate system as if indexing in a
        numpy array. I.e (0, 0) -> 0, (3, 4) -> 28
        """

        if index is not None:
            shift = range_grid[index]

        square_zero = np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000)
        self.bits = square_zero >> np.uint64(shift)
        self.square_index = shift


def flip(bit):
    return bit ^ 1


def iter_squares():
    for i in range(64):
        yield Square(shift=i)


class GameState():
    def __init__(self, board_position=None, castle_rights=None):

        # Black and white are tactically placed in index 0 and 1, as I use 0 and 1 to represent
        # black and white in piece classes. This way we can retrieve the same color just by
        # Accessing the array with color as the idx.
        if board_position is None:
            self.board_position = [
                np.uint64(0b1111111111111111000000000000000000000000000000000000000000000000),  # black
                np.uint64(0b0000000000000000000000000000000000010000000000001111111111111111),  # white
                np.uint64(0b0000000011111111000000000000000000000000000000001111111100000000),  # pawns
                np.uint64(0b1000000100000000000000000000000000000000000000000000000010000001),  # rooks
                np.uint64(0b0100001000000000000000000000000000000000000000000000000001000010),  # knight
                np.uint64(0b0010010000000000000000000000000000000000000000000000000000100100),  # bishop
                np.uint64(0b0001000000000000000000000000000000000000000000000000000000010000),  # queens
                np.uint64(0b0000100000000000000000000000000000010000000000000000000000001000),  # kings
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

    def update(self, piece: pieces.Piece, from_square: Square, to_square: Square):

        captured_piece = self.get_piece_at(to_square)

        from_square_mask = ~from_square.bits
        # Updating piece specific bitboard
        self.board_position[piece.idx] = (
            self.board_position[piece.idx] & from_square_mask) | to_square.bits

        print("This piece type")
        pp_bits(self.board_position[piece.idx])

        # Updating all pieces bit-board
        self.board_position[8] = (self.pieces() & from_square_mask) | to_square.bits

        print("All Pieces")
        pp_bits(self.pieces())

        # Updating color bit-board
        self.board_position[piece.color] = (
            self.board_position[piece.color] & from_square_mask) | to_square.bits
        print("Color")
        pp_bits(self.board_position[piece.color])

        # If we're capturing a piece, we also update the bit-boards of the other
        # color and the bit-board for the type of captured piece.
        if captured_piece:
            # Updating other color
            self.board_position[piece.color ^ 1] = (
                self.board_position[piece.color ^ 1] & ~to_square.bits)

            print("Other color")
            pp_bits(self.board_position[piece.color ^ 1])

            # If the captured piece and moved piece are the same type, we don't need
            # to update anything because the bitboard was already updated earlier
            print("Captured piece before")
            pp_bits(self.board_position[captured_piece.idx])
            if not piece.is_same_type(captured_piece):
                self.board_position[captured_piece.idx] = (
                    self.board_position[captured_piece.idx] & ~to_square.bits)

            print("Captured piece after")
            pp_bits(self.board_position[captured_piece.idx])

        # Updating other color bit-board

    def black(self):
        return self.board_position[0]

    def white(self):
        return self.board_position[1]

    def pawns(self):
        return self.board_position[2]

    def rooks(self):
        return self.board_position[3]

    def knights(self):
        return self.board_position[4]

    def bishops(self):
        return self.board_position[5]

    def queens(self):
        return self.board_position[6]

    def kings(self):
        return self.board_position[7]

    def pieces(self):
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
