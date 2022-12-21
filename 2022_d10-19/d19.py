import re

import numpy as np
from functools import cache

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

        self.ore_max = self.clay_cost_ore + self.ore_cost_ore + self.geo_cost_ore
        self.clay_max = self.obs_cost_clay
        self.obs_max = self.geo_cost_obs

        self.limit = 24
        self.args = (
            index,
            ore_cost_ore,
            clay_cost_ore,
            obs_cost_ore,
            obs_cost_clay,
            geo_cost_ore,
            geo_cost_obs,
        )
        self.hash = hash(self.args)
        self.best_geo = 0

    @cache
    def recurse(
        self,
        minute,
        ore,
        oreR,
        clay,
        clayR,
        obs,
        obsR,
        geos,
        geosR,
    ):
        pad = minute * " "
        self.debug and print(
            pad
            + f"{minute=} {ore=} {oreR=} {clay=} {clayR=} {obs=} {obsR=} {geos=} {geosR=}"
        )
        if minute >= self.limit:
            self.best_geo = max((geos, self.best_geo))
            return

        if ore >= self.geo_cost_ore and obs >= self.geo_cost_obs:
            self.recurse(
                minute,
                ore - self.geo_cost_ore,
                oreR,
                clay,
                clayR,
                obs - self.geo_cost_obs,
                obsR,
                geos,
                geosR + 1,
            )
        if (
            ore >= self.obs_cost_ore
            and clay >= self.obs_cost_clay
            and obs < self.obs_max
        ):
            self.recurse(
                minute,
                ore - self.obs_cost_ore,
                oreR,
                clay - self.obs_cost_clay,
                clayR,
                obs,
                obsR + 1,
                geos,
                geosR,
            )
        if ore >= self.ore_cost_ore and ore < self.ore_max:
            self.recurse(
                minute,
                ore - self.ore_cost_ore,
                oreR + 1,
                clay,
                clayR,
                obs,
                obsR,
                geos,
                geosR,
            )
        if ore >= self.clay_cost_ore and clay < self.clay_max:
            self.recurse(
                minute,
                ore - self.clay_cost_ore,
                oreR,
                clay,
                clayR + 1,
                obs,
                obsR,
                geos,
                geosR,
            )
        ore += oreR
        clay += clayR
        obs += obsR
        geos += geosR
        minute += 1
        self.recurse(
            minute,
            ore,
            oreR,
            clay,
            clayR,
            obs,
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


def get_data(text):
    numbers = re.findall(r"\d+", text)
    print(numbers)
    numiter = iter(numbers)
    results = []
    for _ in range(len(numbers) // 7):
        results.append(Blueprint(*[int(next(numiter)) for _ in range(7)]))
    return results


d = get_data(sample)
