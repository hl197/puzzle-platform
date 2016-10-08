"""Word ladder module.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""

    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words.
    # @type _start: str
    #     The starting word of this puzzle. Every character of the starting word must be a lowercase letter.
    # @type _target: str
    #     The target word of this puzzle. The target word must contain the same number of characters as the starting
    #     word. Every character of the target word must be a lowercase letter.
    # @type _used_words: (str)
    #     A tuple of all the words that have already been used in this puzzle.

    def __init__(self, start, target, used_words=()):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @type used_words: tuple
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                if len(line.strip()) == len(start):
                    self._words.append(line.strip())
        self._start = start
        self._target = target
        self._used_words = used_words + (start, )
        self._tried_words = []

    def __str__(self):
        """Return a human-readable string representation of <self>.

        @type self: WordLadderPuzzle
        @rtype: str
            A string representation of the word ladder.
        >>> w = WordLadderPuzzle('house', 'party', ('mouse', ))
        >>> str(w)
        word chain:
        house -> mouse
        target word: party
        """
        s = 'word chain: ' + '\n'
        for word in self._used_words[:-1]:
            s += word + ' -> '
        s += self._used_words[-1] + '\ntarget word: ' + self._target
        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A word latter puzzle is solved if the start word is the same as the target word.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w = WordLadderPuzzle('bat', 'cat')
        >>> w.is_solved()
        False
        >>> w = WordLadderPuzzle('cat', 'cat')
        >>> w.is_solved()
        True
        """
        return self._start == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        new_words = self._possible_words()
        new_states = []
        for word in new_words:
            new_states.append(self._extend(word))
        return new_states

    def _possible_words(self):
        """Return a list of possible new words in alphabetical order by changing one letter of the current word.

        @type self: WordLadderPuzzle
        @rtype: List[str]
            The list of possible words.
        """
        new_words = []
        for word in self._words:
            if word not in (self._used_words + tuple(self._tried_words)):
                for i in range(len(self._start)):
                    if word[:i] + word[i+1:] == self._start[:i] + self._start[i+1:]:
                        new_words.append(word)
        new_words.sort()
        return new_words

    def _extend(self, word):
        """Return a new Word Ladder Puzzle obtained after changing the current word to <word>.

        @type self: WordLadderPuzzle
        @type word: str
            The new word in the word ladder puzzle.
        @rtype: WordLadderPuzzle
            The new word ladder puzzle.
        """
        return WordLadderPuzzle(word, self._target, self._used_words)

    def move(self, move):
        """Return a new Word Ladder Puzzle specified by making the given move.

        Raise a ValueError if <move> represents an invalid move, such as the new word not
        being a one-letter change from the original word.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzlePuzzle
        """
        possible_words = self._possible_words()
        if move not in possible_words:
            raise ValueError
        else:
            return self._extend(move)

    def generate_strings(self, new_puzzle):
        """Return a string representation of the move the user should make to get from <self> to <new_puzzle>.

        @type self: WordLadderPuzzle
        @type new_puzzle: WordLadderPuzzle
        @rtype: str
        >>> s = WordLadderPuzzle('fit', 'pot')
        >>> w = WordLadderPuzzle('pit', 'pot', ('fit', ))
        >>> s.generate_strings(w)
        'pit'
        """
        return new_puzzle._start

    def add_tried_words(self, tried_words):
        """Adds to the list of used words for the puzzle.

        @type self: WordLadderPuzzle
        @type tried_words: list
        @rtype: None
        """
        self._tried_words = tried_words

    def used_words(self):
        """Returns a tuple of words that have already been used in this puzzle.

        @type self: WordLadderPuzzle
        @rtype: tuple
        """
        return self._used_words

    def start_word(self):
        """Returns the starting word of this puzzle.

        @type self: WordLadderPuzzle
        @rtype: str
        """
        return self._start
