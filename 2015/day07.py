import re
data = open('day7input').read().strip().splitlines()

def extract(line):
    result = re.search(r'([a-z0-9]+)?\s?(?:(NOT|AND|OR|LSHIFT|RSHIFT) ([a-z0-9]+))? -> ([a-z]+)', line)
    n1, op, n2, target = result.groups()
    table[target] = n1,op,n2

table = {}
for d in data:
    extract(d)

def resolve(element):
    if (r := resolved.get(element)) is not None:
        return r

    if isinstance(element, str) and element.isdigit():
        resolved[element] = int(element)
        return int(element)

    def _not():
        result = ~resolve(d[2])
        return 0x10000 + result if result < 0 else result

    def _and():
        return resolve(d[0]) & resolve(d[2])

    def _or():
        return resolve(d[0]) | resolve(d[2])

    def _lshift():
        return resolve(d[0]) << resolve(d[2])

    def _rshift():
        return resolve(d[0]) >> resolve(d[2])

    ops = {
        "NOT": _not,
        "AND": _and,
        "OR": _or,
        "LSHIFT": _lshift,
        "RSHIFT": _rshift,
        }

    d = table[element]
    if d[1] in ops:
        result = ops[d[1]]()
        resolved[element] = result
        return result
    if d[0].isdigit():
        return int(d[0])
    else:
        return resolve(d[0])



resolved = {}
day1 = resolve('a')
print(day1)

table['b'] = (str(day1), None, None)
resolved = {}
day2 = resolve('a')
print(day2)
