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
