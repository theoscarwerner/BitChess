import numpy as np
from constants import range_grid, files, ranks


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

        Attributes:
            self.bits         -> bits where the corresponding square is 1. Everything else is 0.
            self.square_index -> int of the square corresponding to grid above
        """

        if index is not None:
            shift = range_grid[index]

        square_zero = np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000)
        self.bits = square_zero >> np.uint64(shift)
        self.square_index = shift

    def get_rank_bits(self) -> np.uint64:
        return ranks[self.square_index // 8]

    def get_file_bits(self) -> np.uint64:
        return files[self.square_index % 8]


def iter_squares():
    for i in range(64):
        yield Square(shift=i)
