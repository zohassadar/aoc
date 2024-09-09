import re
from functools import reduce

data = open("day09.input").readlines()

# data = """
# 0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# """.strip().splitlines()


def get_numbers(line):
    return list(int(d) for d in re.findall(r"[-\d]+", line))


def dwindle(numbers, lists=None):
    parent = False
    if lists is None:
        parent = True
        lists = [numbers]
    new_list = [numbers[i + 1] - n for i, n in enumerate(numbers[: len(numbers) - 1])]
    if any(new_list):
        lists.append(new_list)
        dwindle(new_list, lists)
    if parent:
        part1 = sum(l[-1] for l in lists)
        part2 = reduce(lambda x,y: y-x, (l[0] for l in reversed(lists)), 0)
        return part1,part2


print(sum(dwindle(get_numbers(line))[0] for line in data))
print(sum(dwindle(get_numbers(line))[1] for line in data))
