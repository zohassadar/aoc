from collections import defaultdict, Counter
import re
from pprint import pp
from queue import Queue

sample = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

real = open('d18.input').read()

def get_data(input_):
    numbers = re.findall('(\d+),(\d+),(\d+)', input_)
    numbers = [(int(a),int(b),int(c)) for a,b,c in numbers]
    return numbers

def addcoords(a,b,c,x,y,z):
    return a+x, b+y, c+z

def get_maxes(input_):
    data = get_data(input_)

    x = [c[0] for c in data]
    xmax = max(x)
    xmin = min(x)

    y = [c[1] for c in data]
    ymax = max(y)
    ymin = min(y)

    z = [c[2] for c in data]
    zmax = max(z)
    zmin = min(z)
    return xmax, xmin, ymax, ymin, zmax, zmin


neighbors = ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1),)

def get_neighbors(x,y,z):
    for neighbor in neighbors:
        yield addcoords(x,y,z,*neighbor)

class Lava:
    def __init__(self, input_, debug=False):
        self.debug = debug
        self.data = get_data(input_)
        xmax, xmin, ymax, ymin, zmax, zmin = get_maxes(input_)
        self.known_outside = set()
        self.cache_hits = 0
        
        xfloor = xmin - 2
        xceiling = xmax + 2
        self.xlimits = (xfloor, xceiling)
        
        yfloor = ymin - 2
        yceiling = ymax + 2
        self.ylimits = (yfloor, yceiling)
        
        zfloor = zmin - 2
        zceiling = zmax + 2
        self.zlimits = (zfloor, zceiling)
        self.visited = []
        self.queue = Queue()
        self.queue.put((xfloor+1,yfloor+1,zfloor+1))
        self.find_outside_neighbors()
        self.find_answers()

    def find_outside_neighbors(self):
        while True:
            if self.queue.empty():
                self.debug and print('Empty Queue.  Ending')
                break
            space = self.queue.get()
            if space in self.visited:
                self.debug and print('Been here already')
                continue
            self.visited.append(space)
            if space in self.data:
                self.debug and print('This is part of the lava.  Skipping')
                continue
            x,y,z = space
            if x in self.xlimits or y in self.ylimits or z in self.zlimits:
                self.debug and print(f'{x=} {y=} {z=} is beyond {self.xlimits=} {self.ylimits=} {self.zlimits=}')
                continue
            self.known_outside.add(space)
            self.debug and print(f'{x=} {y=} {z=} is outside')
            for neighbor in get_neighbors(*space):
                if neighbor in self.visited or neighbor in self.data:
                    continue
                self.queue.put(neighbor)


    def find_answers(self):
        star1 = 0
        star2 = 0
        for d in self.data:
            for n in neighbors:
                potential = addcoords(*d,*n)
                if potential in self.data:
                    continue
                star1 += 1
                if potential in self.known_outside:
                    star2+=1
        print (f"Star1: {star1}  Star2: {star2}")



Lava(sample)
Lava(real)
