import numpy as np
from itertools import cycle
from collections import defaultdict, deque

MIN_PATTERN = 2 

sample = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

real = open('d17.input').read()

conv_movements = lambda mvmnts: [1 if m == ">" else -1 for m in mvmnts if m in "<>"]

direction = {1: "right", -1: "left"}

orientation = {
    0: (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
    ),
    1: (
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 1),
    ),
    2: (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ),
    3: (
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
    ),
    4: (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ),
}


def show_grid(array):
    # array = array
    array = np.flip(array, axis=0)
    for y, row in enumerate(array):
        # print(f"{y:<2}:", end="")
        for x, col in enumerate(row):
            print("@" if col == -1 else "#" if col else ".", end="")
        print("")


class Game:
    def __init__(self, movements=sample, limit=2022, debug=False, shortcut=False):
        self.shortcut = shortcut
        self.debug = debug
        self.limit = limit
        self.grid = np.zeros((7, 7), dtype=int)
        self.pieces = cycle(enumerate(orientation.values()))
        self.movements = cycle(enumerate(conv_movements(movements)))
        self.cycle = 0
        self.pi, self.current_piece = next(self.pieces)
        self.mi, self.current_move = next(self.movements)
        self.top = 0
        self.y = 3
        self.x = 2
        self.y_trimmed = 0
        self.last_height = {i: 0 for i in orientation}
        self.last_cycle = {i: 0 for i in orientation}
        self.differences = {i: deque(maxlen=MIN_PATTERN) for i in orientation}

    @property
    def height(self):
        return self.y_trimmed + self.top

    def is_valid(self, yoff, xoff):
        for pyoff, pxoff in self.current_piece:
            try:
                new_y = yoff + pyoff
                new_x = xoff + pxoff
                if new_y < 0 or new_x < 0 or new_x > 7:
                    self.debug and print (f"{yoff + pyoff}, {xoff + pxoff} out of bounds")
                    return False
                existing = self.grid[new_y, new_x]
                if existing:
                    self.debug and print (f"{yoff + pyoff}, {xoff + pxoff} overlaps")
                    return False
            except IndexError:
                self.debug and print (f"{yoff + pyoff}, {xoff + pxoff} out of bounds (IndexError)")
                return False
        return True

    def new_piece_print(self):
        if not self.debug:
            return
        array = self.grid.copy()
        self.store_piece(array, self.y, self.x, -1)
        show_grid(array)

    def move_things_along(self):
        if not self.shortcut:
            return
        if self.mi:
            return
        y_diff = self.height - self.last_height[self.pi]
        if not y_diff:
            return
        
        self.last_height[self.pi] = self.height

        cyc_diff = self.cycle - self.last_cycle[self.pi]
        self.last_cycle[self.pi] = self.cycle
        self.differences[self.pi].append((y_diff, cyc_diff))
        if not (len(self.differences[self.pi]) == MIN_PATTERN and len(set(self.differences[self.pi])) == 1):
            return
        offsets, cycles = self.differences[self.pi].pop()
        remaining = (self.limit - self.cycle) // cycles
        self.cycle += cycles * remaining
        self.y_trimmed += offsets * remaining


    def move_over(self):
        self.move_things_along()
        dir_ = direction[self.current_move]
        future_x = self.x + self.current_move

        if self.is_valid(self.y, future_x):
            self.x = future_x
        self.mi, self.current_move = next(self.movements)
        self.debug and print(f"Moved {dir_}:")
        self.new_piece_print()

    def move_down(self):
        future_y = self.y - 1
        is_valid = self.is_valid(future_y, self.x)
        if is_valid:
            self.y = future_y
        self.debug and print(f"{self.y=} {self.x=} Moved down {is_valid=}:")
        self.new_piece_print()
        if self.y != future_y:
            self.store_piece(self.grid, self.y, self.x)
            self.next_piece()

    def store_piece(self, array, y, x, value=1):
        # self.debug and print(f"Storing Piece {y=} {x=}")
        for yoff, xoff in self.current_piece:
            array[yoff + y, xoff + x] = value

    def next_piece(self):
        self.cycle += 1
        self.pi, self.current_piece = next(self.pieces)
        self.x = 2
        self.top = next(iter(reversed(np.where( self.grid == 1 )[0]))) + 1
        self.y = self.top + 3
        diff = self.y + 4 - self.grid.shape[0]
        self.debug and print (f"{self.top=} {diff=} more")
        self.grid = np.vstack((self.grid, np.zeros((diff,7))))

    def play_game(self):
        self.debug and print (f"{self.x=} {self.y=} Starting Game")
        self.new_piece_print()
        while self.cycle < self.limit:
            self.move_over()
            self.move_down()


if __name__ == "__main__":
    g = Game(movements=sample, debug=True, limit=2022, shortcut=True)
    g.play_game()
    print(g.height)
    g = Game(movements=real, debug=False, limit=2022, shortcut=True)
    g.play_game()
    print(g.height)
    g = Game(movements=sample, debug=False, limit=1000000000000, shortcut=True)
    g.play_game()
    print(g.height)
    g = Game(movements=real, debug=False, limit=1000000000000, shortcut=True)
    g.play_game()
    print(g.height)