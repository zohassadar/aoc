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
