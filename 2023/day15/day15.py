#part1
data = open('day15.input').read().strip()

print(sum(reduce(lambda a,b:((a+ord(b))*17)%256,t,0) for t in data.split(',')))
