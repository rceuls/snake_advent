from functools import cache, reduce
from itertools import count
from multiprocessing import Pool
import re
from snek_advent import validate

DAMAGED = "#"
OPERATIONAL = "."
UNKNOWN = "?"

spring_regex = re.compile(r"#*")
damaged_regex = re.compile(r"#+")


@cache
def variation(line: str, index: int):
    variations = set()
    if index >= len(line):
        variations.add(line)
        return variations
    if line[index] == "?":
        variations = variations.union(
            variation(line[:index] + "#" + line[index + 1 :], index + 1)
        )
        variations = variations.union(
            variation(line[:index] + "." + line[index + 1 :], index + 1)
        )
    else:
        variations.add(line)
        variations = variations.union(variation(line, index + 1))
    return variations


def calc_line_hit_count(line: str):
    hits = 0
    (spirals, groups) = line.split(" ")
    groups_parsed = [int(x) for x in groups.split(",")]
    variations_on_a_theme = [
        x for x in list(variation(spirals, 0)) if x.count("?") == 0
    ]
    for var in variations_on_a_theme:
        splitted = [len(x) for x in spring_regex.findall(var) if x != ""]
        if splitted == groups_parsed:
            hits += 1
    return hits


def calc_line_hit_count_v2(line: str):
    hits = 0
    (spirals, groups) = line.split(" ")
    groups_parsed = [int(x) for x in groups.split(",")]
    spirals = spirals + "?" + spirals + "?" + spirals + "?" + spirals + "?" + spirals
    variations_on_a_theme = [
        x for x in list(variation(spirals, 0)) if x.count("?") == 0
    ]
    for var in variations_on_a_theme:
        splitted = [len(x) for x in spring_regex.findall(var) if x != ""]
        if splitted == groups_parsed:
            hits += 1
    return hits


def part01(lines: list[str]):
    return 0
    with Pool() as p:
        hits = reduce(lambda x, y: x + y, p.map(calc_line_hit_count, lines))
        validate(hits, 6935)


def part02(lines: list[str]):
    with Pool() as p:
        hits = reduce(lambda x, y: x + y, p.map(calc_line_hit_count_v2, lines))
        validate(hits, 6935)
