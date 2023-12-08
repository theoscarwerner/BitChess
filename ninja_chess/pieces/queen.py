from pieces.piece import Piece


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "Q", 6)
