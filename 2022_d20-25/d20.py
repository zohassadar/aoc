import re
DEBUG = True

key = 811589153

sample = """
1
2
-3
3
-2
0
4
"""
real = open("d20.input").read()

def get_data(input_):
    numbers = re.findall(r'-?\d+', input_)
    return [(i,int(n)) for i,n in enumerate(numbers)]


def get_sum(input_, mix=1):
    data = get_data(input_)
    if mix > 1:
        data = [(i, d * key) for i,d in data]
    copy = data.copy()
    depth = len(data)
    depth_m1 = depth - 1
    zero_stamp = 0
    for _ in range(mix):
        for d in copy:
            DEBUG and print([d[1] for d in data])
            number = d[1]
            if not number:
                zero_stamp = d
            index = data.index(d)
            _, moves = data.pop(index)
            index = index + moves
            index = index % depth_m1
            if index == 0:
                index = depth_m1
            data.insert(index, d)
            DEBUG and print(f'{d[0]=} {number=} {index=} {moves=}')
    zeroindex = data.index(zero_stamp)
    DEBUG and print([d[1] for d in data])
    num1 = data[(1000+zeroindex)%depth][1]
    num2 = data[(2000+zeroindex)%depth][1]
    num3 = data[(3000+zeroindex)%depth][1]
    DEBUG and print(zero_stamp)
    print(sum([num1, num2, num3]))


DEBUG = False
get_sum(sample)
get_sum(real)
get_sum(sample, 10)
get_sum(real, 10)


