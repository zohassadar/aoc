import re

data = open('day05.input').read().strip().splitlines()

def vowel_test(string):
    return len(re.findall(r'[aeiou]', string)) >= 3
def repeat_test(string):
    return bool(re.search(r'(.)\1', string))
def forbidden_test(string):
    if 'ab' in string:
        return False
    if 'cd' in string:
        return False
    if 'pq' in string:
        return False
    if 'xy' in string:
        return False
    return True

def passes_all(string):
    return vowel_test(string) and repeat_test(string) and forbidden_test(string)

i=0
for string in data:
    if passes_all(string):
        i+=1

print(i)




def double_test(string):
    return bool(re.search(r'(..).*\1', string))


def repeat_test(string):
    return bool(re.search(r'(.).\1', string))

def passes_all(string):
    return double_test(string) and repeat_test(string)

i = 0
for string in data:
    if passes_all(string):
        i+=1
print(i)
