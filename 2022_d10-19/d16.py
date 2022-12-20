import re
from sys import maxsize
from collections import defaultdict
from queue import PriorityQueue
from operator import itemgetter
from functools import lru_cache
from pprint import pp
from time import perf_counter
from itertools import combinations

second = itemgetter(1)
first = itemgetter(0)

VALVE = "Valve"
PASSTHRU = "Passthru"
vn = lambda nid: (VALVE, nid)
on = lambda nid: (PASSTHRU, nid)
PATTERN = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)').match

sample = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

real = open('d16.input').read()

def print_this(depth, valve, history):
    running_history = [on("AA"), on("DD")]
    if len(history) == len(running_history) and history == running_history:
        return True

    ondeck = on('BB')
    running_history.append(ondeck)
    if len(history) == len(running_history) and history == running_history:
        return True

    ondeck = on('JJ')
    running_history.append(ondeck)
    if len(history) == len(running_history) and history == running_history:
        return True

    ondeck = on('HH')
    running_history.append(ondeck)
    if len(history) == len(running_history) and history == running_history:
        return True

    ondeck = on('EE')
    running_history.append(ondeck)
    if len(history) == len(running_history) and history == running_history:
        return True

    ondeck = on('CC')
    running_history.append(ondeck)
    if len(history) == len(running_history) and history == running_history:
        return True





def get_data(input_):
    max_rate = 0
    first_pass = {}
    for line in input_.splitlines():
        line = line.strip()
        if not line:
            continue
        data = PATTERN(line)
        if not data:
            raise Exception (f"Something went wrong with {line}")
        valve, rate, neighbors = data.groups()
        neighbors = neighbors.split(", ")
        rate = int(rate)
        max_rate = max((rate, max_rate))
        first_pass[valve] = (rate, neighbors)

    result = {}
    rates = {}
    for tunnel, (rate, neighbors) in first_pass.items():
        new_neighbors = {on(n): 1 for n in neighbors}
        if rate:
            rates[vn(tunnel)] = rate
            new_rate = max_rate - rate + 1
            new_neighbors.update({vn(tunnel): new_rate})
        result[on(tunnel)] = new_neighbors
    return rates, result



class PathFinder:
    def __init__(self, input_, debug=False, round_two=False, round_two_a=False):
        self.debug = debug
        self.rates, self.tunnels = get_data(input_)
        self.ons = tuple((k, False) for k in self.rates)
        self.knowns = {}
        self.hash = hash(str(self.tunnels))
        self.best_score = 0
        self.best_scores = set()
        self.best_halfway = 0
        self.cache_hits = 0
        then = perf_counter()
        self.visited = []
        if round_two:
            self.recurse_two(on("AA"), on("AA"), self.ons)
        elif round_two_a:
            # all_valves = []
            # for neighbors in self.tunnels.values():
            #     all_valves.extend([second(n) for n in neighbors if first(n) is VALVE])
            self.recurse(on("AA"), self.ons, remaining=26)
        else:
            self.recurse(on("AA"), self.ons)
        print(self.best_score, perf_counter() - then)

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash

    def get_todo(self):
        while True:
            if not self.todo.empty():
                ondeck = self.todo.get()
                yield second(ondeck)
            else:
                break

    @lru_cache(maxsize=None)
    def get_best_valves(self, tunnel, ons_tuple, remaining):
        ons = dict(ons_tuple)
        self.crawl_from_position(tunnel)
        valves = [(v,k) for k,v in self.knowns[tunnel].items() if k[0] is VALVE]
        valves.sort()
        if not valves:
            return
        results = []
        for neighbor, _  in ((k,v) for v,k in valves if not ons.get(k, True)):
            ntype, nid = neighbor
            rate = self.rates[neighbor]
            cost_to_neighbor = self.get_cost(tunnel, on(nid)) + 1
            score = (remaining - cost_to_neighbor) * rate
            if score < 1:
                continue
            # print(f"Evaluating: {neighbor=} {remaining=} {cost_to_neighbor=} {rate=} {score=}")
            results.append((score, cost_to_neighbor, neighbor))
        results.sort(reverse=True)
        return results

    def recurse(self, position, ons_tuple, history=None, total=0, remaining=30, depth=0):
        ons = dict(ons_tuple)
        if history is None:
            history = []
        pad = " " * depth
        depth += 1
        recursed = False
        best_scores = self.get_best_valves(position, tuple(ons.items()), remaining)

        for score, cost, (vtype, vid) in best_scores:
            new_start = on(vid)
            new_total = score + total
            new_remaining = remaining - cost
            new_ons = ons.copy()
            new_ons[(vtype, vid)] = True
            new_ons = tuple(new_ons.items())
            recursed = True
            new_history = history.copy()
            new_history.append(new_start)
            if self.debug and print_this(depth, new_start, new_history):
                print(pad + f"{score=}, {cost=} {remaining=}")
                print (pad + f'Starting from {new_start} with {new_remaining} left and a total of {new_total}')
            self.recurse(new_start, new_ons, new_history, new_total, new_remaining, depth)

        if not recursed:
            # print (pad + f'Hit an end! setting new score {total}')
            history = tuple(sorted(history))
            self.best_scores.add((total, history))
            self.best_score = max((total, self.best_score))
        
    @lru_cache(maxsize=None)
    def recurse_two(self, p1, p2, ons_tuple, total=0, r1=26, r2=26):
        ons = dict(ons_tuple)
        recursed = False
        best_scores1 = self.get_best_valves(p1, ons_tuple, r1)
        if not best_scores1:
            best_scores1 = [(0, 0, p1)]

        best_scores2 = self.get_best_valves(p2, ons_tuple, r2)
        if not best_scores2:
            best_scores2 = [(0, 0, p2)]

        for score1, cost1, (vtype1, vid1) in best_scores1:
            for score2, cost2, (vtype2, vid2) in best_scores2:
                if not score1 and not score2:
                    continue
                if (vtype1, vid1) == (vtype2, vid2):
                    continue
                new_start1 = on(vid1)        
                new_start2 = on(vid2)
                new_total = score1 + score2 + total
                new_r1 = r1 - cost1
                new_r2 = r2 - cost2
                (new_r1, new_start1), (new_r2, new_start2) = sorted([(new_r1, new_start1), (new_r2, new_start2)])
                new_ons = ons.copy()
                new_ons[(vtype1, vid1)] = True
                new_ons[(vtype2, vid2)] = True
                new_ons = tuple(new_ons.items())
                recursed = True
                self.debug and print(f"{score1=}, {cost1=} {new_r1=} {new_r2=}")
                self.debug and print (f'Starting from {new_start1=} and {new_start2=} with {new_r1=} {new_r2=} left and a total of {new_total}')
                self.recurse_two(new_start1, new_start2, new_ons, new_total, new_r1, new_r2)

        if not recursed:
            self.debug and print (f'Hit an end! setting new score {total}')
            self.best_score = max((total, self.best_score))

    @lru_cache(maxsize=None)
    def get_cost(self, start, end):
        self.crawl_from_position(end)
        return self.knowns[end][start]

    def crawl_from_position(self, start):
        if self.knowns.get(start):
            self.cache_hits += 1
            return
        knowns = defaultdict(lambda: maxsize)
        knowns[start] = 0
        self.todo = PriorityQueue()
        self.todo.put((0, start))
        self.been_there = set()
        
        for todo in self.get_todo():
            if todo in self.been_there:
                continue
            self.been_there.add(todo)
            my_cost = knowns[todo]
            self.debug and print(f'Regarding {todo}.  Known cost is {my_cost}')
            neighbors = self.tunnels.get(todo, {})
            for neighbor, cost in neighbors.items():
                known_cost = knowns[neighbor]
                new_cost = cost + my_cost
                if new_cost < known_cost:
                    self.debug and print (f"IMPROVED! {neighbor} {known_cost} with {new_cost}")
                    knowns[neighbor] = new_cost
                    self.todo.put((new_cost, neighbor))
                else: 
                    self.debug and print (f"ALREADY GOOD! {neighbor} {known_cost} is better than {new_cost}")
        self.knowns[start] = knowns


a = PathFinder(sample, debug=False)
a = PathFinder(real, debug=False)
a = PathFinder(sample, debug=False, round_two=True)
then = perf_counter()
a = PathFinder(real, debug=False, round_two_a=True)

best_score = 0

from itertools import combinations

for (s1, hist1),(s2, hist2) in combinations(sorted(a.best_scores, reverse=True), 2):
    new_score = s1 + s2
    if new_score < best_score:
        continue
    for hist in hist1:
        if hist in hist2:
            break
    else:
        best_score = max((best_score,new_score))
        
print(best_score)
print(perf_counter() - then)

