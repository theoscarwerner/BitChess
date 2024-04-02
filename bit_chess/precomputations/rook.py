import pickle
import tqdm
import numpy as np
from square import Square
from utils.casting import array_to_bits, bits_to_array
from utils import board_indices
from utils.bit_manipulation import get_cross_bitboard


def compute_available_moves(blockers_bit_array, square):
    """
        Given the blockers and the square the rook is on we loop
       in each direction to and add it as moves until a piece is hit.
    """

    row = square.square_index // 8
    col = square.square_index % 8
    available_moves = np.zeros((8, 8)).astype(int)
    # Move upwards
    for i in range(row - 1, -1, -1):
        available_moves[i][col] = 1

        # We only break after adding the move and assume all pieces are enemy color
        # (i.e we add the move because it's a capture)
        # We filter this later to remove the moves that hit same color
        if blockers_bit_array[i][col] == 1:
            break

    # Move right
    for i in range(col + 1, 8):
        available_moves[row][i] = 1
        if blockers_bit_array[row][i] == 1:
            break

    # Move downwards
    for i in range(row + 1, 8):
        available_moves[i][col] = 1
        if blockers_bit_array[i][col] == 1:
            break

    # Move left
    for i in range(col - 1, -1, -1):
        available_moves[row][i] = 1
        if blockers_bit_array[row][i] == 1:
            break

    return array_to_bits(available_moves)


def get_piece_blockers(cross_array):
    """
    Given a cross bitboard array, yields all permutations of pieces possible
    along the cross.
    """
    count_moveable_squares = 14

    moveable_squares = np.where(cross_array == 1)

    for i in range(2**count_moveable_squares):
        blocker_bits = list(map(int, list("{0:b}".format(i).zfill(count_moveable_squares))))
        blockers_bit_array = np.zeros((8, 8))
        blockers_bit_array[moveable_squares] = blocker_bits
        yield blockers_bit_array


def compute_all_rook_moves():
    """
        TODO: Proper Docstring
        TODO: Magic bitboards for more efficient lookup :D

        Returns a dict of the form:
        {
            (square.bits, blocker_bits): available_moves_bits
        }
    """
    precomputed_moves = {}

    # Looping over [(0, 0), (0, 1), ...,(7, 6) (7, 7)]
    for board_idx in tqdm.tqdm(board_indices):
        square = Square(index=board_idx)
        cross_bitboard = get_cross_bitboard(square)
        cross_array = bits_to_array(cross_bitboard)
        for blockers_bit_array in get_piece_blockers(cross_array):
            available_moves_bits = compute_available_moves(blockers_bit_array, square)

            blocker_bit_board = array_to_bits(blockers_bit_array)
            precomputed_moves[(square.bits, blocker_bit_board)] = available_moves_bits

    return precomputed_moves


# precomputed_moves = compute_all_rook_moves()
# with open("precomputations/files/rook_moves.p", "wb") as f:
#     pickle.dump(precomputed_moves, f)

with open("precomputations/files/rook_moves.p", "rb") as f:
    precomputed_moves = pickle.load(f)