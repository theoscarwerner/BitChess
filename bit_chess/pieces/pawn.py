from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "P", 2)
