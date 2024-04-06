import pygame
import sys
import time
from pymongo import MongoClient
from collections import namedtuple
import threading

# Initialize Pygame font module
pygame.font.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (65, 105, 225)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Define font
FONT = pygame.font.Font(None, 36)

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.eight_queens_puzzle

# Define board size
BOARD_SIZE = 8
SQUARE_SIZE = 0

# Define solutions
solutions = []
max_solutions = 92
solved_solutions = []

# Create a namedtuple to store board positions
Position = namedtuple('Position', ['row', 'col'])

def input_text(prompt, board):
    text = ""
    input_rect = pygame.Rect(240, 200, 320, 50)
    active = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        return text
                    else:
                        text += event.unicode

        SCREEN.fill(WHITE)
        draw_board()
        draw_queens(board)

        prompt_text = FONT.render(prompt, True, BLACK)
        SCREEN.blit(prompt_text, (240, 150))

        color = BLACK if active else GRAY
        pygame.draw.rect(SCREEN, color, input_rect, 2)
        text_surface = FONT.render(text, True, BLACK)
        SCREEN.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        pygame.display.update()

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(
                SCREEN,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                border_radius=5,
            )

def draw_queens(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(SCREEN, BLUE, (x, y), SQUARE_SIZE // 4)

def is_safe(board, position):
    # Check row
    if 1 in board[position.row]:
        return False

    # Check column
    if any(row[position.col] == 1 for row in board):
        return False

    # Check upper-left diagonal
    for i, j in zip(range(position.row, -1, -1), range(position.col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check upper-right diagonal
    for i, j in zip(range(position.row, -1, -1), range(position.col, BOARD_SIZE)):
        if board[i][j] == 1:
            return False

    return True

def solve_queens_threaded(board, col, solutions):
    if col == BOARD_SIZE:
        solutions.append([row[:] for row in board])
        return True

    result = False
    threads = []
    for row in range(BOARD_SIZE):
        position = Position(row, col)
        if is_safe(board, position):
            new_board = [row[:] for row in board]
            new_board[row][col] = 1
            thread = threading.Thread(target=solve_queens_threaded, args=(new_board, col + 1, solutions))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    return any(solutions)

def solve_queens(board, col):
    global solutions
    solutions = []
    solve_queens_threaded(board, col, solutions)

def display_message(text, color):
    message = FONT.render(text, True, color)
    message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    pygame.draw.rect(SCREEN, WHITE, message_rect.inflate(10, 10))
    SCREEN.blit(message, message_rect)
    pygame.display.update()
    time.sleep(0.5)
def handle_input(board):
    global solutions, solved_solutions
    queens_placed = sum(sum(row) for row in board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE
            position = Position(row, col)
            if board[row][col] == 0 and is_safe(board, position):
                board[row][col] = 1
                solutions = []
                solve_queens(board, 0)
                queens_placed += 1
                if queens_placed == BOARD_SIZE:
                    if len(solutions) == max_solutions:
                        display_message("Congratulations! You've found all solutions.", BLUE)
                        solved_solutions.clear()  # Clear the list of solved solutions
                    else:
                        board_str = ''.join(map(str, sum(board, [])))
                        if board_str in [s[0] for s in solved_solutions]:
                            display_message("This solution has already been solved. Try again!", RED)
                        else:
                            display_message("Solution accepted! Player: " + player_name, ORANGE)
                            solved_solutions.append((board_str, player_name))
                            # Save player name along with the correct response in the database
                            collection.insert_one({"player_name": player_name, "solution": board_str})
            else:
                board[row][col] = 0
                solutions = []

def initialize_module(main_window):
    global SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, player_name
    SCREEN = main_window
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
    global SQUARE_SIZE
    SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE
    player_name = input_text("Enter your name: ", [[0]*8]*8)

def run_eight_queens(window):
    initialize_module(window)

    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        SCREEN.fill(WHITE)
        draw_board()
        draw_queens(board)
        handle_input(board)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Eight Queens Puzzle")
    run_eight_queens(SCREEN)