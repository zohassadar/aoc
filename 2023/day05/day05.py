import re
import pprint
debug = True


def main():
    data = open("day05.input").read()
    part2 = Part2(data)
    print(min(part2.results))
    return part2


class Part2:
    def __init__(self, data):
        self.results: list[int] = []
        chunks = data.split("map:")
        self.seed_ranges = list(
            (int(a), int(b))
            for a, b in re.findall(
                r"(\d+)\s(\d+)(?:\s|$)",
                chunks[0],
                re.M,
            )
        )
        self.maps: list[list[tuple[int, int, int]]] = []
        for chunk in chunks[1:]:
            self.maps.append(
                sorted(
                    list(
                        (int(a), int(b), int(c))
                        for a, b, c in re.findall(r"^(\d+) (\d+) (\d+)$", chunk, re.M)
                    ),
                    key=lambda e: e[1],
                ),
            )
        for start, span in self.seed_ranges[:3]:
            self.recurser(start, span)

    def recurser(self, seed, seed_range, depth=0):
        stop = seed + seed_range
        for i,(trans, start, range_) in enumerate(self.maps[depth]):
            xlate_stop = start + range_
            debug and print(
                (depth * "  ")
                + f"{depth}: map#{i} {seed=:08x} {seed+seed_range=:08x} | {trans=:08x} {start=:08x} {range_=:08x} {xlate_stop=:08x}"
            )
            diff = seed - start
            cs = diff >= 0
            if not cs:
                continue
            diff = seed - xlate_stop
            cc = diff < 0
            if not cc:
                continue

            diff = stop - xlate_stop
            cc = diff < 0
            end = stop if cc else xlate_stop
            
            bump = seed - start
            new_span = end - seed
            xlated_start = trans + bump
            debug and print(
                (depth * "  ")
                + f"{depth}: Result! map#{i} {seed=:08x} {end=:08x} {xlated_start=:08x} {bump=:08x} {new_span=:08x} New Seed: {end:08x}"
            )
            seed = end
            if (depth+1 == len(self.maps)) and xlated_start: # why not zero?
                if xlated_start == 1928058:
                    import sys
                    print("xlated_start", file=sys.stdout)
                    sys.exit()
                self.results.append(xlated_start)
            elif (depth+1 != len(self.maps)):
                self.recurser(xlated_start, new_span, depth + 1)
            if seed == stop:
                return
        debug and print(
            (depth * "  ")
            + f"{depth}: Fallback! map#{i} {seed=:08x} {stop:08x}"
        )
        if (depth+1 == len(self.maps)) and seed: # why not zero?
            self.results.append(seed)
        elif depth+1 != len(self.maps):
            self.recurser(seed, stop, depth + 1)


if __name__ == "__main__":
    part2 = main()

