import numpy as np


index_changes_when_move = np.array([
    [1, 1], [-1, 1], [-1, -1], [1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]])


def compute_bits(current_coordinates):
    # Get indexes of places knight can move
    available_coordinates = current_coordinates + index_changes_when_move

    # Remove out of bounds
    out_of_bounds = np.where((available_coordinates > 7) | (available_coordinates < 0))
    valid_moves = np.delete(available_coordinates, out_of_bounds[0], axis=0)

    # Convert to binary
    bit_array = np.zeros((8, 8))
    bit_array[valid_moves[:, 0], valid_moves[:, 1]] = 1
    bit_string = "".join(map(str, bit_array.flatten().astype(int)))
    bits = np.uint64(int(bit_string, 2))
    return bits


def compute_king_moves_array():
    """
    Creates precomputed available knight moves in bits from any of the 64 positions.
    For example, given a knight on g1 (corresponding to square index 62) you can retrieve
    (non-filtered) available squares with precomputed_moves[53] which results in following bits:

        8 | 0  0  0  0  0  0  0  0
        7 | 0  0  0  0  0  0  0  0
        6 | 0  0  0  0  0  0  0  0
        5 | 0  0  0  0  0  0  0  0
        4 | 0  0  0  0  0  0  0  0
        3 | 0  0  0  0  1  1  1  0
        2 | 0  0  0  0  1  0  1  0
        1 | 0  0  0  0  1  1  1  0
            ----------------------
            a  b  c  d  e  f  g  h
    """
    knight_moves = []

    # Loop over the 64 squares
    for i in range(0, 8):
        for j in range(0, 8):
            bits = compute_bits((i, j))
            knight_moves.append(bits)

    return np.array(knight_moves)


precomputed_moves = compute_king_moves_array()
