# constants.py

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROWS = 6
COLS = 5
SQUARE_SIZE = 100  # adjust based on your UI
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

# Colors for drawing squares
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

# Piece values for AI evaluation
PIECE_VALUES = {
    "pawn": 1,
    "rook": 5,
    "knight": 3,
    "bishop": 3,
    "queen": 9,
    "king": 100
}
