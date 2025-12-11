import pygame
from constants import *

class Piece:
    def __init__(self, row, col, color, type_, image_file):
        """
        type_: 'pawn','rook','knight','bishop','queen','king'
        image_file: absolute path to PNG
        """
        self.row = row
        self.col = col
        self.color = color
        self.type = type_
        self.image_file = image_file  # store the file path
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SQUARE_SIZE, SQUARE_SIZE))

    def clone(self):
        # Create a new Piece with the same properties
        from piece import Piece
        new_piece = Piece(self.row, self.col, self.color, self.type, self.image_file)
        return new_piece

    def draw(self, win):
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE
        win.blit(self.image, (x, y))

    def get_valid_moves(self, board):
        moves = []
        if self.type == "pawn":
            direction = -1 if self.color == WHITE else 1
            r = self.row + direction
            if 0 <= r < ROWS:
                if board[r][self.col] is None:
                    moves.append((r, self.col))
            for dc in (-1, 1):
                c = self.col + dc
                r = self.row + direction
                if 0 <= r < ROWS and 0 <= c < COLS:
                    target = board[r][c]
                    if target is not None and target.color != self.color:
                        moves.append((r, c))

        elif self.type in ["rook", "bishop", "queen"]:
            directions = []
            if self.type in ["rook", "queen"]:
                directions += [(1,0),(-1,0),(0,1),(0,-1)]
            if self.type in ["bishop", "queen"]:
                directions += [(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr, dc in directions:
                r, c = self.row + dr, self.col + dc
                while 0 <= r < ROWS and 0 <= c < COLS:
                    target = board[r][c]
                    if target is None:
                        moves.append((r, c))
                    else:
                        if target.color != self.color:
                            moves.append((r, c))
                        break
                    r += dr; c += dc

        elif self.type == "king":
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0: continue
                    r, c = self.row + dr, self.col + dc
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        target = board[r][c]
                        if target is None or target.color != self.color:
                            moves.append((r, c))

        elif self.type == "knight":
            offsets = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
            for dr, dc in offsets:
                r, c = self.row + dr, self.col + dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    target = board[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))

        return moves
