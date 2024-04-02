
def is_in_check(gamestate, moved_piece, piece_moved_to_square):
    return (
        (
            moved_piece.get_valid_moves(piece_moved_to_square, gamestate)
            & gamestate.board[moved_piece.color ^ 1]
            & gamestate.board[7]
        ) != 0
    )
