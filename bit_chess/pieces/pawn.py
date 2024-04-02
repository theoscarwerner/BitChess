from pieces.piece import Piece
import numpy as np


class Pawn(Piece):
    def __init__(self, color):
        self.idx = 2
        self.color = color

    def get_valid_moves(self, square, gamestate):

        # TODO: EN PASSANT
        color = gamestate.get_square_color(square)

        # White
        if color == 1:
            start_rank = 6
            one_forward = square.bits << np.uint64(8)
            two_forward = square.bits << np.uint64(16)
            captures = ((square.bits << np.uint64(7))
                        | (square.bits << np.uint64(9)))
        # Black
        else:
            start_rank = 1
            one_forward = square.bits >> np.uint64(8)
            two_forward = square.bits >> np.uint64(16)
            captures = ((square.bits >> np.uint64(7))
                        | (square.bits >> np.uint64(9)))

        valid_moves = ((one_forward & ~gamestate.board[-1])
                       | (captures & gamestate.board[color ^ 1]))

        # Check two_square forward is empty step up
        if (square.get_rank() == start_rank and two_forward & gamestate.board[8] == 0):
            valid_moves = valid_moves | two_forward

        return valid_moves
