import os
import pygame
from constants import *
from piece import Piece

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
ASSETS_DIR = os.path.abspath(ASSETS_DIR)

class Board:
    HIGHLIGHT_COLOR = (255, 255, 0, 120)  # yellow overlay
    MOVE_COLOR = (0, 255, 0, 120)         # green overlay
    AI_COLOR = (255, 0, 0, 120)           # red overlay

    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.captured_white = []
        self.captured_black = []
        self.create_board()

    def create_board(self):
        # Black back row
        self.board[0] = [
            Piece(0,0,BLACK,"rook",os.path.join(ASSETS_DIR,'black_rook.png')),
            Piece(0,1,BLACK,"knight",os.path.join(ASSETS_DIR,'black_knight.png')),
            Piece(0,2,BLACK,"bishop",os.path.join(ASSETS_DIR,'black_bishop.png')),
            Piece(0,3,BLACK,"king",os.path.join(ASSETS_DIR,'black_king.png')),
            Piece(0,4,BLACK,"queen",os.path.join(ASSETS_DIR,'black_queen.png')),
        ]
        # Black pawns
        for c in range(COLS):
            self.board[1][c] = Piece(1,c,BLACK,"pawn",os.path.join(ASSETS_DIR,'black_pawn.png'))

        # White pawns
        for c in range(COLS):
            self.board[4][c] = Piece(4,c,WHITE,"pawn",os.path.join(ASSETS_DIR,'white_pawn.png'))

        # White back row
        self.board[5] = [
            Piece(5,0,WHITE,"rook",os.path.join(ASSETS_DIR,'white_rook.png')),
            Piece(5,1,WHITE,"knight",os.path.join(ASSETS_DIR,'white_knight.png')),
            Piece(5,2,WHITE,"bishop",os.path.join(ASSETS_DIR,'white_bishop.png')),
            Piece(5,3,WHITE,"king",os.path.join(ASSETS_DIR,'white_king.png')),
            Piece(5,4,WHITE,"queen",os.path.join(ASSETS_DIR,'white_queen.png')),
        ]

    def move_piece(self, src_r, src_c, dst_r, dst_c):
        piece = self.board[src_r][src_c]
        if piece is None:
            return None, None
        captured = self.board[dst_r][dst_c]
        self.board[dst_r][dst_c] = piece
        self.board[src_r][src_c] = None
        piece.row, piece.col = dst_r, dst_c

        if captured:
            cap_clone = captured.clone()
            if captured.color == WHITE:
                self.captured_white.append(cap_clone)
            else:
                self.captured_black.append(cap_clone)
        return piece, captured

    def is_king_alive(self, color):
        for row in self.board:
            for p in row:
                if p and p.color == color and p.type == "king":
                    return True
        return False

    # check/checkmate helpers
    def find_king(self, color):
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.type == "king" and p.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return True
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color != color:
                    if king_pos in p.get_valid_moves(self.board):
                        return True
        return False

    def has_legal_moves(self, color):
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p and p.color == color:
                    for move in p.get_valid_moves(self.board):
                        backup = self.board[move[0]][move[1]]
                        self.board[p.row][p.col] = None
                        self.board[move[0]][move[1]] = p
                        old_r, old_c = p.row, p.col
                        p.row, p.col = move

                        safe = not self.is_in_check(color)

                        p.row, p.col = old_r, old_c
                        self.board[old_r][old_c] = p
                        self.board[move[0]][move[1]] = backup

                        if safe:
                            return True
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_legal_moves(color)

    # draw board and highlights
    def draw(self, win, highlight=None, highlight_moves=None, ai_move=None):
        for r in range(ROWS):
            for c in range(COLS):
                color = LIGHT if (r+c)%2==0 else DARK
                pygame.draw.rect(win, color, (c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

        if highlight:
            hr,hc = highlight
            s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT_COLOR)
            win.blit(s,(hc*SQUARE_SIZE, hr*SQUARE_SIZE))

        if highlight_moves:
            for r,c in highlight_moves:
                s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
                s.fill(self.MOVE_COLOR)
                win.blit(s,(c*SQUARE_SIZE,r*SQUARE_SIZE))

        if ai_move:
            r,c = ai_move
            s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(self.AI_COLOR)
            win.blit(s,(c*SQUARE_SIZE,r*SQUARE_SIZE))

        # draw pieces
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece:
                    piece.draw(win)
