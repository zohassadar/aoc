import re

from pprint import pp
from copy import deepcopy
from sys import maxsize
from time import perf_counter
from json import dumps

DEBUG = False

sample = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

real = """
#############
#...........#
###D#A#B#C###
  #B#A#D#C#
  #########
"""

additional = """
  #D#C#B#A#
  #D#B#A#C#
"""


class Amphipod:
    def __init__(self, input_, debug=False, insert=False):
        if insert:
            splitup = input_.split("#\n  #")
            input_ = ''.join((splitup[0], additional, splitup[1]))
        self.debug = debug
        home_range = list(range(2,9,2))
        letters = re.findall("[ABCD]", input_)
        self.values = dict(A=1,B=10,C=100,D=1000)
        self.lookup={v:k for k,v in self.values.items()}
        self.mapping = dict(zip(home_range, self.values.values()))
        starts = iter(self.values[l] for l in letters)
        self.homes = list()
        self.homedepth = len(letters) // 4
        for _ in range(self.homedepth):
            self.homes.append({i: next(starts) for i in home_range})
        self.rest_areas = {i: 0 for i in range(0,11) if i not in self.homes[0]}
        self.moves = {}
        self.in_between = {}
        self.crap_cache = {}
        self.cache_hits = 0
        self.best_score = maxsize

        for home in self.homes[0]:
            for rest in self.rest_areas:
                distance = abs(rest - home) + 1
                self.moves[(home,rest)] = distance
                start, end = sorted([rest, home])
                self.in_between[(home,rest)] = tuple(i for i in range(start, end + 1) if i != rest and i in self.rest_areas)
        then = perf_counter()
        self.play_n_recurse(self.rest_areas, self.homes)
        print(f"That took {perf_counter() - then} seconds to come up with {self.best_score}")


    def play_n_recurse(self, rests, homes, cost=0):
        hashkey = dumps([rests, homes, cost])
        if self.crap_cache.get(hashkey):
            self.cache_hits += 1
            return
        if self.check_solved(homes):
            self.best_score = cost
            self.debug and print (f"Solved with a score of {cost}")
            return
        moves = self.get_moves_home(rests, homes)
        if not moves:
            moves = self.get_moves_rest(rests, homes)
        moves.sort()
        for added_cost, home_index, subindex, rest_index in moves:
            new_cost = added_cost + cost
            if new_cost >= self.best_score:
                continue
            new_rests = deepcopy(rests)
            new_homes = deepcopy(homes)
            new_rests[rest_index] = homes[subindex][home_index]
            new_homes[subindex][home_index] = rests[rest_index]
            self.play_n_recurse(new_rests, new_homes, new_cost)
        self.crap_cache[hashkey] = 1


    def path_is_clear(self, home_index, home_subindex, rest_index, homes, rests):
        for above in range(home_subindex):
            if home_subindex and homes[above][home_index]:
                return False
        for inb in self.in_between[home_index,rest_index]:
            if rests[inb]:
                return False
        return True

    def visualize(self, rests, homes):
        if not self.debug:
            return
        for r in range(3+self.homedepth):
            for i in range(13):
                if not r:
                    print("#", end="")
                if r == 1:
                    if i in (0,12):
                        print("#", end="")
                        continue
                    current = rests.get(i-1)
                    print(self.lookup[current] if current else ".", end="")
                if r == 2:
                    if i in (0,1,2,4,6,8,10,11,12):
                        print("#", end="")
                        continue
                    current = homes[0].get(i-1)
                    print(self.lookup[current] if current else ".", end="")
                if r >=3 and r < self.homedepth + 2:
                    if i in (2,4,6,8,10):
                        print("#", end="")
                        continue
                    if i in (0,1,11,12):
                        print(" ", end="")
                        continue
                    current = homes[1].get(i-1)
                    print(self.lookup[current] if current else ".", end="")
                if r == self.homedepth + 2:
                    if i in (2,3,4,5,6,7,8,9,10):
                        print("#", end="")
                    else:
                        print(" ", end="")
            print("")

    def check_solved(self, homes):
        for home in homes:
            for hi, hv in home.items():
                if hv != self.mapping[hi]:
                    return False
        return True

    def get_moves_home(self, rests, homes):
        results = []
        for rest_index, rest_value in rests.items():
            if not rest_value:
                continue
            for subindex, sublist in reversed(list(enumerate(homes))):
                for home_index, home in sublist.items():
                    if home:
                        continue
                    if self.mapping[home_index] != rest_value:
                        continue

                    beneath_not_good = False
                    for under in range(subindex+1, self.homedepth):
                        if homes[under][home_index] != rest_value:
                            beneath_not_good = True

                    if beneath_not_good:
                        continue

                    if not self.path_is_clear(home_index, subindex, rest_index, homes, rests):
                        continue

                    self.debug and print(f"Valid path to {subindex}! {rest_index=} to {home_index=}")
                    cost = (self.moves[(home_index, rest_index)] + subindex) * rest_value
                    results.append((cost, home_index, subindex, rest_index))
        return results

    def get_moves_rest(self, rests, homes):
        results = []
        for subindex, sublist in reversed(list(enumerate(homes))):
            for home_index, home in sublist.items():
                if not home:
                    continue
                if self.mapping[home_index] == home:
                    if all(homes[under][home_index] == home for under in range(subindex+1, self.homedepth)):
                        continue
                for rest_index, rest in rests.items():
                    if rest:
                        continue
                    if not self.path_is_clear(home_index, subindex, rest_index, homes, rests):
                        continue
                    self.debug and print(f"Valid path from {subindex} row to rest! {home_index=} to {rest_index=}")
                    cost = (self.moves[(home_index, rest_index)] + subindex) * home
                    results.append((cost, home_index, subindex, rest_index))
                
        return results





a = Amphipod(sample)
a = Amphipod(real)
a = Amphipod(sample, insert=True)
a = Amphipod(real, insert=True)
