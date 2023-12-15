from square import Square


def get_cross_bitboard(square: Square):
    """
    Computes the bitboard of all reachable position from square
    assuming there are no pieces on the board. E.g a rook on d5 would return
    bits corresponding to the following:

        8 | 0  0  0  1  0  0  0  0
        7 | 0  0  0  1  0  0  0  0
        6 | 0  0  0  1  0  0  0  0
        5 | 1  1  1  0  1  1  1  1
        4 | 0  0  0  1  0  0  0  0
        3 | 0  0  0  1  0  0  0  0
        2 | 0  0  0  1  0  0  0  0
        1 | 0  0  0  1  0  0  0  0
            ----------------------
            a  b  c  d  e  f  g  h
    """

    return (square.get_rank_bits() | square.get_file_bits()) & ~square.bits

