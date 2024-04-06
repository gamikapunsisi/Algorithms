import pytest
from predict_the_value_index import binary_search, jump_search, exponential_search, fibonacci_search

# Sample data for testing
numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

@pytest.mark.parametrize("search_func", [
    binary_search,
    jump_search,
    exponential_search,
    fibonacci_search
])
def test_search_algorithms(search_func):
    # Test case for existing element
    assert search_func(numbers, 10)[0] == 4

    # Test case for non-existing element
    assert search_func(numbers, 5)[0] == -1

    # Test case for time taken
    assert search_func(numbers, 10)[1] >= 0  # Check if time is non-negative
