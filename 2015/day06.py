import numpy as np
import re

data = open('day06.input').read().strip().splitlines()

grid = np.zeros((1000,1000),dtype=np.uint8)

for line in data:
    a,b,x,y = (int(d) for d in re.findall(r'\d+', line))
    subgrid = grid[a:x+1,b:y+1]
    if 'off' in line:
        subgrid[:] = 0
    elif 'on' in line:
        subgrid[:] = 1
    elif 'toggle' in line:
        subgrid[:] ^= 1



print(np.count_nonzero(grid))


grid = np.zeros((1000,1000),dtype=np.int16)

for line in data:
    a,b,x,y = (int(d) for d in re.findall(r'\d+', line))
    subgrid = grid[a:x+1,b:y+1]
    if 'off' in line:
        subgrid[:] -= 1
        subgrid[subgrid<0] = 0
    elif 'on' in line:
        subgrid[:] += 1
    elif 'toggle' in line:
        subgrid[:] += 2

print(np.sum(grid))
