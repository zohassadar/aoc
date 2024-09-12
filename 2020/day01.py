data = [int(d) for d in open('day01.input').read().strip().splitlines()]




for number in data:
    other = 2020 - number
    if other in data:
        print(other*number)
        break


from itertools import permutations


for number,other in permutations(data, 2):
    otherother = 2020 - (number+other)
    if otherother in data:
        print(otherother*other*number)
        break
