# part 1
data = open('day8input').read().strip().splitlines()

c = 0
v = 0
for d in data:
    c+=len(d)
    v+=len(eval(d))

print(c-v)
