import re
import numpy as np
from collections import defaultdict, deque
from pprint import pp

real = open("d22.input").read()


sample = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def get_data(text):
    grid, steps = text.split("\n\n")
    size = 1000

    for line in grid.splitlines():
        if not line.strip():
            continue
        size = min(len(re.findall(r"[.#]", line)), size)

    sub_grids = defaultdict(list)
    for sub_y, sublines in enumerate(zip(*[iter(grid.splitlines())] * size)):
        for subline in sublines:
            for sub_x, groups in enumerate(zip(*[iter(subline)] * size)):
                if groups == tuple([" "] * size):
                    continue
                sub_grids[(sub_y, sub_x)].extend([1 if g == "#" else 0 for g in groups])

    sub_grids = {k: np.array(v, dtype=int) for k, v in sub_grids.items()}
    sub_width = max(k[1] for k in sub_grids) + 1
    sub_height = max(k[0] for k in sub_grids) + 1
    grid = np.ones((sub_height, sub_width), dtype=int)
    for key in sub_grids:
        grid[key] = 0
    for subgrid in sub_grids.values():
        subgrid.shape = size, size
    steps = deque(int(i) if i.isdigit() else i for i in re.findall(r"[RL]|\d+", steps))
    return grid, sub_grids, steps


def add_pair(next_y, next_x, off_y, off_x, limit_y, limit_x):
    next_y += off_y
    next_x += off_x
    new_grid = True
    if next_y < 0:
        next_y = limit_y - 1
    elif next_y == limit_y:
        next_y = 0
    elif next_x < 0:
        next_x = limit_x - 1
    elif next_x == limit_x:
        next_x = 0
    else:
        new_grid = False
    return next_y, next_x, new_grid


class GroveRoamer:
    L = "L"
    R = "R"

    N = "N"
    S = "S"
    W = "W"
    E = "E"

    SCORE = {E: 0, S: 1, W: 2, N: 3}
    CLOCKWISE = dict(E=S, S=W, W=N, N=E)
    COUNTER = dict(E=N, N=W, W=S, S=E)
    flipx = flipy = None
    # clockwise = lambda (y, x, dir): flipy, flipx
    def get_trans(self, dir):
        def max_x(y, _):
            return y, self.max

        def zero_x(y, _):
            return y, 0

        def max_y(_, x):
            return self.max, x

        def zero_y(_, x):
            return 0, x

        def zero_y_x_inv_y(y, _):
            return 0, self.invert[y]

        def max_y_x_inv_y(y, _):
            return self.max, self.invert[y]

        def max_y_x_inv_x(_, x):
            return self.max, self.invert[x]

        def max_x_y_inv_x(_, x):
            return self.invert[x], self.max

        def max_x_y_inv_y(y, _):
            return self.invert[y], self.max

        def zero_x_y_inv_y(y, _):
            return self.invert[y], 0

        def zero_x_y_inv_x(_, x):
            return self.invert[x], 0

        def zero_x_y_is_x(_, x):
            return x, 0

        def zero_y_x_is_y(y, _):
            return 0, y

        def zero_y_x_inv_x(_, x):
            return 0, self.invert[x]

        def max_y_x_is_y(y, _):
            return self.max, y

        def max_x_y_is_x(_, x):
            return x, self.max

        def max_x_y_inv_y(y, _):
            return self.invert[y], self.max

        return {
            self.E: [
                ((0, 1), self.E, zero_x),
                ((1, 1), self.S, zero_y_x_inv_y),
                ((-1, 1), self.N, max_y_x_is_y),
                ((-2, -1), self.W, max_x_y_inv_y),
                ((2, 1), self.W, max_x_y_inv_y),
                ((2, -1), self.W, max_x_y_inv_y),
                ((-2, 1), self.W, max_x_y_inv_y),
            ],
            self.W: [
                ((0, -1), self.W, max_x),
                ((-3, 1), self.S, zero_y_x_is_y),
                ((-1, -1), self.N, max_y_x_inv_y),
                ((1, -1), self.S, zero_y_x_is_y),
                ((2, -1), self.E, zero_x_y_inv_y),
                ((-2, 1), self.E, zero_x_y_inv_y),
                ((1, 3), self.N, max_y_x_inv_y),
            ],
            self.N: [
                ((-1, 0), self.N, max_y),
                ((-1, -1), self.W, max_x_y_inv_x),
                ((-1, 1), self.E, zero_x_y_is_x),
                ((1, -2), self.S, zero_y_x_inv_x),
                ((-1, 2), self.S, zero_y_x_inv_x),
                ((3, -1), self.E, zero_x_y_is_x),
                ((3, -2), self.N, max_y),
            ],
            self.S: [
                ((1, 0), self.S, zero_y),
                ((1, 1), self.E, zero_x_y_inv_x),
                ((1, -1), self.W, max_x_y_is_x),
                ((-1, -2), self.N, max_y_x_inv_x),
                ((1, 2), self.N, max_y_x_inv_x),
                ((-1, -3), self.W, zero_x_y_inv_x),
                ((-3, 2), self.S, zero_y),
            ],
        }[dir]

    MOVES = {
        N: (-1, 0),
        S: (1, 0),
        W: (0, -1),
        E: (0, 1),
    }

    NEXT = {
        (N, L): W,
        (N, R): E,
        (S, L): E,
        (S, R): W,
        (W, L): S,
        (W, R): N,
        (E, L): N,
        (E, R): S,
    }

    def __init__(self, text, debug=False, cube=False):
        self.cube = cube
        self.debug = debug
        self.grid, self.sub_grids, self.steps = get_data(text)
        self.size = next(iter(self.sub_grids.values())).shape[0]
        self.current_grid = next(iter(self.sub_grids))
        self.current_pos = (0, 0)
        self.current_dir = self.E
        self.max = self.size - 1
        self.invert = {
            old: new for old, new in zip(range(self.size), range(self.size - 1, -1, -1))
        }
        self.next_grid = {}
        if self.cube:
            self.scan_sides()

        self.roam()
        self.print_score()

    def scan_sides(self):
        i = 0
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[y, x]:
                    continue
                for dir in self.SCORE:
                    possibilities = self.get_trans(dir)
                    for poss in possibilities:
                        (off_y, off_x), new_dir, mutate = poss
                        new_y, new_x = off_y + y, off_x + x
                        if new_y < 0 or new_x < 0:
                            continue
                        try:
                            if self.grid[new_y, new_x]:
                                continue
                        except IndexError:
                            continue
                        i += 1
                        self.next_grid[(y, x, dir)] = new_y, new_x, new_dir, mutate
                        self.debug and print(
                            f"{i:<2} ({y}, {x}, {dir}) -> ({new_y}, {new_x}, {new_dir}) {mutate.__name__}"
                        )

                        break

    def print_score(self):
        y, x = self.current_pos
        gy, gx = self.current_grid
        y = gy * self.size + y + 1
        x = gx * self.size + x + 1
        print(y * 1000 + x * 4 + self.SCORE[self.current_dir])

    def new_grid(self):
        move = self.MOVES[self.current_dir]
        next_grid_y, next_grid_x, _ = add_pair(
            *move, *self.current_grid, *self.grid.shape
        )
        grid_test = self.grid[next_grid_y, next_grid_x]
        while grid_test:
            next_grid_y, next_grid_x, _ = add_pair(
                *move, next_grid_y, next_grid_x, *self.grid.shape
            )
            grid_test = self.grid[next_grid_y, next_grid_x]
        return next_grid_y, next_grid_x, self.current_dir, lambda y, x: (y, x)

    def go_one_move(self):
        """-> next_grid, next_coord"""
        start_y, start_x = self.current_pos
        grid_y, grid_x = self.current_grid
        self.debug and print(f"{start_y=} {start_x=} {grid_y=} {grid_x=}")

        move = self.MOVES[self.current_dir]
        next_grid_y, next_grid_x = self.current_grid
        next_y, next_x, new_grid = add_pair(
            *move, *self.current_pos, self.size, self.size
        )
        mutator = lambda y, x: (y, x)
        next_dir = self.current_dir
        if new_grid and not self.cube:
            next_grid_y, next_grid_x, next_dir, mutator = self.new_grid()
        elif new_grid:
            next_grid_y, next_grid_x, next_dir, mutator = self.next_grid[
                (*self.current_grid, self.current_dir)
            ]
        if self.sub_grids[next_grid_y, next_grid_x][mutator(next_y, next_x)]:
            next_y, next_x = self.current_pos
            next_grid_y, next_grid_x = self.current_grid
            next_dir = self.current_pos
            mutator = lambda y, x: (y, x)
        self.debug and print(f"{next_y=} {next_x=} {next_grid_y=} {next_grid_x=}")
        next_y, next_x = mutator(next_y, next_x)
        return (next_y, next_x), (next_grid_y, next_grid_x), next_dir

    def visualize(self):
        for y, row in enumerate(self.grid):
            for i in range(self.size):
                for x, col in enumerate(row):
                    if col:
                        print(" " * self.size, end="")
                        continue
                    print(
                        "".join("#" if e else "." for e in self.sub_grids[(y, x)][i]),
                        end="",
                    )
                print("")

    def roam(self):
        while self.steps:
            next_step = self.steps.popleft()
            if isinstance(next_step, int):
                for _ in range(next_step):
                    next_pos, next_grid, next_dir = self.go_one_move()
                    if next_pos == self.current_pos and next_grid == self.current_grid:
                        break
                    self.current_dir = next_dir
                    self.current_pos = next_pos
                    self.current_grid = next_grid
            else:
                self.current_dir = self.NEXT[self.current_dir, next_step]


s = GroveRoamer(sample)
s = GroveRoamer(real)
s = GroveRoamer(sample, cube=True)
r = GroveRoamer(real, cube=True)
# r.scan_sides()
