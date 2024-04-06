import pytest
from identify_shortest_path import Game

@pytest.fixture
def game():
    return Game()

# Test Dijkstra's algorithm
def test_dijkstra(game):
    start_city = game.cities[0].name
    end_city = game.cities[-1].name
    distance, duration = game.dijkstra(start_city, end_city)
    assert isinstance(distance, int)
    assert isinstance(duration, float)

# Test Bellman-Ford algorithm
def test_bellman_ford(game):
    start_city = game.cities[0].name
    end_city = game.cities[-1].name
    result, duration = game.bellman_ford(start_city, end_city)
    if result != "negative cycle":
        assert isinstance(result, int)
    assert isinstance(duration, float)
