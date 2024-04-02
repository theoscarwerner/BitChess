class Piece:
    def is_same_type(self, other):
        # Check whether two Pieces are same type
        # Index in board position is static for piece_types
        # hence we can just check if they are equal
        return self.idx == other.idx

    def get_valid_moves(self, square, gamestate):
        raise NotImplementedError