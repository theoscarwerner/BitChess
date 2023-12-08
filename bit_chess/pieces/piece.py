class Piece:
    def __init__(self, color, char, idx):
        self.idx = idx
        self.color = color
        if color == 0:  # Black
            self.char = char.lower()
        elif color == 1:  # White
            self.char = char.upper()
        else:
            raise ValueError("Invalid color {color} passed. Excepted 0 or 1.".format(color=color))

    def is_same_type(self, other):
        # Check whether two Pieces are same type
        # Index in board position is static for piece_types
        # hence we can just check if they are equal
        return self.idx == other.idx