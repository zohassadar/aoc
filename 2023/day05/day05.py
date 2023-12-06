import re
import pprint

debug = False


def main():
    data = open("day05.input").read()
    part2 = Part2(data)
    debug and pprint.pprint(part2.seed_ranges)
    debug and pprint.pprint(part2.maps)
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

    def recurser(self, start, span, depth=0):
        debug and print((depth * "  ") + f"{depth}: Entering recurser with {start=} {span=}")
        stop = start + span
        for xlate, xlate_start, xlate_span in self.maps[depth]:
            debug and print(
                (depth * "  ")
                + f"{depth}: Comparing against {xlate=} {xlate_start=} {xlate_span=}"
            )
            xlate_stop = xlate_start + xlate_span
            if start >= xlate_start and start < xlate_stop:
                end = stop if stop < xlate_stop else xlate_stop
                offset = start - xlate_start
                new_span = end - start
                xlated_start = xlate + offset
                xlated_end = xlate + offset + new_span
                debug and print(
                    (depth * "  ")
                    + f"{depth}: Result! {start=} {end=} {xlated_start=} {xlated_end=} New: {end=}"
                )
                start = end
                if (depth+1 == len(self.maps)) and xlated_start: # why not zero?
                    self.results.append(xlated_start)
                elif (depth+1 != len(self.maps)):
                    self.recurser(xlated_start, xlated_end, depth + 1)
                if start == stop:
                    break
        if start == stop:
            return
        if (depth+1 == len(self.maps)) and start: # why not zero?
            self.results.append(start)
        elif depth+1 != len(self.maps):
            self.recurser(start, stop, depth + 1)


if __name__ == "__main__":
    part2 = main()
