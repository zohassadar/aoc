import re
import numpy as np
from itertools import permutations
from collections import defaultdict

DEBUG = False

sample="""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

real = open('d15.input').read()

def get_data(input_):
    numbers = re.findall(r'-?\d+', input_)
    integers = [int(n) for n in numbers]
    array = np.array(integers)
    array.shape = len(array)//4,4
    return array

def consolidate(overlaps):
    overlaps.sort()
    matches = False
    replaced = list()
    results = set()
    while not matches:
        if len(overlaps) < 2:
            return overlaps
        original = overlaps.copy()
        results=set()
        for saea, sbeb in permutations(overlaps, 2):
            if saea in replaced or sbeb in replaced:
                continue
            (sa, ea), (sb, eb) = saea, sbeb
            if sb > sa and eb < ea:
                results.add(saea)
                replaced.append(sbeb)
                continue
            if sa > sb and ea < eb:
                results.add(sbeb)
                replaced.append(saea)
                continue
            DEBUG and print(f"({sa}, {ea}) compared to ({sb}, {eb})")
            cond1 = sa <= eb and sb <= ea + 1
            cond2 = sb <= ea and sa <= eb + 1
            if cond1:
                DEBUG and print(f"({sa} <= {eb}),({sb} <= {ea})")
            if cond2:
                DEBUG and print(f"({sb} <= {ea}),({sa} <= {eb})")
            if cond1 or cond2:
                result = (min((sb,sa)), max((ea,eb)))
                if result != saea:
                    replaced.append(saea)
                elif result != sbeb:
                    replaced.append(sbeb)
                results.add(result)
            else:
                results.add(saea)
                results.add(saea)
        overlaps = sorted([r for r in results if r not in replaced])
        matches = overlaps == original

    return original


class Sensor:
    def __init__(self, x, y, cbx, cby, debug=False):
        self.debug = debug
        self.x = x
        self.y = y 
        self.cbx = cbx
        self.cby = cby
        xdist = abs(x - cbx)
        ydist = abs(y - cby)
        self.debug and print(f"!{x},{y} -> {cbx},{cby}")
        self.debug and print(f"abs({x=} - {cbx=}) = {xdist=} abs({y=} {cby=}) = {ydist=}")
        self.distance = xdist + ydist
        

    def known_empties(self, y):
        dist = abs(self.y - y)
        if dist > self.distance:
            return 
        gap = self.distance - dist
        start_gap = self.x - gap
        end_gap = self.x + gap
        self.debug and print(f'Empties:  {y=} {self.y=} {dist=} {self.distance=} {gap} {start_gap} {end_gap}')
        if not y == self.cby:
            return ((start_gap, end_gap))
        if self.cbx == start_gap:
            return ((start_gap+1, end_gap))
        if self.cbx == end_gap:
            return ((start_gap, end_gap-1))
        
    def __repr__(self):
        return f'Sensor(x={self.x}, y={self.y}, cbx={self.cbx}, cby={self.cby})[Distance: {self.distance}]'



class Sensors:
    def __init__(self, input_, debug=False):
        global DEBUG
        DEBUG = debug
        self.sensors = [Sensor(*row, debug=debug) for row in get_data(input_)]
        self.beacons = defaultdict(list)
        for sensor in self.sensors:
            self.beacons[sensor.cby].append((sensor.cbx, sensor.cbx))

    def get_gaps(self, y, add_beacons=False):
        gaps = [s.known_empties(y) for s in self.sensors]
        gaps = [g for g in gaps if g]
        if add_beacons:
            gaps.extend(self.beacons[y])
        return consolidate(gaps)

    def what_cant_be(self, y):
        consolidated = self.get_gaps(y)
        return sum(abs(x-y)+1 for x,y in consolidated)


    def sweep(self, lower, upper):
        from time import perf_counter
        then = perf_counter()
        broken = False
        for y in range(upper, lower-1, -1):
            if broken:
                break
            for start, end in self.get_gaps(y, add_beacons=True):
                if start < lower and end > upper:
                    continue
                if start >= lower:
                    x = start-1
                elif end <= upper:
                    x = end+1
                print(f"{y=} {x=}.  Result is {x*4000000+y}")
                broken = True
                break
        print(f"That took {perf_counter() - then} seconds to do")
                

sensor = Sensors(sample)
print(sensor.what_cant_be(10))

sensor.sweep(0,20)

sensor = Sensors(real)
print(sensor.what_cant_be(2000000))

sensor.sweep(0,4000000)