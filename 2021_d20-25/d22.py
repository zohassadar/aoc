
#come back to this later, clean up, try again.

import re
from pprint import pp
from functools import lru_cache
from itertools import chain

LIMIT = 105
DEBUG = False 

sample = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

bigger_sample = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
"""
"""
 

4..4
7..7

4..4
8..9

5..6
7..7

5..6
8..9



4..6 5..7 -> 4, 5..6, 7

7..9 8..10 -> 7, 8..9, 10

"""


def get_data(data):
    coords = re.findall(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', data)
    results = []
    for op,x1,x2,y1,y2,z1,z2 in coords:
        op = True if op == "on" else False
        x1,x2,y1,y2,z1,z2 = (int(i) + 51 for i in (x1,x2,y1,y2,z1,z2) if abs(int(i)) <= 50)
        results.append((op,x1,x2,y1,y2,z1,z2))
    return results



def split_1d(a1,a2,b1,b2):
    DEBUG and print(f"({a1},{a2}) and ({b1},{b2})")
    alist = []
    blist = []
    if not (a1 <= b2 and a2 >= b1):
        DEBUG and print(f"({a1},{a2}) and ({b1},{b2}) do not overlap")
        return [(a1,a2)],(None,None),[(b1,b2)]
    overlap_0 = None
    overlap_1 = None
    if a1 < b1:
        alist.append((a1,b1-1))
        overlap_0 = b1
        DEBUG and print(f"{a1=} < {b1=}: adding range ({a1=},{b1-1=}).  Overlap Start: {b1=}")
    elif b1 < a1:
        blist.append((b1,a1-1))
        overlap_0 = a1
        DEBUG and print(f"{b1=} < {a1=}: adding range ({b1=},{a1-1=}).  Overlap Start: {a1=}")
    else:
        overlap_0 = a1
        DEBUG and print(f"{b1=} == {a1=}:  Overlap Start: {a1=}")

    if a2 > b2:
        alist.append((b2+1,a2))
        overlap_1 = b2
        DEBUG and print(f"{a2=} > {b2=}: adding range ({b2+1=},{a2=}).  Overlap End: {b2=}")
    elif b2 > a2:
        blist.append((a2+1,b2))
        overlap_1 = a2
        DEBUG and print(f"{b2=} > {a2=}: adding range ({a2+1=},{b2=}).  Overlap End: {a2=}")
    else:
        overlap_1 = a2
        DEBUG and print(f"{b2=} == {a2=}:  Overlap End: {a2=}")

    alist.append((overlap_0, overlap_1))
    blist.append((overlap_0, overlap_1))
    if not None in (overlap_0, overlap_1):
        alist = sorted(alist)
        blist = sorted(blist)
    result = alist, (overlap_0, overlap_1), blist
    DEBUG and print(f"{result=}")
    return result



def combine_frags(cx, cy, cz, overlap):
    result = []
    for x in cx:
        for y in cy:
            for z in cz:
                # DEBUG and print(f'{x=} {y=} {z=}')
                fragment = tuple(chain(x,y,z))
                if fragment != overlap:
                    result.append(fragment)
    return result



def split_3d(ax1,ax2,ay1,ay2,az1,az2,bx1,bx2,by1,by2,bz1,bz2):
    abefore = get_product([(ax1,ax2,ay1,ay2,az1,az2)])
    bbefore = get_product([(bx1,bx2,by1,by2,bz1,bz2)])
    cxa, cxoverlap, cxb = split_1d(ax1,ax2,bx1,bx2)
    cya, cyoverlap, cyb = split_1d(ay1,ay2,by1,by2)
    cza, czoverlap, czb = split_1d(az1,az2,bz1,bz2)

    overlap = tuple(chain(*(cxoverlap, cyoverlap, czoverlap)))
  
    if None in overlap:
        # print("No overlap: A ",ax1,ax2,ay1,ay2,az1,az2,"B ",bx1,bx2,by1,by2,bz1,bz2,)
        return
    
    overlaptotal = get_product([overlap])
  
    aside = combine_frags(cxa, cya, cza, overlap)
    aafter = get_product(aside)
  
    bside = combine_frags(cxb, cyb, czb, overlap)
    bafter = get_product(bside)
    assert (aafter + overlaptotal) == abefore
    assert (bafter + overlaptotal) == bbefore
    DEBUG and print (f"A: {aside}")
    DEBUG and print (f"Overlap: {overlap}")
    DEBUG and print (f"B: {bside}")
    return aside,overlap,bside




def add_to_ons(ons, a1,a2,b1,b2,c1,c2):
    # bside_before = get_product([(a1,a2,b1,b2,c1,c2)])
    modified = True
    new_ons = set()
    # minimum_total = get_product(ons)
    for on in ons:    
        # before_new_total = get_product(new_ons)
        # aside_before = get_product([on])
        result = split_3d(*on, a1,a2,b1,b2,c1,c2)
        if result is None:
            new_ons.add((a1,a2,b1,b2,c1,c2))
            new_ons.add(on)
            # print(f"Removed {aside_before} and putting it back in.")
            return modified, list(new_ons)
        aside,overlap,bside = result
        DEBUG and print(f"Adding from aside: {aside}")
        new_ons.update(aside)
        new_ons.update([overlap])
        DEBUG and print(f"Adding from aside: {bside}")
        new_ons.update(bside)
        return modified, list(new_ons)
        # new_total = get_product(new_ons)
        # aside_after = get_product(aside)
        # bside_after = get_product(bside)
        # overlap_total = get_product([overlap])
        # try:
        #     assert aside_before == aside_after + overlap_total
        #     assert bside_before == bside_after + overlap_total
        #     assert new_total >= before_new_total
        # except:
        #     print(on, a1,a2,b1,b2,c1,c2)
        #     print(f'{before_new_total=}')
        #     print(f'{aside_before=}')
        #     print(f'{bside_before=}')
        #     print(f'{new_total=}')
        #     print(f'{get_product(aside)=}')
        #     print(f'{get_product(bside)=}')
        #     print(f'{get_product([overlap])=}')
        #     print(f'{aside=}')
        #     print(f'{overlap=}')
        #     print(f'{bside=}')
        #     raise
        # if None not in overlap:
        #     DEBUG and print(f"Adding overlap: {overlap}")
        #     new_ons.add(overlap)
    
    return False, list(new_ons)


def remove_from_ons(ons, a1,a2,b1,b2,c1,c2):
    new_ons = set()
    for on in ons:
        result = split_3d(*on, a1,a2,b1,b2,c1,c2)
        if result is None:
            new_ons.add(on)
            continue
        aside,overlap,bside = result
        DEBUG and print(f"(sub) Adding from aside: {aside}")
        DEBUG and print(f"(sub) Subtracted: {overlap=} {bside=}")
        new_ons.update(aside)
    return list(new_ons)





def get_product(ons):
    total = 0
    for (x1,x2,y1,y2,z1,z2) in ons:
        product = abs(x2 + 1 - x1) * abs(y2 + 1 - y1) * abs(z2  + 1 - z1)
        total += product
        DEBUG and print (f"The product of {x1} {x2} {y1} {y2} {z1} {z2} is {product}")
    return total


def go_through_data(data, limit=True):
    ons = []
    before_len = 0
    for i,(state,a1,a2,b1,b2,c1,c2) in enumerate(data):
        # if limit and not (a1 >= LIMIT * -1 and a2 <= LIMIT):
        #     print("Skipping ", state,a1,a2,b1,b2,c1,c2)
        #     continue
        # if limit and not (b1 >= LIMIT * -1 and b2 <= LIMIT):
        #     print("Skipping ", state,a1,a2,b1,b2,c1,c2)
        #     continue
        # if limit and not (c1 >= -50 and c2 <= 50):
        #     print("Skipping ", state,a1,a2,b1,b2,c1,c2)
        #     continue
        if state and not ons:
            ons.append((a1,a2,b1,b2,c1,c2))
            lights = get_product(ons)
            print(f"ons is new!  there are now {lights} lights on")
            before_len = lights
        elif state:
            modified = True
            while modified:
                modified, ons = add_to_ons(ons, a1,a2,b1,b2,c1,c2)
            lights = get_product(ons)
            print(f"Added stuff to ons!  {lights} lights on.  Used to be {before_len}")
            assert lights >= before_len
            before_len = lights
        elif not state:
            ons = remove_from_ons(ons, a1,a2,b1,b2,c1,c2)
            lights = get_product(ons)
            print(f"Removed stuff from ons!  {lights} lights on.  Used to be {before_len}")
            assert lights <= before_len
            before_len = lights
        DEBUG and input(f"Well?")

    return ons
        
DEBUG = False
data = get_data(bigger_sample)
ons = go_through_data(data)
print(get_product(ons))


