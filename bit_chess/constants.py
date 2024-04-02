import numpy as np


range_grid = np.array(
    [
        [0, 1, 2, 3, 4, 5, 6, 7],
        [8, 9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29, 30, 31],
        [32, 33, 34, 35, 36, 37, 38, 39],
        [40, 41, 42, 43, 44, 45, 46, 47],
        [48, 49, 50, 51, 52, 53, 54, 55],
        [56, 57, 58, 59, 60, 61, 62, 63],
    ]
)

RANK_8 = np.uint64(0b1111111100000000000000000000000000000000000000000000000000000000)
RANK_7 = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
RANK_6 = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
RANK_5 = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
RANK_4 = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
RANK_3 = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
RANK_2 = np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
RANK_1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)

# Rank 8 is first index because in a chessboard array board[0] = the top rank which is 8
ranks = [RANK_8, RANK_7, RANK_6, RANK_5, RANK_4, RANK_3, RANK_2, RANK_1]

FILE_A = np.uint64(0b1000000010000000100000001000000010000000100000001000000010000000)
FILE_B = np.uint64(0b0100000001000000010000000100000001000000010000000100000001000000)
FILE_C = np.uint64(0b0010000000100000001000000010000000100000001000000010000000100000)
FILE_D = np.uint64(0b0001000000010000000100000001000000010000000100000001000000010000)
FILE_E = np.uint64(0b0000100000001000000010000000100000001000000010000000100000001000)
FILE_F = np.uint64(0b0000010000000100000001000000010000000100000001000000010000000100)
FILE_G = np.uint64(0b0000001000000010000000100000001000000010000000100000001000000010)
FILE_H = np.uint64(0b0000000100000001000000010000000100000001000000010000000100000001)

files = [FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H]

# Available bishop moves assuming an empty board for all 64 locations
# Computed with the ugly code outcommented below.
square_index_to_bishop_diagonals = np.array([
    np.uint64(0b0000000001000000001000000001000000001000000001000000001000000001),
    np.uint64(0b0000000010100000000100000000100000000100000000100000000100000000),
    np.uint64(0b0000000001010000100010000000010000000010000000010000000000000000),
    np.uint64(0b0000000000101000010001001000001000000001000000000000000000000000),
    np.uint64(0b0000000000010100001000100100000110000000000000000000000000000000),
    np.uint64(0b0000000000001010000100010010000001000000100000000000000000000000),
    np.uint64(0b0000000000000101000010000001000000100000010000001000000000000000),
    np.uint64(0b0000000000000010000001000000100000010000001000000100000010000000),
    np.uint64(0b0100000000000000010000000010000000010000000010000000010000000010),
    np.uint64(0b1010000000000000101000000001000000001000000001000000001000000001),
    np.uint64(0b0101000000000000010100001000100000000100000000100000000100000000),
    np.uint64(0b0010100000000000001010000100010010000010000000010000000000000000),
    np.uint64(0b0001010000000000000101000010001001000001100000000000000000000000),
    np.uint64(0b0000101000000000000010100001000100100000010000001000000000000000),
    np.uint64(0b0000010100000000000001010000100000010000001000000100000010000000),
    np.uint64(0b0000001000000000000000100000010000001000000100000010000001000000),
    np.uint64(0b0010000001000000000000000100000000100000000100000000100000000100),
    np.uint64(0b0001000010100000000000001010000000010000000010000000010000000010),
    np.uint64(0b1000100001010000000000000101000010001000000001000000001000000001),
    np.uint64(0b0100010000101000000000000010100001000100100000100000000100000000),
    np.uint64(0b0010001000010100000000000001010000100010010000011000000000000000),
    np.uint64(0b0001000100001010000000000000101000010001001000000100000010000000),
    np.uint64(0b0000100000000101000000000000010100001000000100000010000001000000),
    np.uint64(0b0000010000000010000000000000001000000100000010000001000000100000),
    np.uint64(0b0001000000100000010000000000000001000000001000000001000000001000),
    np.uint64(0b0000100000010000101000000000000010100000000100000000100000000100),
    np.uint64(0b0000010010001000010100000000000001010000100010000000010000000010),
    np.uint64(0b1000001001000100001010000000000000101000010001001000001000000001),
    np.uint64(0b0100000100100010000101000000000000010100001000100100000110000000),
    np.uint64(0b0010000000010001000010100000000000001010000100010010000001000000),
    np.uint64(0b0001000000001000000001010000000000000101000010000001000000100000),
    np.uint64(0b0000100000000100000000100000000000000010000001000000100000010000),
    np.uint64(0b0000100000010000001000000100000000000000010000000010000000010000),
    np.uint64(0b0000010000001000000100001010000000000000101000000001000000001000),
    np.uint64(0b0000001000000100100010000101000000000000010100001000100000000100),
    np.uint64(0b0000000110000010010001000010100000000000001010000100010010000010),
    np.uint64(0b1000000001000001001000100001010000000000000101000010001001000001),
    np.uint64(0b0100000000100000000100010000101000000000000010100001000100100000),
    np.uint64(0b0010000000010000000010000000010100000000000001010000100000010000),
    np.uint64(0b0001000000001000000001000000001000000000000000100000010000001000),
    np.uint64(0b0000010000001000000100000010000001000000000000000100000000100000),
    np.uint64(0b0000001000000100000010000001000010100000000000001010000000010000),
    np.uint64(0b0000000100000010000001001000100001010000000000000101000010001000),
    np.uint64(0b0000000000000001100000100100010000101000000000000010100001000100),
    np.uint64(0b0000000010000000010000010010001000010100000000000001010000100010),
    np.uint64(0b1000000001000000001000000001000100001010000000000000101000010001),
    np.uint64(0b0100000000100000000100000000100000000101000000000000010100001000),
    np.uint64(0b0010000000010000000010000000010000000010000000000000001000000100),
    np.uint64(0b0000001000000100000010000001000000100000010000000000000001000000),
    np.uint64(0b0000000100000010000001000000100000010000101000000000000010100000),
    np.uint64(0b0000000000000001000000100000010010001000010100000000000001010000),
    np.uint64(0b0000000000000000000000011000001001000100001010000000000000101000),
    np.uint64(0b0000000000000000100000000100000100100010000101000000000000010100),
    np.uint64(0b0000000010000000010000000010000000010001000010100000000000001010),
    np.uint64(0b1000000001000000001000000001000000001000000001010000000000000101),
    np.uint64(0b0100000000100000000100000000100000000100000000100000000000000010),
    np.uint64(0b0000000100000010000001000000100000010000001000000100000000000000),
    np.uint64(0b0000000000000001000000100000010000001000000100001010000000000000),
    np.uint64(0b0000000000000000000000010000001000000100100010000101000000000000),
    np.uint64(0b0000000000000000000000000000000110000010010001000010100000000000),
    np.uint64(0b0000000000000000000000001000000001000001001000100001010000000000),
    np.uint64(0b0000000000000000100000000100000000100000000100010000101000000000),
    np.uint64(0b0000000010000000010000000010000000010000000010000000010100000000),
    np.uint64(0b1000000001000000001000000001000000001000000001000000001000000000),
])


""""
import numpy as np


fill = 8 * [1]
crosses = [0 for _ in range(64)]


def array_to_bits(bit_array):
    # Pretty ugly but this is what I came up with
    bit_array = list(bit_array.astype(int).flatten())
    int_value = int("".join([str(i) for i in bit_array]), 2)
    return np.uint64(int_value)


for i in range(-7, 8):
    a = np.diag(fill, i)[:8, :8]
    for j in range(-7, 8):
        b = np.diag(fill, j)[:8, :8][::-1]

        both = a + b
        intersection = np.where(both == 2)
        row, col = intersection[0], intersection[1]
        if len(row) != 0:
            row, col = row[0], col[0]
            idx = row * 8 + col
            both[intersection] = 0
            crosses[idx] = both

for i in crosses:
    bits = array_to_bits(i)
    bit_string = "{0:b}".format(bits).zfill(64)
    print(bit_string)
"""
