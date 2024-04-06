import pytest

# Import the functions to be tested
from tik_tak_toe import check_winner, minimax

# Test cases for check_winner function
def test_check_winner_empty_board():
    board = [' ' for _ in range(9)]

    winner = check_winner(board)

    assert winner is None

def test_check_winner_horizontal_win():
    board = ['X', 'X', 'X',
             'O', 'O', ' ',
             ' ', ' ', ' ']

    winner = check_winner(board)

    assert winner == 'X'

def test_check_winner_vertical_win():
    board = ['O', 'X', ' ',
             'O', 'X', ' ',
             'O', ' ', ' ']

    winner = check_winner(board)

    assert winner == 'O'

def test_check_winner_diagonal_win():
    board = ['X', 'O', ' ',
             'O', 'X', ' ',
             ' ', ' ', 'X']

    winner = check_winner(board)

    assert winner == 'X'

def test_check_winner_no_winner():
    board = ['X', 'O', 'X',
             'O', 'X', 'O',
             'O', 'X', 'O']

    winner = check_winner(board)

    assert winner is None

def test_check_winner_tie():
    board = ['X', 'O', 'X',
             'X', 'X', 'O',
             'O', 'X', 'O']

    winner = check_winner(board)

    assert winner is None


def test_minimax_human_wins():
    board = ['X', 'X', 'X',
             'O', 'O', ' ',
             ' ', ' ', ' ']

    score = minimax(board, 0, False)

    assert score == -1

def test_minimax_computer_wins():
    board = ['O', 'O', ' ',
             ' ', 'X', 'X',
             ' ', ' ', 'O']

    score = minimax(board, 0, True)

    assert score == 1

def test_minimax_tie():
    board = ['X', 'O', 'X',
             'X', 'X', 'O',
             'O', 'X', 'O']

    score = minimax(board, 0, True)

    assert score == 0


