# Puzzle interface (supports Sudoku & WordLadder)

Allow interactive game play using either the command line or a web-based view (for WordLadder only). Web-based view is launched using localhost.

Goal of Sudoku:
Fill in all spaces of the board such that each letter only appears once per row, per column, and per square grid.

Goal of WordLadder:
Go from the starting word to the target word by finding words that differ by at most one letter from the previous word.

Example:
start: cat
target: fig

cat -> pat -> pit -> pig -> fig

Hint, Undo, and Solve functions can be called anytime.

Main function is located in controller.py.
