import math
from constants import *
from board import Board

MAX_DEPTH = 2

def evaluate(board):
    score = 0
    for row in board:
        for p in row:
            if p:
                val = PIECE_VALUES[p.type]
                score += val if p.color == WHITE else -val
    return score

def minimax(board_obj, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate(board_obj.board), None

    color = WHITE if maximizing else BLACK

    if board_obj.is_checkmate(color):
        return (-9999 if maximizing else 9999), None

    best_move = None

    for r in range(ROWS):
        for c in range(COLS):
            p = board_obj.board[r][c]
            if p and p.color == color:
                for move in p.get_valid_moves(board_obj.board):
                    backup = board_obj.board[move[0]][move[1]]
                    board_obj.board[r][c] = None
                    board_obj.board[move[0]][move[1]] = p
                    old = (p.row, p.col)
                    p.row, p.col = move

                    score, _ = minimax(board_obj, depth-1, alpha, beta, not maximizing)

                    p.row, p.col = old
                    board_obj.board[r][c] = p
                    board_obj.board[move[0]][move[1]] = backup

                    if maximizing:
                        if score > alpha:
                            alpha = score
                            best_move = (p, move)
                    else:
                        if score < beta:
                            beta = score
                            best_move = (p, move)

                    if beta <= alpha:
                        return (alpha if maximizing else beta), best_move

    return (alpha if maximizing else beta), best_move

def ai_best_move(board_obj):
    _, move = minimax(board_obj, MAX_DEPTH, -math.inf, math.inf, False)
    return move
