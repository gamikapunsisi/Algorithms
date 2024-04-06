import pygame
import random
from pymongo import MongoClient
import time
import math 

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Predict the Value Index")

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.predict_the_value_index

# Define colors
BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (64, 128, 255)
BUTTON_HOVER_COLOR = (96, 160, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
TEXT_COLOR = (64, 64, 64)
BAR_COLOR = (64, 128, 255)
CORRECT_COLOR = (0, 200, 0)
INCORRECT_COLOR = (200, 0, 0)

# Define fonts
FONT_LARGE = pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 18)

# Function to generate random numbers
def generate_random_numbers():
    loading_text = FONT_LARGE.render("Generating Random Numbers...", True, TEXT_COLOR)
    loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    loading_bar_width = 400
    loading_bar_height = 30
    loading_bar_rect = pygame.Rect((WINDOW_WIDTH - loading_bar_width) // 2, loading_rect.bottom + 20,
                                   loading_bar_width, loading_bar_height)
    progress = 0

    while progress < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(loading_text, loading_rect)

        # Draw the outline of the loading bar
        pygame.draw.rect(screen, TEXT_COLOR, loading_bar_rect, 2)

        # Calculate the width of the loading bar based on progress
        loading_progress_rect = pygame.Rect(loading_bar_rect.left, loading_bar_rect.top,
                                            loading_bar_width * progress // 100, loading_bar_height)
        pygame.draw.rect(screen, BUTTON_COLOR, loading_progress_rect)

        pygame.display.flip()
        time.sleep(0.03)  # Animation speed
        progress += 1

    arr = []
    for _ in range(5000):
        arr.append(random.randint(1, 1000000))
    return arr



# Function to display the game menu
def display_menu():
    screen.fill(BACKGROUND_COLOR)
    title = FONT_LARGE.render("Predict the Value Index", True, TEXT_COLOR)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

    play_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 25, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, play_button, border_radius=5) 
    play_text = FONT_MEDIUM.render("Play", True, BUTTON_TEXT_COLOR)
    screen.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2 - play_text.get_height() // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    play_game()
            elif event.type == pygame.MOUSEMOTION:  
                if play_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_HOVER_COLOR, play_button, border_radius=5)
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, play_button, border_radius=5)
                screen.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2 - play_text.get_height() // 2))
                pygame.display.update()


def play_game():
    return_to_menu = False 

    numbers = generate_random_numbers()
    numbers.sort()

    search_data = []
    max_time = 0
    random_value = random.choice(numbers)
    index_final = 0
    for search_func in [binary_search, jump_search, exponential_search, fibonacci_search]:
        index, time_taken = search_func(numbers, random_value)
        search_data.append((search_func.__name__, time_taken, index))
        max_time = max(max_time, time_taken)
        index_final = index

    choices = []
    while len(choices) < 4:
        random_choice = random.choice(numbers)
        if random_choice not in choices:
            choices.append(random_choice)
    choices.append(index_final)
    random.shuffle(choices)

    # Display search results
    screen.fill(BACKGROUND_COLOR)
    title = FONT_LARGE.render("Search Results", True, TEXT_COLOR)
    screen.blit(title, (50, 50))

    bar_width = 400
    bar_height = 30
    y = 100
    for data in search_data:
        result = FONT_MEDIUM.render(f"{data[0]}: Time Taken = {data[1]*1000:.2f} ms, Index = {data[2]}", True, TEXT_COLOR)
        screen.blit(result, (100, y))

        animation_width = 0
        while animation_width <= int((data[1] / max_time) * bar_width):
            pygame.draw.rect(screen, BAR_COLOR, (100, y + 20, animation_width, bar_height))
            pygame.display.update()
            time.sleep(0.02)  
            animation_width += 5 

        y += 50

    prediction_text = FONT_LARGE.render(f"Predict the value:", True, TEXT_COLOR)
    screen.blit(prediction_text, (50, y + 50))

    y += 100
    choice_rects = []
    for i, choice in enumerate(choices):
        choice_text = FONT_MEDIUM.render(f"{i + 1}. {choice}", True, TEXT_COLOR)
        choice_rect = pygame.Rect(100, y, choice_text.get_width() + 20, choice_text.get_height() + 10)
        choice_rects.append(choice_rect)
        pygame.draw.rect(screen, BUTTON_COLOR, choice_rect)
        screen.blit(choice_text, (105, y + 5))
        y += 50

    pygame.display.update()

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_to_menu = True
                pygame.quit()
                return return_to_menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, choice_rect in enumerate(choice_rects): 
                    if choice_rect.collidepoint(mouse_pos):
                        print(choices[i + 1])
                        if choices[i] == index_final:
                            
                            result_text = FONT_LARGE.render("Correct!", True, (0, 200, 0))
                            screen.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT - 100))

                            # Get user name and save data
                            name = FONT_MEDIUM.render("Enter your name:", True, TEXT_COLOR)
                            screen.blit(name, (WINDOW_WIDTH // 2 - name.get_width() // 2, WINDOW_HEIGHT - 200))
                            pygame.display.update()

                            user_name = ""
                            while True:
                                event = pygame.event.wait()
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        break
                                    elif event.key == pygame.K_BACKSPACE:
                                        user_name = user_name[:-1]
                                    else:
                                        user_name += event.unicode

                                    text = FONT_SMALL.render(user_name, True, TEXT_COLOR)
                                    screen.fill(BACKGROUND_COLOR, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 150, 200, 50))
                                    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT - 150))
                                    pygame.display.update()

                            collection.insert_one({"name": user_name, "correct_answer": 1})
                        else:
                            # User predicted incorrectly
                            result_text = FONT_LARGE.render("Incorrect!", True, (200, 0, 0))
                            screen.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT - 100))
                            collection.insert_one({"name": "Anonymous", "correct_answer": 0})
                        pygame.display.update()
                        pygame.time.delay(2000)
                        display_menu()

def binary_search(arr, target):
    start = time.time()
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, time.time() - start  
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, time.time() - start  

# Function to perform Jump Search
def jump_search(arr, target):
    start = time.time()
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1, time.time() - start
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1, time.time() - start
    if arr[prev] == target:
        return prev, time.time() - start
    return -1, time.time() - start

def exponential_search(arr, target):
    start = time.time()
    n = len(arr)
    if arr[0] == target:
        return 0, time.time() - start

    i = 1
    while i < n and arr[i] <= target:
        i *= 2

    left = i // 2
    right = min(i, n)

    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, time.time() - start
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return -1, time.time() - start  
def fibonacci_search(arr, target):
    start = time.time()
    n = len(arr)
    fib_n = 0
    fib_nm1 = 1
    fib_nm2 = 0
    while fib_n < n:
        fib_nm2 = fib_nm1
        fib_nm1 = fib_n
        fib_n = fib_nm1 + fib_nm2
    offset = -1
    while fib_n > 1:
        i = min(offset + fib_nm2, n - 1)
        if arr[i] < target:
            fib_n = fib_nm1
            fib_nm1 = fib_nm2
            fib_nm2 = fib_n - fib_nm1
            offset = i
        elif arr[i] > target:
            fib_n = fib_nm2
            fib_nm1 = fib_nm1 - fib_nm2
            fib_nm2 = fib_n - fib_nm1
        else:
            return i, time.time() - start
    if fib_nm1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1, time.time() - start
    return -1, time.time() - start  

# Start the game
display_menu()

# Close the database connection
client.close()
