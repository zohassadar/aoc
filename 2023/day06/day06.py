import re
from math import prod

data = open('day06.input').readlines()

# data = """
# Time:      7  15   30
# Distance:  9  40  200
# """.strip().splitlines()

def get_digits(line):
    return list(int(d) for d in re.findall(r'\d+', line))

times = get_digits(data[0])
distances = get_digits(data[1])

totals = []
for time, distance in zip(times,distances):
    total = 0
    for i in range(1,time):
        if (i * (time-i) > distance):
            total+=1
    totals.append(total)

print(prod(totals))
