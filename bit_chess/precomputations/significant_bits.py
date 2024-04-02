import numpy as np
import random
from utils import pp_bits

"""
Precompute the index of each 1 in a 16-bit integer.

Example:
    1001110001101011: (0, 1, 3, 5, 6, 10, 11, 12, 15)

Look-up is an array sized 2^16
"""


def compute_significant_bits(number):
    significant_bits = np.empty(0, dtype=int)
    for i in range(16):
        # Check if the i-th bit is set.
        # 2**15 is only leftmost bit set in 16 bit int.
        if (number << i) & 2**15:
            significant_bits = np.append(significant_bits, i)
    return significant_bits


significant_sixteen_bits = []
for number in range(2**16):
    significant_bits = compute_significant_bits(number)
    significant_sixteen_bits.append(significant_bits)


a = np.uint16(16)
b = np.uint16(32)
c = np.uint16(48)
sixteen_bits_a = np.uint64(0b1111111111111111000000000000000000000000000000000000000000000000)
sixteen_bits_b = np.uint64(0b0000000000000000111111111111111100000000000000000000000000000000)
sixteen_bits_c = np.uint64(0b0000000000000000000000000000000011111111111111110000000000000000)
sixteen_bits_d = np.uint64(0b0000000000000000000000000000000000000000000000001111111111111111)
empty = np.array([])

lsb_64_table = np.array([
   63, 30,  3, 32, 59, 14, 11, 33,
   60, 24, 50,  9, 55, 19, 21, 34,
   61, 29,  2, 53, 51, 23, 41, 18,
   56, 28,  1, 43, 46, 27,  0, 35,
   62, 31, 58,  4,  5, 49, 54,  6,
   15, 52, 12, 40,  7, 42, 45, 16,
   25, 57, 48, 13, 10, 39,  8, 44,
   20, 47, 38, 22, 17, 37, 36, 26
])


magic_number = np.uint64(2015959759)
def lsb(bits):
    assert bits != 0
    bits = bits ^ 32
    folded = bits ^ (bits >> np.uint64(32))
    return lsb_64_table[folded * magic_number >> np.uint64(26)]


def get_significant_bits(bits):
    return np.concatenate((
        significant_sixteen_bits[(bits & sixteen_bits_a) >> c],  # NOQA
        significant_sixteen_bits[(bits & sixteen_bits_b) >> b] + 16,  # NOQA
        significant_sixteen_bits[(bits & sixteen_bits_c) >> a] + 32,  # NOQA
        significant_sixteen_bits[(bits & sixteen_bits_d)] + 48,  # NOQA
    ))


pp_bits(np.uint64(2**32 - 1))
print(lsb(np.uint64(2**64 - 2)))


# print(get_significant_bits(np.uint64(655)))
