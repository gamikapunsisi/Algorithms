import pytest
from test_remember_the_value_index import bubble_sort, insertion_sort, merge_sort, radix_sort, shell_sort, quick_sort, tim_sort

# Sample data for testing
numbers = [2, 5, 1, 9, 7, 3, 6, 8, 4]

@pytest.mark.parametrize("sorting_func", [
    bubble_sort,
    insertion_sort,
    merge_sort,
    radix_sort,
    shell_sort,
    quick_sort,
    tim_sort
])
def test_sorting_algorithms(sorting_func):
    # Test case for sorted output
    sorted_numbers = sorting_func(numbers.copy())
    assert sorted_numbers == sorted(numbers)

    # Test case for empty list
    assert sorting_func([]) == []

    # Test case for single element list
    assert sorting_func([1]) == [1]

    # Test case for already sorted list
    assert sorting_func([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Test case for reverse sorted list
    assert sorting_func([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
