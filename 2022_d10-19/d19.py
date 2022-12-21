import re
from functools import cache
from math import prod
from time import perf_counter

import numpy as np

sample = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian."""

real = open("d19.input").read()


class Blueprint:
    def __init__(
        self,
        index,
        ore_cost_ore,
        clay_cost_ore,
        obs_cost_ore,
        obs_cost_clay,
        geo_cost_ore,
        geo_cost_obs,
        limit,
        debug=False,
    ):
        self.index = index
        self.debug = debug
        self.ore_cost_ore = ore_cost_ore

        self.clay_cost_ore = clay_cost_ore

        self.obs_cost_ore = obs_cost_ore
        self.obs_cost_clay = obs_cost_clay

        self.geo_cost_ore = geo_cost_ore
        self.geo_cost_obs = geo_cost_obs

        self.ore_max = sum(
            (
                self.clay_cost_ore,
                self.ore_cost_ore,
                self.geo_cost_ore,
                self.obs_cost_ore,
            )
        )

        self.limit = limit
        self.args = (
            index,
            ore_cost_ore,
            clay_cost_ore,
            obs_cost_ore,
            obs_cost_clay,
            geo_cost_ore,
            geo_cost_obs,
            limit,
        )
        self.hash = hash(self.args)
        self.best_geo = 0

    @cache
    def best_case(self, minute):
        return sum(range(1, (self.limit - minute) + 3))

    @cache
    def recurse(
        self,
        minute=1,
        ore=0,
        oreR=1,
        clay=0,
        clayR=0,
        obs=0,
        obsR=0,
        geos=0,
        geosR=0,
    ):

        pad = minute * " "
        self.debug and print(
            pad
            + f"{minute=} {ore=} {oreR=} {clay=} {clayR=} {obs=} {obsR=} {geos=} {geosR=}"
        )
        if minute > self.limit:
            self.debug and print(pad + f"Giving up at minute {minute} with {geos}")
            self.best_geo = max((geos, self.best_geo))
            if geos == self.best_geo:
                self.debug and print(
                    pad
                    + f"{minute=} {ore=} {oreR=} {clay=} {clayR=} {obs=} {obsR=} {geos=} {geosR=}"
                )
            return
        remaining = self.limit - minute + 2
        best_case = geos + (remaining * (remaining + 1) // 2)
        if best_case <= self.best_geo:
            self.debug and print(
                pad
                + f"Giving up at minute {minute} because {best_case} <= {self.best_geo}"
            )
            return

        ore += oreR
        clay += clayR
        obs += obsR
        geos += geosR

        minute += 1
        if obsR and ore >= self.geo_cost_ore and obs >= self.geo_cost_obs:
            self.recurse(
                minute,
                min((ore - self.geo_cost_ore, self.ore_max)),
                oreR,
                min((clay, self.obs_cost_clay)),
                clayR,
                min((obs - self.geo_cost_obs, self.geo_cost_obs)),
                obsR,
                geos - 1,
                geosR + 1,
            )

        if (
            ore >= self.obs_cost_ore
            and clay >= self.obs_cost_clay
            and obs < self.geo_cost_obs
        ):
            self.recurse(
                minute,
                min((ore - self.obs_cost_ore, self.ore_max)),
                oreR,
                min((clay - self.obs_cost_clay, self.obs_cost_clay)),
                clayR,
                min((obs - 1, self.geo_cost_obs)),
                obsR + 1,
                geos,
                geosR,
            )

        if ore >= self.clay_cost_ore and clay < self.obs_cost_clay:
            self.recurse(
                minute,
                min((ore - self.clay_cost_ore, self.ore_max)),
                oreR,
                min((clay - 1, self.obs_cost_clay)),
                clayR + 1,
                min((obs, self.geo_cost_obs)),
                obsR,
                geos,
                geosR,
            )

        if ore >= self.ore_cost_ore and ore < self.ore_max:
            self.recurse(
                minute,
                min((ore - self.ore_cost_ore - 1, self.ore_max)),
                oreR + 1,
                min((clay, self.obs_cost_clay)),
                clayR,
                min((obs, self.geo_cost_obs)),
                obsR,
                geos,
                geosR,
            )

        self.recurse(
            minute,
            min((ore, self.ore_max)),
            oreR,
            min((clay, self.obs_cost_clay)),
            clayR,
            min((obs, self.geo_cost_obs)),
            obsR,
            geos,
            geosR,
        )

    def __str__(self):
        return (
            f"Blueprint {self.index}:\n"
            f"  Each ore robot costs {self.ore_cost_ore} ore.\n"
            f"  Each clay robot costs {self.clay_cost_ore} ore.\n"
            f"  Each obsidian robot costs {self.obs_cost_ore} ore and {self.obs_cost_clay} clay.\n"
            f"  Each geode robot costs {self.geo_cost_ore} ore and {self.geo_cost_obs} obsidian.\n"
        )

    def __repr__(self):
        return f"{type(self).__name__}({','.join(map(str,self.args))})"

    def __eq__(self, a):
        return self.args == a.args

    def __hash__(self):
        return self.hash


def get_data(text, limit):
    numbers = re.findall(r"\d+", text)
    numiter = iter(numbers)
    results = []
    for _ in range(len(numbers) // 7):
        results.append(Blueprint(*[int(next(numiter)) for _ in range(7)], limit))
    return results


def print_answer(text, limit=24, debug=False):
    then = perf_counter()
    data = get_data(text, limit=limit)
    if limit != 24:
        data = data[:3]
    for d in data:
        d.recurse()
    for d in data:
        debug and print(f"{d.index=} {d.best_geo}")
    if limit == 24:
        print(sum(d.index * d.best_geo for d in data), end=" ")
    else:
        print(prod(d.best_geo for d in data), end=" ")

    print(perf_counter() - then)


print_answer(sample)
print_answer(real)
