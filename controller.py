"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth, hint_by_breadth


class Controller:
    """Class responsible for connection between puzzles and views.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller.
    # @type _view: View
    #     The view associated with this game controller.
    # @type _tree: _ControllerTree
    #     The entire tree associated with this controller.
    # @type _current_tree: _ControllerTree
    #     The tree that represents the current state of the puzzle.

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._tree = _ControllerTree(puzzle)
        self._current_tree = self._tree
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
            A string representation of the puzzle state.
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
            The user input.
        @rtype: (str, bool)
            The current state of the puzzle or a message and whether the program should end.
        """
        if action == 'exit':
            return '', True
        elif action == ':SOLVE':
            return self._act_solve()
        elif action == ':SOLVE-ALL':
            return self._act_solve_all()
        elif action == ':UNDO':
            return self._act_undo()
        elif action == ':ATTEMPTS':
            return self._act_attempts()
        elif action == ":HINT":
            return self._act_hint()
        elif action == ":DISPLAY":
            return str(self._puzzle), False
        else:
            try:
                return self._act_move(action)
            except ValueError:
                return 'Sorry, that is not a valid move. Please try again.', False

    def _act_solve(self):
        """Returns a solution of the puzzle if there is one or 'There are no solutions.' if no solutions exist, and
        tells the program to end.

        @type self: Controller
        @rtype: (str, bool)
        """
        solution = solve(self._puzzle)
        if solution is not None:
            return str(solution), True
        else:
            return 'There are no solutions.', True

    def _act_solve_all(self):
        """Returns all the solution of the puzzle if there exists any or 'There are no solutions.' if no solutions
        exist, and tells the program to end.

        @type self: Controller
        @rtype: (str, bool)
        """
        all_solutions = ''
        solutions = solve_complete(self._puzzle)
        for solution in solutions:
            all_solutions += str(solution) + '\n'
        if all_solutions != '':
            return all_solutions, True
        else:
            return 'There are no solutions.', True

    def _act_undo(self):
        """Returns the previous puzzle state if there is one or 'You have not made any moves.' if there is no previous
        state, and tells the program not to end.

        @type self: Controller
        @rtype: (str, bool)
        """
        previous_state_tree = self._current_tree.find_parent(self._tree)
        if previous_state_tree is not None:
            self._current_tree = previous_state_tree[0]
            self._puzzle = previous_state_tree[1]
            return self.state(), False
        else:
            return 'You have not made any moves.', False

    def _act_attempts(self):
        """Prints all the puzzle states that have been reached from this puzzle state and tells the program not to end.

        @type self: Controller
        @rtype: (str, bool)
        """
        puzzle_state, move = self._current_tree.return_subtrees()
        if len(puzzle_state) == 0:
            return 'You have never reached this state before.', False
        else:
            for i in range(len(puzzle_state)):
                print('You attempted... \n' + str(puzzle_state[i]) + "\nYour move was '" + move[i] + "'\n")
            return '', False

    def _act_hint(self):
        """Returns a hint that will either solve the puzzle, or if the the puzzle leads to no more moves, return
        'No possible extensions!'. If the puzzle is already solved, return 'Already at a solution!'. Also, tells the
        program not to end.

        @type self: Controller
        @rtype: (str, bool)
        """
        if type(self._puzzle) == WordLadderPuzzle:
            hint = hint_by_breadth(self._puzzle)
        else:
            hint = hint_by_depth(self._puzzle)

        return 'Try entering: ' + hint, False

    def _act_move(self, action):
        """Updates the state of the puzzle according to <action>. Returns 'Congratulations, you solved it!' and tells
        the program to end if the puzzle is solved or returns the new state of the puzzle and tells the program not to
        end.

        @type self: Controller
        @type action: str
            The user input.
        @rtype: (str, bool)
        """
        self._puzzle = self._puzzle.move(action)
        if self._current_tree.in_subtree(self._puzzle):
            self._current_tree = self._current_tree.in_subtree(self._puzzle)
        else:
            new_subtree = _ControllerTree(self._puzzle, action)
            self._current_tree.add_subtree(new_subtree)
            self._current_tree = new_subtree
        if self._puzzle.is_solved():
            return 'Congratulations, you solved it!', True
        return self.state(), False


class _ControllerTree:
    """A tree class responsible for keeping track of all the states of a puzzle. It should only be used by the
    controller class.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle state associated with this tree.
    # @type _user_input: str
    #     The user input that led to the puzzle state.
    # @type _subtrees: [_ControllerTree]
    #     A list of the puzzle states that resulted from making one move to this puzzle state.

    # === Representation Invariants ===
    # An empty _ControllerTree cannot be created, it must have a valid puzzle state associated with it.
    # Only the initial _ControllerTree, which has no parent, has _user_input is None.
    def __init__(self, puzzle, move=None):
        """Initialize a new _ControllerTree representing a puzzle state. The puzzle state and the move made to reach
        the puzzle state are saved as attributes.

        @type puzzle: Puzzle
        @type move: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._user_input = move
        self._subtrees = []

    def add_subtree(self, subtree):
        """Add a new subtree representing a new puzzle state reached by making one move from the original puzzle
        state.

        @type self: _ControllerTree
        @type subtree: _ControllerTree
        @rtype: None
        """
        self._subtrees.append(subtree)

    def in_subtree(self, puzzle_state):
        """Return the subtree that represents <puzzle_state>. If no such subtree exists, return None.

        @type self: _ControllerTree
        @type puzzle_state: Puzzle
        @rtype: _ControllerTree | None
        """
        for subtree in self._subtrees:
            if str(subtree._puzzle) == str(puzzle_state):
                return subtree
        return None

    def find_parent(self, family_tree):
        """Find and return the tree in <family_tree> that <self> is a subtree of and the puzzle associated with the
        tree. If <self> does not have a parent, return None.

        @type self: _ControllerTree
        @type family_tree: _ControllerTree
        @rtype: (_ControllerTree, Puzzle) | None
        """
        if self._user_input is None:
            return None
        elif self in family_tree._subtrees:
            return family_tree, family_tree._puzzle
        else:
            for subtree in family_tree._subtrees:
                if self.find_parent(subtree) is not None:
                    return self.find_parent(subtree)
            return None

    def return_subtrees(self):
        """Return a tuple of a list of all the puzzle states of the subtrees and a list of the moves it took to get to
        each subtree.

        @type self: _ControllerTree
        @rtype: ([Puzzle], [str])
        """
        puzzle = []
        moves = []
        for subtree in self._subtrees:
            puzzle.append(subtree._puzzle)
            moves.append(subtree._user_input)
        return puzzle, moves


def main():
    """Prompt the user to configure and play the game.

    @rtype: None
    """
    game = input("Do you want to play Sudoku (s) or Word Ladder (w)? ")
    while game != "s" and game != "w":
        print("That is not a valid input.")
        game = input("Do you want to play Sudoku (s) or Word Ladder (w)? ").lower()

    if game == "s":
        view_type = "text"
        g = SudokuPuzzle([['', '', '', 'A'],
                      ['D', '', 'B', ''],
                      ['C', '', '', ''],
                      ['', 'B', '', 'D']])
        print("\n\nTo make a move: use the format (<row>, <column>) -> letter.")
    elif game == "w":
        view_type = input("Would you like to play in text mode or web mode? ").lower()
        if view_type != "web"and view_type != "text":
            print("That is not a valid mode, you will be playing in text mode.")
            view_type = "text"
        choice = input("Do you want to choose your start and end words? (y/n) ")
        if choice == "y":
            print("Your starting and ending words should have the same length.")
            start = input("What would you like your starting word to be? ")
            end = input("What would you like your ending word to be? ")
            while len(start) != len(end):
                print("Your starting and ending words don't have the same length. Please try again.")
                start = input("What would you like your starting word to be? ")
                end = input("What would you like your ending word to be? ")
        else:
            start = "rock"
            end = "taco"
        g = WordLadderPuzzle(start, end)
        print("\n\nTo make a move, type a word which does not differ by more than one letter from the current word.")

    if view_type == "text":
        print("To quit the game, type exit.")
        print("To ask for a solution, type :SOLVE.")
        print("To ask for a hint, type :HINT.")
        print("To undo a move, type :UNDO.")
        print("To look at your past moves from this current game state, type :ATTEMPTS.\n")

    c = Controller(g, mode=view_type)


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle

    main()
