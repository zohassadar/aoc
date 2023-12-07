import re
import pprint

debug = False


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
        for trans, start, range_ in self.maps[depth]:
            xlate_stop = start + range_
            debug and print(
                (depth * "  ")
                + f"{depth}: {seed=:04x} {stop=:04x} {trans=:04x} {start=:04x} {range_=:04x}"
            )
            if not (seed >= start and seed < xlate_stop):
                continue
            end = stop if stop < xlate_stop else xlate_stop
            bump = seed - start
            new_span = end - seed
            xlated_start = trans + bump
            xlated_end = trans + bump + new_span
            debug and print(
                (depth * "  ")
                + f"{depth}: Result! {seed=:04x} {end=:04x} {xlated_start=:04x} {xlated_end=:04x} New: {end=:04x}"
            )
            seed = end
            if (depth+1 == len(self.maps)) and xlated_start: # why not zero?
                self.results.append(xlated_start)
            elif (depth+1 != len(self.maps)):
                self.recurser(xlated_start, xlated_end, depth + 1)
            if seed == stop:
                return
        if (depth+1 == len(self.maps)) and seed: # why not zero?
            self.results.append(seed)
        elif depth+1 != len(self.maps):
            self.recurser(seed, stop, depth + 1)


if __name__ == "__main__":
    part2 = main()

