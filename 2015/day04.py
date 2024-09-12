import hashlib

i = 1
while True:
    if hashlib.md5(f"yzbqklnj{i}".encode()).hexdigest().startswith('00000'):
        break
    i+=1
print(i)

i = 1
while True:
    if hashlib.md5(f"yzbqklnj{i}".encode()).hexdigest().startswith('000000'):
        break
    if i % 1000000 == 0:
        print(i)
    i+=1
print(i)
