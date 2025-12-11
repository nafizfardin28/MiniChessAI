import os
import pygame
from constants import *
from piece import Piece


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
ASSETS_DIR = os.path.abspath(ASSETS_DIR)


class Board:
    HIGHLIGHT_COLOR = (255, 255, 0, 120)      # yellow
    MOVE_COLOR = (0, 255, 0, 120)             # green
    AI_COLOR = (255, 0, 0, 120)               # red

    def __init__(self):
        self.board = []
        self.captured_white = []
        self.captured_black = []
        self.create_board()

    def create_board(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # Black pieces
        self.board[0] = [
            Piece(0, 0, BLACK, "rook",   os.path.join(ASSETS_DIR, "black_rook.png")),
            Piece(0, 1, BLACK, "knight", os.path.join(ASSETS_DIR, "black_knight.png")),
            Piece(0, 2, BLACK, "bishop", os.path.join(ASSETS_DIR, "black_bishop.png")),
            Piece(0, 3, BLACK, "king",   os.path.join(ASSETS_DIR, "black_king.png")),
            Piece(0, 4, BLACK, "queen",  os.path.join(ASSETS_DIR, "black_queen.png")),
        ]

        for col in range(COLS):
            self.board[1][col] = Piece(1, col, BLACK, "pawn",
                                       os.path.join(ASSETS_DIR, "black_pawn.png"))

        # White pieces
        for col in range(COLS):
            self.board[4][col] = Piece(4, col, WHITE, "pawn",
                                       os.path.join(ASSETS_DIR, "white_pawn.png"))

        self.board[5] = [
            Piece(5, 0, WHITE, "rook",   os.path.join(ASSETS_DIR, "white_rook.png")),
            Piece(5, 1, WHITE, "knight", os.path.join(ASSETS_DIR, "white_knight.png")),
            Piece(5, 2, WHITE, "bishop", os.path.join(ASSETS_DIR, "white_bishop.png")),
            Piece(5, 3, WHITE, "king",   os.path.join(ASSETS_DIR, "white_king.png")),
            Piece(5, 4, WHITE, "queen",  os.path.join(ASSETS_DIR, "white_queen.png")),
        ]

    def move_piece(self, src_r, src_c, dst_r, dst_c):
        piece = self.board[src_r][src_c]
        if piece is None:
            return None, None

        captured = self.board[dst_r][dst_c]

        # perform move
        self.board[dst_r][dst_c] = piece
        self.board[src_r][src_c] = None
        piece.row, piece.col = dst_r, dst_c

        # record captured clone
        if captured:
            clone_cap = captured.clone()
            if captured.color == WHITE:
                self.captured_white.append(clone_cap)
            else:
                self.captured_black.append(clone_cap)

        return piece, captured

    def draw(self, win, highlight=None, highlight_moves=None, ai_move=None):

        # board squares
        for r in range(ROWS):
            for c in range(COLS):
                color = LIGHT if (r + c) % 2 == 0 else DARK
                pygame.draw.rect(win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # highlight selected piece
        if highlight:
            hr, hc = highlight
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT_COLOR)
            win.blit(s, (hc * SQUARE_SIZE, hr * SQUARE_SIZE))

        # highlight valid moves
        if highlight_moves:
            for (r, c) in highlight_moves:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill(self.MOVE_COLOR)
                win.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        # highlight AI last move
        if ai_move:
            r, c = ai_move
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(self.AI_COLOR)
            win.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        # draw pieces
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece:
                    piece.draw(win)
