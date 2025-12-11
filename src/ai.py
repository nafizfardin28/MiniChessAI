import random
from constants import WHITE, BLACK, ROWS, COLS, PIECE_VALUES

def evaluate_board(board):
    """Simple evaluation: white positive, black negative."""
    score = 0
    for row in board:
        for piece in row:
            if piece:
                val = PIECE_VALUES[piece.type]
                score += val if piece.color == WHITE else -val
    return score

def generate_moves_limited(board, color, limit_per_piece=3):
    """Generate all valid moves, limit number of moves per piece."""
    moves = []
    for row in board:
        for piece in row:
            if piece and piece.color == color:
                valid = piece.get_valid_moves(board)
                if valid:
                    # Randomly select a few moves to limit branching
                    if len(valid) > limit_per_piece:
                        valid = random.sample(valid, limit_per_piece)
                    for move in valid:
                        moves.append((piece, move))
    return moves

def ai_best_move(board):
    """Return best move for AI (Black) using depth=1 evaluation."""
    best_score = float('inf')
    best_move = None

    moves = generate_moves_limited(board, BLACK)
    for piece, (r, c) in moves:
        # simulate move in-place
        orig_piece = board[r][c]
        orig_row, orig_col = piece.row, piece.col
        board[orig_row][orig_col] = None
        board[r][c] = piece
        piece.row, piece.col = r, c

        score = evaluate_board(board)

        # revert move
        piece.row, piece.col = orig_row, orig_col
        board[orig_row][orig_col] = piece
        board[r][c] = orig_piece

        if score < best_score:
            best_score = score
            best_move = (piece, (r, c))

    return best_move
