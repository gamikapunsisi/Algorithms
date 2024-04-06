import pygame
import random
import time
from pymongo import MongoClient

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Remember the Value Index")

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.remember_the_value_index

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Define fonts
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 24)

def generate_random_numbers_with_animation():
    loading_text = font.render("Generating Random Numbers...", True, WHITE)
    loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    loading_bar_width = 400
    loading_bar_height = 30
    loading_bar_rect = pygame.Rect((WINDOW_WIDTH - loading_bar_width) // 2, loading_rect.bottom + 20,
                                   loading_bar_width, loading_bar_height)
    progress = 0

    while progress <= 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)
        screen.blit(loading_text, loading_rect)

        # Draw the outline of the loading bar
        pygame.draw.rect(screen, WHITE, loading_bar_rect, 2)

        # Calculate the width of the loading bar based on progress
        loading_progress_rect = pygame.Rect(loading_bar_rect.left, loading_bar_rect.top,
                                            loading_bar_width * progress // 100, loading_bar_height)
        pygame.draw.rect(screen, LIGHT_BLUE, loading_progress_rect)

        pygame.display.flip()
        time.sleep(0.02)  # Adjust the speed of the animation for smoother transitions
        progress += 1

    numbers = [random.randint(1, 1000000) for _ in range(5000)]
    return numbers


# Sorting algorithms
def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers

def insertion_sort(numbers):
    for i in range(1, len(numbers)):
        key = numbers[i]
        j = i - 1
        while j >= 0 and key < numbers[j]:
            numbers[j + 1] = numbers[j]
            j -= 1
        numbers[j + 1] = key
    return numbers

def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    mid = len(numbers) // 2
    left = numbers[:mid]
    right = numbers[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]

    return result

def radix_sort(numbers):
    max_num = max(numbers)
    exp = 1

    while max_num / exp > 0:
        counting_sort(numbers, exp)
        exp *= 10

    return numbers

def counting_sort(numbers, exp):
    n = len(numbers)
    output = [0] * n
    count = [0] * 10

    for num in numbers:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        digit = (numbers[i] // exp) % 10
        output[count[digit] - 1] = numbers[i]
        count[digit] -= 1
        i -= 1

    for i in range(n):
        numbers[i] = output[i]

def shell_sort(numbers):
    n = len(numbers)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = numbers[i]
            j = i
            while j >= gap and numbers[j - gap] > temp:
                numbers[j] = numbers[j - gap]
                j -= gap
            numbers[j] = temp
        gap //= 2

    return numbers

def quick_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    pivot = numbers[len(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    middle = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

def tim_sort(numbers):
    min_run = 32
    n = len(numbers)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        numbers[start:end + 1] = insertion_sort(numbers[start:end + 1])

    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (n - 1))

            merged_array = merge(
                left=numbers[start:midpoint + 1],
                right=numbers[midpoint + 1:end + 1]
            )

            numbers[start:start + len(merged_array)] = merged_array

        size *= 2

    return numbers

# Sort the numbers and record the time taken
def sort_numbers(numbers):
    sorting_times = []

    start_time = time.time()
    bubble_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Bubble Sort", end_time - start_time))

    start_time = time.time()
    insertion_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Insertion Sort", end_time - start_time))

    start_time = time.time()
    merge_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Merge Sort", end_time - start_time))

    start_time = time.time()
    radix_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Radix Sort", end_time - start_time))

    start_time = time.time()
    shell_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Shell Sort", end_time - start_time))

    start_time = time.time()
    quick_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Quick Sort", end_time - start_time))

    start_time = time.time()
    tim_sort(numbers.copy())
    end_time = time.time()
    sorting_times.append(("Tim Sort", end_time - start_time))

    return numbers, sorting_times

# Display the sorted numbers
def display_numbers(sorted_numbers):
    y_offset = 0
    small_font = pygame.font.Font(None, 50)  # Define a smaller font size
    for i in range(20):
        print(i, str(sorted_numbers[i]))
        screen.fill(BLACK)
        text = small_font.render(str(sorted_numbers[i]), True, WHITE)  # Use the smaller font
        text_rect = text.get_rect()
        text_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + y_offset)
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)


# Get the index of a value
def get_index(value, sorted_numbers):
    return sorted_numbers.index(value)

# Get user input using Pygame UI
def get_user_input(prompt):
    input_text = ""
    input_rect = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2, 40)
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Clear the screen
        screen.fill(BLACK)

        # Render the prompt
        prompt_text = font.render(prompt, True, WHITE)
        prompt_rect = prompt_text.get_rect()
        prompt_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        screen.blit(prompt_text, prompt_rect)

        # Render the input text
        input_surface = input_font.render(input_text, True, WHITE)
        input_rect.w = max(200, input_surface.get_width() + 10)
        pygame.draw.rect(screen, GRAY, input_rect, 2)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        if active:
            pygame.draw.line(screen, WHITE, (input_rect.right - 10, input_rect.y + 20), (input_rect.right - 2, input_rect.y + 20), 2)

        pygame.display.flip()


def draw_progress_bar(screen, x, y, width, height, progress, max_value, color):
    # Create a surface for the progress bar
    bar_surface = pygame.Surface((width, height))
    bar_surface.fill((64, 64, 64))  # Darker gray background

    # Create a surface for the progress
    progress_surface = pygame.Surface((int(width * progress / max_value), height))
    progress_surface.fill(color)

    # Blit the progress surface onto the bar surface
    bar_surface.blit(progress_surface, (0, 0))

    # Blit the bar surface onto the main screen
    screen.blit(bar_surface, (x, y))
def animate_progress_bars(screen, sorting_times):
    screen.fill((0, 0, 0))  # Black background
    max_time = max(time for _, time in sorting_times)
    y = 100
    bar_width = 400
    bar_height = 30

    for algorithm, time_taken in sorting_times:
        font = pygame.font.Font(None, 24)
        text = font.render(f"{algorithm}: {time_taken:.6f} seconds", True, (255, 255, 255))
        screen.blit(text, (50, y))

        progress = 0
        while progress <= time_taken:
            draw_progress_bar(screen, 300, y, bar_width, bar_height, progress, time_taken, (0, 255, 0))
            pygame.display.flip()
            progress += max_time / 100  # Adjust the speed of the animation

        y += 50

    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before exiting

def game_loop():
    time.sleep(20)
    running = True
    numbers = generate_random_numbers_with_animation()
    sorted_numbers, sorting_times = sort_numbers(numbers)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Animate the progress bars for sorting times
        animate_progress_bars(screen, sorting_times)

        # Display the sorted numbers
        display_numbers(sorted_numbers)

        # Ask the user for the index of two random values
        random_values = random.sample(sorted_numbers[:20], 2)
        for value in random_values:
            user_input = get_user_input(f"Enter the index of {value}: ")
            try:
                index = int(user_input)
                if index == get_index(value, sorted_numbers):
                    print("Correct!")
                    player_name = get_user_input("Enter your name: ")
                    collection.insert_one({"player_name": player_name, "correct_response": value})
                else:
                    print("Incorrect.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

# Run the game loop
game_loop()

