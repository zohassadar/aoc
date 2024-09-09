from functools import reduce
from collections import OrderedDict
from pprint import pprint
import re

data = open("day15.input").read().strip()

# data="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

elements = data.split(",")


def get_hash(element):
    return reduce(lambda a, b: ((a + ord(b)) * 17) % 256, element, 0)


# part1
print(sum(get_hash(t) for t in elements))


# part2
structure = [OrderedDict() for _ in range(256)]

for element in elements:
    label, value = re.split(r"[-=]", element)
    box_id = get_hash(label)
    if "=" in element:
        structure[box_id].update({label: int(value)})
    else:
        structure[box_id].pop(label, None)

total = 0
for box_id, box in enumerate(structure, start=1):
    total += sum(box_id * i * v for i, v in enumerate(box.values(), start=1))

print(total)
