import re
from operator import mul, floordiv, sub, add, eq

ROOT = "root"
HUMAN = "humn"

sample = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

real = open("d21.input").read()


def get_data(input_):
    op_map = {"*": mul, "/": floordiv, "+": add, "-": sub}
    results = {}
    data = re.findall(r"([a-z]{4}): (?:([a-z]{4}) ([*+-/]) ([a-z]{4})|(\d+))", input_)
    for id, m1, op, m2, number in data:
        results[id] = (
            m1,
            op_map[op] if op else None,
            m2,
            int(number) if number else None,
        )
    return results


def recurse_this(data, monkey):
    m1, op, m2, number = data[monkey]
    if number:
        return number
    return op(recurse_this(data, m1), recurse_this(data, m2))


def get_number(input_):
    data = get_data(input_)
    return recurse_this(data, ROOT)


def human_check(data, monkey):
    if monkey == HUMAN:
        return True
    m1, op, m2, number = data[monkey]
    if number:
        return
    if m1 == HUMAN or m2 == HUMAN:
        return True
    if human_check(data, m1):
        return True
    if human_check(data, m2):
        return True


def get_eq(_, b):
    return b


def rev_div(a, b):
    return b // a


def rev_sub(a, b):
    return b - a


def get_my_number(input_):
    data = get_data(input_)
    l_map = {
        mul: floordiv,
        floordiv: mul,
        sub: add,
        add: sub,
        eq: get_eq,
    }
    r_map = {
        mul: floordiv,
        floordiv: rev_div,
        sub: rev_sub,
        add: sub,
        eq: get_eq,
    }

    def what_to_do(monkey, target, depth=0):
        pad = depth * " "
        depth += 1
        m1, op, m2, _ = data[monkey]
        if monkey == HUMAN:
            return target
        if monkey == ROOT:
            op = eq
        if human_check(data, m1):
            known, unknown = m2, m1
            known_value = recurse_this(data, known)
            new_target = l_map[op](target, known_value)
        else:
            known, unknown = m1, m2
            known_value = recurse_this(data, known)
            new_target = r_map[op](target, known_value)

        DEBUG and print(
            pad
            + f"Received {monkey} {op} and {target=} with {known_value=} and {new_target=}"
        )
        return what_to_do(unknown, new_target, depth)

    return what_to_do(ROOT, 1)


DEBUG = False
print(get_number(sample))
print(get_number(real))
print(get_my_number(sample))
print(get_my_number(real))
