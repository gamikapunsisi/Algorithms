import pygame
import sys
import math
from datetime import datetime
from pymongo import MongoClient

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

# Define colors
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
X_COLOR = (247, 185, 0)  # Yellow
O_COLOR = (0, 187, 211)  # Cyan
WINNER_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (0, 0, 0)
INPUT_COLOR = (255, 255, 255)  # White
INPUT_BORDER_COLOR = (100, 100, 100)
SHADOW_COLOR = (200, 200, 200)

# Define the game board
board = [' ' for _ in range(9)]

# Define the players
HUMAN = 'X'
COMPUTER = 'O'

# Define the game state
GAME_OVER = False
WINNER = None

# Define the font
FONT = pygame.font.SysFont("Arial", 72)  
SMALL_FONT = pygame.font.SysFont("Arial", 36)  

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.tik_tak_toe

# Function to draw the game board
def draw_board():
    WINDOW.fill(BACKGROUND_COLOR)
    cell_width = WINDOW_SIZE[0] // 3
    cell_height = WINDOW_SIZE[1] // 3

    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(WINDOW, GRID_COLOR, (i * cell_width, 0), (i * cell_width, WINDOW_SIZE[1]), 5)

    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw.line(WINDOW, GRID_COLOR, (0, i * cell_height), (WINDOW_SIZE[0], i * cell_height), 5)

    # Draw X's and O's
    for i in range(9):
        x = (i % 3) * cell_width + cell_width // 2
        y = (i // 3) * cell_height + cell_height // 2
        if board[i] == 'X':
            draw_x(x, y, X_COLOR, cell_width, cell_height)
        elif board[i] == 'O':
            draw_o(x, y, O_COLOR)

# Function to draw an X
def draw_x(x, y, color, cell_width, cell_height):
    line_width = 18
    pygame.draw.line(WINDOW, color, (x - cell_width // 3, y - cell_height // 3), (x + cell_width // 3, y + cell_height // 3), line_width)
    pygame.draw.line(WINDOW, color, (x + cell_width // 3, y - cell_height // 3), (x - cell_width // 3, y + cell_height // 3), line_width)

# Function to draw an O
def draw_o(x, y, color):
    pygame.draw.circle(WINDOW, color, (x, y), 36, 18)

# Function to check for a winner
def check_winner():
    global WINNER, GAME_OVER
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            WINNER = board[i]
            GAME_OVER = True
            return WINNER
    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            WINNER = board[i]
            GAME_OVER = True
            return WINNER
    # Check diagonals
    if board[0] == board[4] == board[8] != ' ':
        WINNER = board[0]
        GAME_OVER = True
        return WINNER
    if board[2] == board[4] == board[6] != ' ':
        WINNER = board[2]
        GAME_OVER = True
        return WINNER
    # Check for a tie
    if ' ' not in board:
        GAME_OVER = True
        return None

def minimax(board, depth, is_maximizing):
    # Check for a winner or a tie
    result = check_winner()
    if result != None:
        if result == 'X':
            return -1
        elif result == 'O':
            return 1
        else:
            return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = COMPUTER
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(best_score, score)
        return best_score

def computer_move():
    corners = [0, 2, 6, 8]
    edges = [1, 3, 5, 7]
    center = 4

    # Prioritize corner, center, and edges moves
    for move in [corners, [center], edges]:
        for pos in move:
            if board[pos] == ' ':
                board[pos] = COMPUTER
                return

BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (50, 50, 50)
INPUT_COLOR = (245, 245, 245)
INPUT_BORDER_COLOR = (200, 200, 200)
INPUT_ACTIVE_COLOR = (235, 235, 235)
INPUT_ACTIVE_BORDER_COLOR = (150, 150, 150)

# Define the font
FONT = pygame.font.Font(None, 36) 

def run_tic_tac_toe():
    global GAME_OVER, WINNER, board
    username = ''
    input_active = True
    input_rect = pygame.Rect(150, 300, 300, 50)  

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        WINDOW.fill(BACKGROUND_COLOR)

        # Draw input box
        input_color = INPUT_ACTIVE_COLOR if input_active else INPUT_COLOR
        input_border_color = INPUT_ACTIVE_BORDER_COLOR if input_active else INPUT_BORDER_COLOR
        pygame.draw.rect(WINDOW, input_border_color, input_rect, 2, border_radius=25)
        pygame.draw.rect(WINDOW, input_color, input_rect.inflate(-4, -4), border_radius=20)

        input_surface = FONT.render(username, True, TEXT_COLOR)
        input_surface_rect = input_surface.get_rect(midleft=(input_rect.x + 15, input_rect.centery))
        WINDOW.blit(input_surface, input_surface_rect)

        text_surface = FONT.render("Enter your username:", True, TEXT_COLOR)
        WINDOW.blit(text_surface, (150, 250))
        pygame.display.update()


    while not GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // (WINDOW_SIZE[1] // 3)
                col = x // (WINDOW_SIZE[0] // 3)
                index = row * 3 + col
                if board[index] == ' ':
                    board[index] = HUMAN
                    check_winner()
                    if not GAME_OVER:
                        computer_move()
                        check_winner()

        draw_board()

        if GAME_OVER:
            if WINNER is None:
                message = "It's a tie!"
            else:
                message = f"{WINNER} wins!"
                timestamp = datetime.now()
                data = {
                    "username": username,
                    "correct_response": WINNER,
                    "timestamp": timestamp
                }
                try:
                    collection.insert_one(data)
                    print("Data inserted successfully!")
                except Exception as e:
                    print("Error inserting data:", e)
            text = FONT.render(message, True, WINNER_COLOR)
            text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            WINDOW.blit(text, text_rect)

            # winner message
            alpha = 255
            while alpha > 0:
                text.set_alpha(alpha)
                WINDOW.blit(text, text_rect)
                pygame.display.update()
                alpha -= 5
                pygame.time.delay(10)

            # Reset the game
            board = [' ' for _ in range(9)]
            GAME_OVER = False
            WINNER = None

        pygame.display.update()

# Run the game
run_tic_tac_toe()
