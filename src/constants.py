# constants.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
ASSETS_DIR = os.path.abspath(ASSETS_DIR)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROWS = 6
COLS = 5
SQUARE_SIZE = 100

WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE + 40

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

PIECE_VALUES = {
    "pawn": 1,
    "rook": 5,
    "knight": 3,
    "bishop": 3,
    "queen": 9,
    "king": 1000
}
