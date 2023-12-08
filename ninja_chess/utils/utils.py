import numpy as np


def iter_board_indices():
    """Generator returning indices in chess board.
        (0, 0)
        (0, 1)
        (0, 2)
         ...
        (1, 0)
        (1, 1)
         ...
        (7, 7)
    """
    for x, y in np.ndindex((8, 8)):
        yield (x, y)


def pp_bits(bits):
    bit_string = "{0:b}".format(bits).zfill(64)
    print()
    for i in range(0, 63, 8):
        print(" ".join(list(bit_string[i: i + 8])))
    print()