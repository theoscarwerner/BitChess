import numpy as np

board_indices = list(np.ndindex((8, 8)))


def pp_bits(bits):
    bit_string = "{0:b}".format(bits).zfill(64)

    print()
    for i in range(0, 63, 8):
        print(" ".join(list(bit_string[i: i + 8])))
    print()
