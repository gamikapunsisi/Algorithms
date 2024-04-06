# Eight Queens Puzzle

## 3.1.1. Explain the Program Logic used to solve the problem

The program uses a recursive backtracking algorithm to solve the Eight Queens Puzzle. The `solve_queens` function is responsible for finding all possible solutions. It starts by placing a queen in the first column and recursively tries to place the remaining queens in the subsequent columns. The `is_safe` function checks if a queen can be placed on a given position by ensuring that it does not conflict with any previously placed queens in the same row, column, or diagonal.

## 3.1.2. UI screenshot allowing game players to provide answers

![UI for Entering Player Name](random_image_1.jpg)

## 3.1.3. UI screenshots when game players provide correct answer & incorrect answers

![Correct Answer](random_image_2.jpg)
![Incorrect Answer](random_image_3.jpg)

## 3.1.4. Explain the Validations and Exception Handling in this application.

The application performs input validation to ensure that the player enters a valid name. It also handles the `pygame.QUIT` event to gracefully exit the application when the user closes the window. Additionally, it catches any exceptions that may occur during the game loop and handles them appropriately.

## 3.1.5. Code Segment screenshots: unit Testing

*Note: No unit tests are provided in the given code.*

## 3.1.6. Indicate the Data Structures used and Explain its purpose

The program uses a 2D list (`board`) to represent the chessboard. Each element in the list represents a square on the board, and its value is either 0 (empty) or 1 (queen placed). The `solutions` list is used to store all the valid solutions found by the backtracking algorithm.

## 3.1.7. Screenshot of the Normalized DB Table Structure used for this Game Option

*Note: No database structure is provided in the given code.*

## 3.1.8. Compare the time taken & logic used for the Sequential program & the Threaded program.

*Note: The provided code does not implement any threading or parallel execution.*

# 3.2. Tic-Tac-Toe

## 3.2.1. Explain the Program Logic used to solve the problem

The program implements a Tic-Tac-Toe game where the player competes against an AI opponent. The AI uses the Minimax algorithm with alpha-beta pruning to make optimal moves. The algorithm recursively explores all possible game states and evaluates the best move based on a scoring system (-1 for a loss, 0 for a tie, and 1 for a win).

## 3.2.2. UI screenshot allowing game players to provide answers

![UI for Entering Username](random_image_4.jpg)

## 3.2.3. UI screenshots when game players provide correct answer & incorrect answers

![Winner Message](random_image_5.jpg)
![Tie Message](random_image_6.jpg)

## 3.2.4. Explain the Validations and Exception Handling in this application.

The application validates the user's input for the username and handles the `pygame.QUIT` event to gracefully exit the application. It also catches any exceptions that may occur during the game loop or database operations and handles them appropriately.

## 3.2.5. Code Segment screenshots: unit Testing

*Note: No unit tests are provided in the given code.*

## 3.2.6. Indicate the Data Structures used and purpose

The program uses a list (`board`) to represent the Tic-Tac-Toe board. Each element in the list corresponds to a cell on the board and can have a value of ' ' (empty), 'X' (player's move), or 'O' (computer's move).

## 3.2.7. Screenshot of the Normalized DB Table Structure used for this Game Option

*Note: No database structure is provided in the given code.*

# 3.3. Identify Shortest Path

## 3.3.1. Explain the Program Logic used to solve the problem

The program generates a random set of cities with randomly assigned distances between them. It then allows the player to select two cities by clicking on them. The program uses Dijkstra's algorithm to calculate the shortest path between the selected cities. The player is prompted to enter the correct shortest distance, and their response is recorded.

## 3.3.2. UI screenshot allowing game players to provide answers

![City Selection](random_image_7.jpg)

## 3.3.3. UI screenshots when game players provide correct answer & incorrect answers

![Correct Distance](random_image_8.jpg)
![Incorrect Distance](random_image_9.jpg)

## 3.3.4. Explain the Validations and Exception Handling in this application.

The application handles the `pygame.QUIT` event to gracefully exit the application. It also validates the player's input for the shortest distance and handles any non-numeric input appropriately.

## 3.3.5. Code Segment screenshots: unit Testing

*Note: No unit tests are provided in the given code.*

## 3.3.6. Indicate the Data Structures used with its purpose

The program uses a dictionary (`distances`) to store the distances between cities. The keys of the dictionary are the city names, and the values are nested dictionaries containing the distances to other cities.

## 3.3.7. Screenshot of the Normalized DB Table Structure used for this Game Option

*Note: No database structure is provided in the given code.*

## 3.3.8. Compare the Shortest path identifying algorithms (logic/complexity, which scenarios are best to use it, etc.)

*Note: The provided code only implements Dijkstra's algorithm for finding the shortest path.*

# 3.4. Remember the Value Index

## 3.4.1. UI screenshot allowing game players to provide answers

![Value Index Input](random_image_10.jpg)

## 3.4.2. UI screenshots when game players provide correct answer & incorrect answers

*Note: No UI screenshots for correct/incorrect answers are provided in the given code.*

## 3.4.3. Chart Containing the time Taken for each Sorting Technique

*Note: No chart or timing information for sorting techniques is provided in the given code.*

## 3.4.4. Compare the sorting techniques (e.g., explain the logic used in the sorting Techniques, determine their complexity, which scenarios are best to use it, etc.).

The provided code implements the following sorting techniques:

1. **Bubble Sort**: Compares adjacent elements and swaps them if they are in the wrong order. It has a time complexity of O(n^2), making it inefficient for large datasets.

2. **Insertion Sort**: Builds the final sorted array one element at a time by inserting each element into its correct position in the sorted portion of the array. It has a time complexity of O(n^2) in the worst case and O(n) in the best case when the array is already sorted.

3. **Merge Sort**: Divide the unsorted list into n sublists, each containing one element, and then repeatedly merge the sublists to produce new sorted sublists until there is only one sublist remaining. It has a time complexity of O(n log n) in all cases.

4. **Radix Sort**: Sorts the elements by first grouping them by their most significant digit, then by their second most significant digit, and so on. It has a time complexity of O(kn), where k is the number of digits in the maximum element.

5. **Shell Sort**: An optimization of Insertion Sort that allows the exchange of elements that are far apart. It has a time complexity of O(n^2) in the worst case and O(n log n) in the best case.

6. **Quick Sort**: Selects a "pivot" element from the array and partitions the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then sorted recursively. It has an average time complexity of O(n log n), but a worst-case time complexity of O(n^2) when the array is already sorted or reverse-sorted.

7. **Tim Sort**: A combination of Insertion Sort and Merge Sort. It uses Insertion Sort for small arrays and Merge Sort for larger arrays. It has a time complexity of O(n log n) in the worst case and performs well on sorted and partially sorted data.

The choice of sorting algorithm depends on the size and characteristics of the dataset, as well as the time and space complexity requirements of the application.

# 3.5. Predict the Value Index

## 3.5.1. UI screenshot allowing game players to provide answers

![Predict Value Index](random_image_11.jpg)

## 3.5.2. UI screenshots when game players provide correct answer & incorrect answers

![Correct Prediction](random_image_12.jpg)
![Incorrect Prediction](random_image_13.jpg)

## 3.5.3. Chart Containing the time Taken for each search Technique

*Note: No chart or timing information for search techniques is provided in the given code.*

## 3.5.4. Compare the search techniques (e.g., explain the logic used in the search Techniques, determine their complexity, which scenarios are best to use it, etc.).

The provided code implements the following search techniques:

1. **Binary Search**: Repeatedly divides the search interval in half based on whether the target value is higher or lower than the middle element. It has a time complexity of O(log n) in the average and best cases, but requires the input array to be sorted.

2. **Jump Search**: Jumps ahead by a fixed step size and then performs a linear search around the nearest element to the target value. It has a time complexity of O(√n) in the best case and O(n) in the worst case.

3. **Exponential Search**: Finds a range where the target value might exist by exponentially increasing the search range until it exceeds the target value. It then performs a binary search on the found range. Its time complexity is O(log n) in the best case and O(log n) in the worst case.

4. **Fibonacci Search**: Similar to Binary Search, but uses Fibonacci numbers to determine the next search interval instead of dividing the interval in half. It has a time complexity of O(log n) in the average and best cases, but requires the input array to be sorted.

The choice of search technique depends on the characteristics of the dataset, such as whether it is sorted or unsorted, and the time complexity requirements of the application. Binary Search and Fibonacci Search are efficient for sorted arrays, while Jump Search and Exponential Search can be useful for partially sorted or unsorted arrays.