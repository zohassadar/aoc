# part 1
data = open('day8input').read().strip().splitlines()

c = 0
v = 0
for d in data:
    c+=len(d)
    v+=len(eval(d))

print(c-v)

data = open('day8input', 'rb').read()

v2 = 0
i = 0
while True:
    if i == len(data):
        break
    if data[i] == 0x0a:
        i+=1
        continue
    if tuple(data[i:i+2]) == (0x5c,0x22):
        i+=2
        v2+=4
    elif tuple(data[i:i+2]) == (0x5c, 0x78):
        i+=4
        v2+=5
    elif tuple(data[i:i+2]) == (0x5c, 0x5c):
        i+=2
        v2+=4
    elif data[i] == 0x22:
        i+=1
        v2+=3
    else:
        i+=1
        v2+=1

print(v2-c)
