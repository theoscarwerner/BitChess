import numpy as np


def bits_to_array(bits):
    """Convert bits to 8x8 array with each field marked with 0 or 1 bit"""
    bit_string = "{0:b}".format(bits).zfill(64)
    return np.array([int(bit) for bit in bit_string]).reshape((8, 8))


def array_to_bits(bit_array):
    # Pretty ugly but this is what I came up with
    bit_array = list(bit_array.astype(int).flatten())
    int_value = int("".join([str(i) for i in bit_array]), 2)
    return np.uint64(int_value)
