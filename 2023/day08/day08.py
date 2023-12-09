from itertools import cycle
from math import lcm
from re import findall, M
from functools import reduce

s = open("day08.input").read()

t, b = s.split("\n", 1)

l = findall(r"\w{3}", b)

q = {k: (w, x) for k, w, x in zip(*([iter(l)] * 3))}

m = {
    "L": lambda e: e[0],
    "R": lambda e: e[1],
}

p = []
for a in findall(r"^..A", s, M):
    o = r = a
    for i, z in enumerate(cycle(m[d] for d in t), 1):
        r = z(q[r])
        if r.endswith("Z"):
            p.append(i)
            print(i) if o == "AAA" else ...
            break

A = reduce(lcm, p)

print(A)
