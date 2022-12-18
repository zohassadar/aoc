import numpy as np
from itertools import pairwise

sample = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


real = open('d14.input').read()


moves = dict(down=(1,0), downleft=(1,-1), downright=(1,1))

def show_grid(array, xmin):
    for y, row in enumerate(array):
        for x, col in enumerate(row):
            if x < xmin:
                continue
            print('#' if col == 1 else "o" if col == -1 else " ", end="")
        print("")
    

def get_data(input_, floor=False):
    results = []
    xmax = 0
    ymax = 0
    xmin = 500
    for line in input_.splitlines():
        result = []
        for xy in line.split(" -> "):
            x,y = xy.split(",")
            x,y = int(x), int(y)
            xmax = max((x,xmax))
            ymax = max((y,ymax))
            xmin = min((x,xmin))
            result.append((x,y))
        results.append(tuple(result))
    if floor:
        array = np.zeros((ymax+3, xmax+1+ymax),dtype=int)
        array[-1,:] = 1
    else:
        array = np.zeros((ymax+1, xmax+1),dtype=int)
    for result in results:
        for (x1,y1),(x2,y2) in pairwise(result):
            x1,x2 = sorted([x1,x2])
            y1,y2 = sorted([y1,y2])
            for x in range(x1,x2+1):
                for y in range(y1,y2+1):
                    array[y,x] =1
    return array, xmin

class Faller:
    def __init__(self, input_, debug=False, floor=False):
        self.debug = debug
        self.grid, self.xmin = get_data(input_, floor)
        self.grains = 0
        self.x = 500
        self.y = 0
        self.end = False

    def is_valid(self, yoff, xoff):
        new_y = self.y + yoff
        new_x = self.x + xoff
        try:
            existing = self.grid[new_y, new_x]
            if existing:
                self.debug and print (f"{new_y}, {new_x} overlaps")
                return False
        except IndexError:
            self.debug and print (f"{new_y}, {new_x} out of bounds (IndexError)")
            self.end = True
        return True

    def new_piece_print(self):
        if not self.debug:
            return
        show_grid(self.grid, self.xmin)


    def fall_the_sand(self):
        for move, (yoff,xoff) in moves.items():
            self.debug and print(f"Moving {move} ({yoff=}, {xoff=})")
            if self.is_valid(yoff, xoff):
                self.debug and print(f"{move} is valid")
                self.x += xoff
                self.y += yoff
                break
            elif self.end:
                return
        else:
            self.debug and print(f"No moves.  Planting")
            self.grid[self.y, self.x] = -1
            self.next_sand()


    def next_sand(self):
        self.grains += 1
        if self.y == 0 and self.x == 500:
            self.end=True
            return
        self.x = 500
        self.y = 0
    
    def start_falling(self):
        self.debug and print (f"{self.x=} {self.y=} Starting Game")
        self.new_piece_print()
        while not self.end:
            self.fall_the_sand()



f = Faller(sample, debug=False)
f.start_falling()
print(f"Sample star 1: {f.grains}")

f = Faller(real, debug=False)
f.start_falling()
print(f"Real star 1: {f.grains}")

f = Faller(sample, debug=False, floor=True)
f.start_falling()
print(f"Sample star 2: {f.grains}")

f = Faller(real, floor=True)
f.start_falling()
print(f"Real star 2: {f.grains}")

