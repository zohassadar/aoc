from itertools import cycle


data = cycle(eval(d) for d in open('day01.input').read().strip().splitlines())


frequencies = [0]


frequency = 0


while True:
    next_number = next(data)
    frequency = frequency + next_number
    if frequency in frequencies:
        break
    frequencies.append(frequency)


print (frequency)
