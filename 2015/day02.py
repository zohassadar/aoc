import re

data = "2x3x4"
data = open('day02.input').read().strip().splitlines()

def get_numbers(line):
    return [int(d) for d in line.split("x")]

def get_area(x,y,z):
    areas = [x*y,x*z,y*z]
    smallest = min(areas)
    return sum(2*d for d in areas) + smallest



total = 0
for line in data:
    total += get_area(*get_numbers(line))
print(total)


def get_ribbon(x,y,z):
    smallest = sum(2*d for d in sorted([x,y,z])[:-1])
    return smallest + (x*y*z)

total2 = 0
for line in data:
    total2 += get_ribbon(*get_numbers(line))
print(total2)
