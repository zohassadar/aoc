data = [int(d) for d in open('day01.input').read().strip().splitlines()]




for number in data:
    other = 2020 - number
    if other in data:
        print(other*number)
        break
