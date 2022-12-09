#this is a successful failure.  revisit it.  
#it takes too long and player1's score is off by a factor of 27


from itertools import product
from collections import defaultdict,Counter
import time
then = time.perf_counter()

get_new = lambda last, new: ((last + new - 1) % 10) + 1

combos = list( sum(c) for c in product((1,2,3), repeat=3) )

mult = Counter(combos)

jumps = defaultdict(dict)
for i in range(1,11):
    for j in range(3,10):
        jumps[i][j] = get_new(i,j)


all_rolls = list(product(mult.items(), repeat=2))

p1wins = 0
p2wins = 0

winning_depths = defaultdict(int)
mpliers = defaultdict(int)


def get_winners(p1start, p1roll, p1score, p2start, p2roll, p2score, mplier, depth=0):
    if p1score >= 21 or p2score >= 21:
        exit("FUCK")
    depth+=1
    global p1wins, p2wins
    p1new = jumps[p1start][p1roll]
    p1score += p1new
    if p1score >= 21:
        p1wins += mplier
        # mpliers[mplier] += 1
        return
    p2new = jumps[p2start][p2roll]
    p2score += p2new
    if p2score >= 21:
        p2wins += mplier
        # mpliers[mplier] += 1
        return
    for (p1r, p1m), (p2r, p2m) in all_rolls:
        newplier = p1m * p2m
        get_winners(p1new, p1r, p1score, p2new, p2r, p2score, newplier * mplier, depth)
        


p1 = 4
p2 = 1

for (p1roll, p1mult), (p2roll, p2mult) in all_rolls:
    mplier = p1mult * p2mult
    i+=1
    get_winners(p1, p1roll, 0, p2, p2roll, 0, mplier)

print(time.perf_counter() - then)
print(p1wins // 27) # <- come back to this
print(p2wins)

