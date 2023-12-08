import pygame
import math
import numpy as np
import draw
from draw import GAMESIZE, PIECE_OFFSET
from board import GameState, Square



x_to_rank = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
y_to_row = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}


def translate_move(from_square, to_square):
    from_move_translation = "{row}{rank}".format(
        rank=y_to_row[from_square[0]], row=x_to_rank[from_square[1]])

    to_move_translation = "{row}{rank}".format(
        rank=y_to_row[to_square[0]], row=x_to_rank[to_square[1]])

    translation = f"{from_move_translation} -> {to_move_translation}"
    print(translation)
    return translation


def to_square_index(pos):
    return (math.floor(pos[1] / PIECE_OFFSET), math.floor(pos[0] / PIECE_OFFSET))


def get_clicked_square(click_position):
    board_index = (math.floor(click_position[1] / PIECE_OFFSET),
                   math.floor(click_position[0] / PIECE_OFFSET))
    return Square(index=board_index)


class Main():
    def __init__(self):
        # self.board = Board(GAMESIZE, PIECE_OFFSET)
        self.gamestate = GameState()

        draw.draw_gamestate(self.gamestate)

    def run(self):
        first_click = True
        from_square, to_square = False, False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if first_click:
                        click_position = pygame.mouse.get_pos()
                        from_square = get_clicked_square(click_position)

                        piece = self.gamestate.get_piece_at(from_square)

                        # If not clicked a piece
                        if piece == 0:
                            from_square = False
                            continue

                        move_bits = piece.get_valid_moves(from_square, self.gamestate)

                        # If there are valid moves
                        if move_bits != 0:
                            draw.highlight_coordinates(move_bits)

                        first_click = False

                    # Second click
                    else:
                        click_position = pygame.mouse.get_pos()
                        to_square = get_clicked_square(click_position)
                        first_click = True

            # If piece has been clicked and the square to move to has been clicked,
            # and they're not the same square
            if from_square and to_square and from_square != to_square:
                if to_square.bits & move_bits != 0:
                    print("Valid!")
                    self.gamestate.update(piece, from_square, to_square)
                    # self.board.draw_gamestate(self.gamestate, self.screen)

                    from_square, to_square = False, False

                    # print(self.gamestate.evaluate())

                else:
                    print("Invalid Move!")

                # self.board.draw_gamestate(self.gamestate, self.screen)
                from_square, to_square = False, False
                # opponent_move = self.opponent.search_move(self.gamestate)
                # self.gamestate.move(*opponent_move)
                draw.draw_gamestate(self.gamestate)


if __name__ == '__main__':
    main = Main()
    main.run()
