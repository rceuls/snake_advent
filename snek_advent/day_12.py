import re
from functools import cache

from snek_advent import validate

spring_regex = re.compile(r"#*")


@cache
def check_springs(line, springs, result=0):
    if not springs:
        return "#" not in line
    current, springs = springs[0], springs[1:]
    for i in range(len(line) - sum(springs) - len(springs) - current + 1):
        if "#" in line[:i]:
            break
        if (
            (nxt := i + current) <= len(line)
            and "." not in line[i:nxt]
            and line[nxt : nxt + 1] != "#"
        ):
            result += check_springs(line[nxt + 1 :], springs)
    return result


def part01(lines: list[str]):
    total = 0
    for line in [line.split() for line in lines]:
        check = check_springs(line[0], (springs := tuple(map(int, line[1].split(",")))))
        total += check
    validate(total, 6935)


def part02(lines: list[str]):
    total = 0
    for line in [line.split() for line in lines]:
        check = check_springs(
            "?".join([line[0]] * 5),
            (springs := tuple(5 * list(map(int, line[1].split(","))))),
        )
        total += check
    validate(total, 6935)
