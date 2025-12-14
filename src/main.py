import pygame
import sys
import os
import math
from constants import ASSETS_DIR
from board import Board
from constants import *
from board import Board, ASSETS_DIR
from ai import ai_best_move   # your AI function

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("6x5 Minichess")

FONT_BIG = pygame.font.SysFont(None, 40)
FONT_MD = pygame.font.SysFont(None, 24)


def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None, None


def draw_button(win, rect, text, font, hover_color, default_color):
    mx, my = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mx, my) else default_color
    pygame.draw.rect(win, color, rect, border_radius=10)
    txt = font.render(text, True, (255, 255, 255))
    txt_rect = txt.get_rect(center=rect.center)
    win.blit(txt, txt_rect)


def main_menu():
    button_w, button_h = 260, 80
    start_rect = pygame.Rect(WIDTH//2 - button_w//2, HEIGHT//2 - 60, button_w, button_h)
    quit_rect = pygame.Rect(WIDTH//2 - button_w//2, HEIGHT//2 + 40, button_w, button_h)

    while True:
        WIN.fill((28, 30, 34))

        # Title
        title = FONT_BIG.render("Minichess 6×5", True, (240, 240, 240))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 60))

        # Info
        info = FONT_MD.render("Play vs Computer. Press Start to play.", True, (200, 200, 200))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, 150))

        draw_button(WIN, start_rect, "Start Game", FONT_MD, (0, 180, 0), (0, 140, 0))
        draw_button(WIN, quit_rect, "Quit", FONT_MD, (180, 0, 0), (140, 0, 0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_rect.collidepoint(mx, my):
                    game_loop()
                    return
                if quit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()


def promote_piece_image(piece):
    """Promotes a pawn to a queen"""
    img_name = 'white_queen.png' if piece.color == WHITE else 'black_queen.png'
    path = os.path.join(ASSETS_DIR, img_name)
    piece.type = 'queen'
    piece.image = pygame.image.load(path).convert_alpha()
    piece.image = pygame.transform.smoothscale(piece.image, (SQUARE_SIZE, SQUARE_SIZE))


def animate_move(board_obj, moving_piece, src, dst, duration_ms=180):
    """Animate piece sliding from src to dst"""
    clock = pygame.time.Clock()
    start_x = src[1] * SQUARE_SIZE
    start_y = src[0] * SQUARE_SIZE
    end_x = dst[1] * SQUARE_SIZE
    end_y = dst[0] * SQUARE_SIZE
    elapsed = 0
    while elapsed < duration_ms:
        dt = clock.tick(60)
        elapsed += dt
        t = min(1.0, elapsed / duration_ms)
        t_eased = -0.5 * (math.cos(math.pi * t) - 1)
        cur_x = start_x + (end_x - start_x) * t_eased
        cur_y = start_y + (end_y - start_y) * t_eased

        WIN.fill((0, 0, 0))
        board_obj.draw(WIN)
        WIN.blit(moving_piece.image, (cur_x, cur_y))
        pygame.display.update()


def game_loop():
    board_obj = Board()
    selected = None
    valid_moves = []
    human_color = WHITE
    ai_color = BLACK
    turn = WHITE
    clock = pygame.time.Clock()
    game_over = False
    MOVE_SOUND_PATH = os.path.join(ASSETS_DIR, "click.wav")
    move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)

    while True:
        clock.tick(60)
        moved_piece = None  # <-- reset every frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Human move
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and turn == human_color:
                row, col = get_square_under_mouse()
                if row is None:
                    continue
                clicked = board_obj.board[row][col]

                if clicked and clicked.color == human_color:
                    selected = clicked
                    valid_moves = selected.get_valid_moves(board_obj.board)

                elif selected and (row, col) in valid_moves:
                    src = (selected.row, selected.col)
                    dst = (row, col)
                    moved_piece, captured = board_obj.move_piece(src[0], src[1], dst[0], dst[1])
                    animate_move(board_obj, moved_piece, src, dst, 200)
                    move_sound.play()

                    # Pawn promotion
                    if moved_piece.type == "pawn":
                        if (moved_piece.color == WHITE and moved_piece.row == 0) or \
                           (moved_piece.color == BLACK and moved_piece.row == ROWS - 1):
                            promote_piece_image(moved_piece)

                    selected = None
                    valid_moves = []
                    turn = ai_color

        # AI move
        if not game_over and turn == ai_color:
            pygame.time.delay(300)  # simulate thinking
            move = ai_best_move(board_obj)
            if move:
                piece_obj, (r, c) = move
                src = (piece_obj.row, piece_obj.col)
                dst = (r, c)
                moved_piece, captured = board_obj.move_piece(src[0], src[1], dst[0], dst[1])
                animate_move(board_obj, moved_piece, src, dst, 400)
                move_sound.play()

                # Pawn promotion
                if moved_piece.type == "pawn":
                    if (moved_piece.color == WHITE and moved_piece.row == 0) or \
                       (moved_piece.color == BLACK and moved_piece.row == ROWS - 1):
                        promote_piece_image(moved_piece)

            turn = human_color

        # Check for checkmate
        if not game_over:
            if board_obj.is_checkmate(WHITE):
                game_over = True
                winner_text = "BLACK WINS!"
            elif board_obj.is_checkmate(BLACK):
                game_over = True
                winner_text = "WHITE WINS!"

        # Draw everything
        WIN.fill((0, 0, 0))
        board_obj.draw(WIN,
            highlight=(selected.row, selected.col) if selected else None,
            highlight_moves=valid_moves
        )

        # Show turn
        turn_text = FONT_BIG.render(
            f"Turn: {'White (You)' if turn == WHITE else 'Black (AI)'}",
            True, (240, 240, 240)
        )
        WIN.blit(turn_text, (8, HEIGHT - 40))

        # Show checkmate
        if game_over:
            msg = FONT_BIG.render(f"CHECKMATE! {winner_text}", True, (255, 0, 0))
            WIN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))

        pygame.display.update()




if __name__ == "__main__":
    main_menu()
