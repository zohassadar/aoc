import re

sample = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

real = open('d18.input').read()

def get_data(input_):
    numbers = re.findall('(\d+),(\d+),(\d+)', input_)
    numbers = [(int(a),int(b),int(c)) for a,b,c in numbers]
    return numbers


def get_answer(input_):
    total = 0
    examined = []
    data = get_data(input_)
    for x,y,z in data:
        total += 6
        for xe,ye,ze in examined:
            if (x,y,z) == (xe,ye,ze):
                continue
            if x == xe and y == ye and abs(z - ze) == 1:
                total -= 2
            if z == ze and y == ye and abs(x - xe) == 1:
                total -= 2
            if x == xe and z == ze and abs(y - ye) == 1:
                total -= 2
        examined.append((x,y,z))
    print (total)
 
get_answer(sample) 
get_answer(real)
  
