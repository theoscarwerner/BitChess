import pickle
import tqdm
import numpy as np
from square import Square, iter_squares
from utils.casting import array_to_bits, bits_to_array
from utils import board_indices
from constants import square_index_to_bishop_diagonals


def compute_available_moves(blockers_bit_array, square):
    """
        Given the blockers and the square the rook is on we loop
       in each direction to and add it as moves until a piece is hit.
    """
    row = square.square_index // 8
    col = square.square_index % 8
    available_moves = np.zeros((8, 8)).astype(int)
    # Move upwards right

    path = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
    index_changes_when_move = np.array([
        path * [-1, -1],
        path * [-1, 1],
        path * [1, -1],
        path * [1, 1],
    ])

    available_coordinates = index_changes_when_move + np.array([row, col])
    for direction in available_coordinates:
        for coordinate in direction:
            row, col = coordinate[0], coordinate[1]
            if not all((coordinate < 8) & (coordinate >= 0)):
                break

            available_moves[row][col] = 1
            if blockers_bit_array[row][col] == 1:
                # break_ = True
                break

    return array_to_bits(available_moves)


def get_piece_blockers(diagonals_array):
    """
    Given a cross bitboard array, yields all permutations of pieces possible
    along the cross.
    """
    count_moveable_squares = diagonals_array.sum()

    moveable_squares = np.where(diagonals_array == 1)

    for i in range(2**count_moveable_squares):
        blocker_bits = list(map(int, list("{0:b}".format(i).zfill(count_moveable_squares))))
        blockers_bit_array = np.zeros((8, 8))
        blockers_bit_array[moveable_squares] = blocker_bits
        yield blockers_bit_array


def compute_all_bishop_moves():
    """
        TODO: Proper Docstring
        TODO: Magic bitboards for more efficient lookup :D

        Returns a dict of the form:
        {
            (square.bits, blocker_bits): available_moves_bits
        }
    """
    precomputed_moves = {}

    for square in tqdm.tqdm(iter_squares()):

        diagonals_bits = square_index_to_bishop_diagonals[square.square_index]
        diagonals_array = bits_to_array(diagonals_bits)

        for blockers_bit_array in get_piece_blockers(diagonals_array):
            available_moves_bits = compute_available_moves(blockers_bit_array, square)
            blocker_bit_board = array_to_bits(blockers_bit_array)
            precomputed_moves[(square.bits, blocker_bit_board)] = available_moves_bits

    return precomputed_moves


# precomputed_moves = compute_all_bishop_moves()
# with open("precomputations/files/bishop_moves.p", "wb") as f:
#     pickle.dump(precomputed_moves, f)

with open("precomputations/files/bishop_moves.p", "rb") as f:
    precomputed_moves = pickle.load(f)