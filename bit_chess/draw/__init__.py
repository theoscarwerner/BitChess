import pygame
import numpy as np
from board import Square, GameState
from utils import board_indices
from pieces import Knight, Rook, Bishop, Queen, King, Pawn


GAMESIZE = 480
PIECE_OFFSET = GAMESIZE / 8
RED = (255, 0, 0)


piece_images = {
    "P": pygame.image.load("draw/images/wp.png"),
    "p": pygame.image.load("draw/images/bp.png"),
    "R": pygame.image.load("draw/images/wR.png"),
    "r": pygame.image.load("draw/images/bR.png"),
    "N": pygame.image.load("draw/images/wN.png"),
    "n": pygame.image.load("draw/images/bN.png"),
    "B": pygame.image.load("draw/images/wB.png"),
    "b": pygame.image.load("draw/images/bB.png"),
    "Q": pygame.image.load("draw/images/wQ.png"),
    "q": pygame.image.load("draw/images/bQ.png"),
    "K": pygame.image.load("draw/images/wK.png"),
    "k": pygame.image.load("draw/images/bK.png"),
}


def get_piece_image(piece):
    if isinstance(piece, Knight):
        char = "N"
    elif isinstance(piece, King):
        char = "K"
    elif isinstance(piece, Queen):
        char = "Q"
    elif isinstance(piece, Pawn):
        char = "P"
    elif isinstance(piece, Bishop):
        char = "B"
    elif isinstance(piece, Rook):
        char = "R"
    else:
        raise "Can't detect piece."

    if piece.color == 0:
        char = char.lower()

    return piece_images[char]


screen = pygame.display.set_mode((GAMESIZE, GAMESIZE))
pygame.display.set_caption("Chess")


def create_board():
    board = pygame.image.load("draw/images/board.png").convert_alpha()
    board = pygame.transform.scale(board, (GAMESIZE, GAMESIZE))
    board.set_alpha(128)
    return board


board = create_board()


def draw_gamestate(gamestate: GameState):
    screen.fill("WHITE")
    screen.blit(board, (0, 0))

    for x, y in board_indices:
        piece = gamestate.get_piece_at(Square(index=(x, y)))
        if piece != 0:
            screen.blit(get_piece_image(piece), (y * PIECE_OFFSET, x * PIECE_OFFSET))

    pygame.display.update()


def highlight_coordinates(bits: np.uint64):
    bit_string = "{0:b}".format(bits).zfill(64)
    for bit, (x, y) in zip(bit_string, board_indices):
        if bit == "1":
            rect = (y * 60, x * 60, 60, 60)
            shape_surf = pygame.Surface(pygame.Rect(rect).size)
            shape_surf.set_alpha(128)
            pygame.draw.rect(shape_surf, RED, shape_surf.get_rect())
            screen.blit(shape_surf, rect)

    pygame.display.update()