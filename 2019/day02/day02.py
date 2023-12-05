data = open('day02.input').read().strip()

def add_(table,n1,n2,target): 
    table[target]=table[n1]+table[n2]
    return 4

def multiply(table,n1,n2,target): 
    table[target]=table[n1]*table[n2]
    return 4

def halt(*_): 
    return 0

opcodes = {
    1: add_,
    2: multiply,
    99: halt,
}

def crunch(one=0,two=0):
    table = eval(f"[{data}]")
    table[1] = one
    table[2] = two
    ptr = 0
    while True:
        jump = opcodes[table[ptr]](table, *table[ptr+1:ptr+4])
        if not jump:
            break
        ptr+=jump

    return table[0]


print(f"Part 1: {crunch(12,2)}")

target = 19690720
baseline = crunch()
noun_leap = crunch(1) - baseline
verb_leap = crunch(0,1) - baseline

noun_value, remainder = divmod(target - baseline, noun_leap) 
verb_value = remainder // verb_leap

print(f"Part 2: {100*noun_value+verb_value}")


