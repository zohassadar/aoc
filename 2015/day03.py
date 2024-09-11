data = "^v^v^v^v^v"
data = open('day03.input').read()
ops = {
    ">": lambda x, y: (x + 1, y),
    "<": lambda x, y: (x - 1, y),
    "^": lambda x, y: (x, y + 1),
    "v": lambda x, y: (x, y - 1),
}


current = 0, 0

houses = {current}

for char in data:
   current = ops[char](*current)
   houses.add(current)

print(len(houses))


current1 = 0,0
houses1 = {current1}
current2 = 0,0
houses2 = {current2}

for char in data[::2]:
    current1 = ops[char](*current1)
    houses1.add(current1)

for char in data[1::2]:
    current2 = ops[char](*current2)
    houses2.add(current2)


print(len(houses1 | houses2))
