import pygame
import sys
import random
import heapq
import time
from pymongo import MongoClient

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.identify_shortest_path

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)  # Steel Blue
RED = (220, 20, 60)  # Crimson Red
FONT_NAME = "Arial"
FONT_SIZE = 18
CITY_RADIUS = 20
NUM_CITIES = 6

# Class representing a city
class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.selected = False  # Added selected attribute to track if the city is selected

# Class representing the game
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Set resizable flag
        pygame.display.set_caption("Identify Shortest Path")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.cities = self.generate_cities()
        self.distances = self.generate_distances()
        self.selected_cities = []
        self.player_name = self.get_player_name()
        self.run()

    # Method to get the player's name
    def get_player_name(self):
        pygame.display.set_caption("Enter Your Name")
        input_box = InputBox(300, 200, 200, 40, font=self.font)
        name_entered = False
        while not name_entered:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player_name = input_box.text
                    name_entered = True
                input_box.handle_event(event)

            self.screen.fill(WHITE)
            prompt_text = self.font.render("Enter your name:", True, BLACK)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(prompt_text, prompt_rect)
            input_box.draw(self.screen)
            pygame.display.flip()
        return player_name

    # Generate random cities
    def generate_cities(self):
        cities = []
        for i in range(NUM_CITIES):
            x = random.randint(CITY_RADIUS, WIDTH - CITY_RADIUS)
            y = random.randint(CITY_RADIUS, HEIGHT - CITY_RADIUS)
            city = City(chr(65 + i), x, y)  # City names A, B, C, ...
            cities.append(city)
        return cities

    # Generate random distances between cities
    def generate_distances(self):
        distances = {}
        for city1 in self.cities:
            distances[city1.name] = {}
            for city2 in self.cities:
                if city1 != city2:
                    distance = random.randint(5, 50)
                    distances[city1.name][city2.name] = distance
        return distances

    # Draw cities and distances on the screen
    def draw(self):
        self.screen.fill(WHITE)  # Light gray background
        for city in self.cities:
            color = RED if city.selected else BLUE  # Highlight the selected city
            pygame.draw.circle(self.screen, color, (city.x, city.y), CITY_RADIUS)
            pygame.draw.circle(self.screen, BLACK, (city.x, city.y), CITY_RADIUS, 2)
            text = self.font.render(city.name, True, BLACK)
            text_rect = text.get_rect(center=(city.x, city.y))
            self.screen.blit(text, text_rect)

        for city1 in self.distances:
            for city2 in self.distances[city1]:
                distance = self.distances[city1][city2]
                x1, y1 = [city.x for city in self.cities if city.name == city1][0], [city.y for city in self.cities if city.name == city1][0]
                x2, y2 = [city.x for city in self.cities if city.name == city2][0], [city.y for city in self.cities if city.name == city2][0]
                pygame.draw.aaline(self.screen, BLACK, (x1, y1), (x2, y2))  # Smooth line drawing
                text = self.font.render(str(distance), True, BLACK)
                text_rect = text.get_rect(center=((x1 + x2) // 2, (y1 + y2) // 2))
                self.screen.blit(text, text_rect)

        pygame.display.flip()

    # Dijkstra's algorithm to find the shortest path
    def dijkstra(self, start, end):
        distances = {city.name: float('inf') for city in self.cities}
        distances[start] = 0
        heap = [(0, start)]

        start_time = time.time()  # Start time for algorithm execution

        while heap:
            current_distance, current_city = heapq.heappop(heap)
            if current_city == end:
                duration = time.time() - start_time  # Calculate algorithm execution duration
                return current_distance, duration
            if current_distance > distances[current_city]:
                continue
            for neighbor, distance in self.distances[current_city].items():
                total_distance = current_distance + distance
                if total_distance < distances[neighbor]:
                    distances[neighbor] = total_distance
                    heapq.heappush(heap, (total_distance, neighbor))

    # Bellman-Ford algorithm to find the shortest path
    def bellman_ford(self, start, end):
        distances = {city.name: float('inf') for city in self.cities}
        distances[start] = 0

        start_time = time.time()  # Start time for algorithm execution

        for _ in range(len(self.cities) - 1):
            for city1 in self.distances:
                for city2 in self.distances[city1]:
                    distance = self.distances[city1][city2]
                    if distances[city1] + distance < distances[city2]:
                        distances[city2] = distances[city1] + distance

        for city1 in self.distances:
            for city2 in self.distances[city1]:
                distance = self.distances[city1][city2]
                if distances[city1] + distance < distances[city2]:
                    duration = time.time() - start_time  # Calculate algorithm execution duration
                    return "negative cycle", duration

        duration = time.time() - start_time  # Calculate algorithm execution duration
        return distances[end], duration

    # Show popup window for input
    def show_popup(self, correct_distance_dijkstra, correct_distance_bf):
        input_box = InputBox(300, 200, 200, 40, font=self.font)
        input_box.text = ""
        input_box.active = True
        print("dijkstra:", str(correct_distance_dijkstra) + " Bellman-Ford:" ,str(correct_distance_bf))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return input_box.text
                input_box.handle_event(event)

            self.screen.fill(WHITE)
            prompt_text = self.font.render(f"Enter the correct shortest distance:", True, BLACK)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(prompt_text, prompt_rect)
            input_box.draw(self.screen)
            pygame.display.flip()

    # Main game loop
    def run(self):
        pygame.display.set_caption("Identify Shortest Path - Player: " + self.player_name)
        running = True
        while running:
            self.clock.tick(30)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for city in self.cities:
                        if abs(x - city.x) < CITY_RADIUS and abs(y - city.y) < CITY_RADIUS:
                            city.selected = not city.selected  # Toggle selection
                            if city.selected:
                                self.selected_cities.append(city.name)
                                if len(self.selected_cities) == 2:
                                    city1, city2 = self.selected_cities
                                    correct_distance_dijkstra, duration_dijkstra = self.dijkstra(city1, city2)
                                    correct_distance_bf, duration_bf = self.bellman_ford(city1, city2)
                                    user_distance = self.show_popup(correct_distance_dijkstra, correct_distance_bf)
                                    if user_distance == str(correct_distance_dijkstra) or user_distance == str(correct_distance_bf):
                                        print("Correct!")
                                    else:
                                        print(f"Wrong! Correct distances: Dijkstra - {correct_distance_dijkstra}, Bellman-Ford - {correct_distance_bf}")
                                    print(f"Dijkstra's algorithm execution time: {duration_dijkstra} milliseconds")
                                    print(f"Bellman-Ford algorithm execution time: {duration_bf} milliseconds")
                                    # Record algorithm execution durations in the database
                                    collection.insert_one({"player_name": self.player_name, "dijkstra_duration": duration_dijkstra, "bellman_ford_duration": duration_bf})
                                    self.selected_cities = []
                                    # Unhighlight selected cities
                                    for city in self.cities:
                                        city.selected = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame.quit()

# Class representing the input box
class InputBox:
    def __init__(self, x, y, width, height, text='', font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the color of the input box
            self.color = BLACK if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Draw the input box and the text surface
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=8)  # Rounded border
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

if __name__ == "__main__":
    Game().run()
