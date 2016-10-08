"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle.
"""
from puzzle import Puzzle
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle
import collections


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    @type puzzle: Puzzle
    @type verbose: bool
        Whether every state explored should be printed out.
    @rtype: Puzzle | None
        A solution to puzzle or None if the puzzle cannot be solved.
    """
    if type(puzzle) == SudokuPuzzle:
        return solve_depth(puzzle)
    else:
        return solve_breadth(puzzle)


def solve_depth(puzzle, verbose=False):
    """Return a solution of the puzzle by searching possible game states using depth-first search.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: SudokuPuzzle
    @type verbose: bool
        Whether every state explored should be printed out.
    @rtype: Puzzle | None
        A solution to puzzle or None if the puzzle cannot be solved.
    """
    if puzzle.is_solved():
        return puzzle
    else:
        for new_state in puzzle.extensions():
            if verbose:
                print(new_state)
            state = solve_depth(new_state, verbose)
            if state:
                return state
        return None


def solve_breadth(puzzle):
    """Return a solution of the puzzle using breadth-first search.

    @type puzzle: WordLadderPuzzle
    @rtype: Puzzle | None
        A solution to puzzle or None if the puzzle cannot be solved.
    """
    solution = solve_in_breadth(puzzle, hint=False)
    if solution[0]:
        return solution[1]
    else:
        return None


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
        Whether every state explored should be printed out.
    @rtype: list[Puzzle] | None
        A list of all solutions to the puzzle.
    """
    if puzzle.is_solved():
        return [puzzle]
    else:
        solutions = []
        for new_state in puzzle.extensions():
            if verbose:
                print(new_state)
            if solve_complete(new_state, verbose):
                solutions.extend(solve_complete(new_state, verbose))
        return solutions


def hint_by_depth(puzzle, n=100):
    """Return a hint for the given puzzle state using depth-first search. Used for Sudoku puzzle.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution, return the string 'No possible extensions!'

    @type puzzle: SudokuPuzzle
    @type n: int
        The 'depth' / number of moves that should be explored. Default is 100 to prevent search from taking too long.
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    else:
        for extension in puzzle.extensions():
            if solve_in_depth(extension, n - 1):
                return puzzle.generate_strings(extension)
        # for extension in puzzle.extensions():
        #     if valid_state(extension, n - 1):
        #         return puzzle.generate_strings(extension)
        return 'No possible extensions!'


def solve_in_depth(puzzle, n):
    """Returns whether or not the puzzle can be solved in the next <n> steps.

    @type puzzle: Puzzle
    @type n: int
        The 'depth' / number of moves that should be explored.
    @rtype: bool
    """
    if puzzle.is_solved():
        return True
    elif n == 0:
        return False
    else:
        for extension in puzzle.extensions():
            sol = solve_in_depth(extension, n - 1)
            if sol:
                return sol
    return False


def valid_state(puzzle, n):
    """Return whether or not the puzzle can still be in a valid state after <n> moves.

    @type puzzle: Puzzle
    @type n: int
        The 'depth' or the number of moves that should be explored.
    @rtype: bool
    """
    if n == 0:
        if len(puzzle.extensions()) > 0:
            return True
    else:
        for extension in puzzle.extensions():
            sol = valid_state(extension, n - 1)
            if sol:
                return sol
    return False


def hint_by_breadth(puzzle):
    """Return a hint for the given puzzle. Used for word ladder puzzle.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution, return the string 'No possible extensions!'

    @type puzzle: WordLadderPuzzle
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    else:
        solution = solve_in_breadth(puzzle)
        if solution[0]:
            return solution[1]
        return 'No possible extensions!'


def solve_in_breadth(puzzle, hint=True):
    """Returns whether or not the puzzle can be solved using breadth-first search . If it can be solved, return the
    next word to be inputted if hint is true, otherwise return the final solved puzzle.

    @type puzzle: WordLadderPuzzle
    @rtype: (bool, str)
    """
    queue = collections.deque()
    queue.append(puzzle)
    used_words = []
    while len(queue) > 0:
        extensions = queue.popleft().extensions()
        for extension in extensions:
            extension.add_tried_words(used_words)
            if extension.is_solved():
                if hint:
                    chain = extension.used_words()
                    i = chain.index(puzzle.start_word())
                    return True, chain[i+1]
                else:
                    return True, extension
            else:
                queue.append(extension)
                used_words.append(puzzle.generate_strings(extension))
    return False, None
