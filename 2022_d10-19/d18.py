from collections import defaultdict, Counter
import re
from pprint import pp

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


def get_answer(input_): 
    total = 0
    examined = []
    data = get_data(input_)
    for x,y,z in data:
        total += 6
        for xe,ye,ze in examined:
            if (x,y,z) == (xe,ye,ze):
                continue
            if x == xe and y == ye and abs(z - ze) == 1:
                total -= 2
            if z == ze and y == ye and abs(x - xe) == 1:
                total -= 2
            if x == xe and z == ze and abs(y - ye) == 1:
                total -= 2
        examined.append((x,y,z))
    print (total)
 

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

def get_volume(xmax, xmin, ymax, ymin, zmax, zmin):
    return abs(xmin-xmax)*abs(ymin-ymax)*abs(zmin-zmax)


neighbors = ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1),)

def get_neighbors(x,y,z):
    for neighbor in neighbors:
        yield addcoords(x,y,z,*neighbor)



class Lava:
    def __init__(self, input_):
        self.data = get_data(input_)
        xmax, xmin, ymax, ymin, zmax, zmin = get_maxes(input_)
        self.known_outside = {}
        self.cache_hits = 0
        
        xfloor = xmin - 1
        xceiling = xmax + 1
        self.xlimits = (xfloor, xceiling)
        
        yfloor = ymin - 1
        yceiling = ymax + 1
        self.ylimits = (yfloor, yceiling)
        
        zfloor = zmin - 1
        zceiling = zmax + 1
        self.zlimits = (zfloor, zceiling)

    
    def recurse_to_yonder(self, x,y,z, visited=None):
        debug = False
        if (x,y,z) == (2,5,5):
            debug = True

        if cached := self.known_outside.get((x,y,z)):
            self.cache_hits += 1
            return cached
        if x in self.xlimits or y in self.ylimits or z in self.zlimits:
            self.known_outside[(x,y,z)] = True
            return True
        if visited is None:
            visited = []
        visited.append((x,y,z))
        for nx,ny,nz in get_neighbors(x,y,z):
            if debug:
                print(nx,ny,nz)
            if (nx,ny,nz) in self.data:
                continue
            if (nx,ny,nz) in visited:
                continue
            if nx in self.xlimits or ny in self.ylimits or nz in self.zlimits:
                return True
            new_visited = visited.copy()
            if result := self.recurse_to_yonder(nx, ny, nz, new_visited):
                self.known_outside[(x,y,z)] = True
                return result
        


def crawl_neighbors(input_):
    data = get_data(input_)
    results = defaultdict(list)
    other_total = 0
    total = 0
    lava_lurker = Lava(input_)
    for d in data:
        for n in neighbors:
            potential = addcoords(*d,*n)
            if potential in data:
                continue
            other_total += 1
            if lava_lurker.recurse_to_yonder(*potential):
                if potential == (2,2,5):
                    print ("Wtf")
                print(potential)
                total+=1
    return other_total, total, lava_lurker

other_total, total, lava_lurker = crawl_neighbors(sample)
