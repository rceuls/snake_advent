import re
from functools import cache

from snek_advent import validate

spring_regex = re.compile(r"#*")


@cache
def check_springs(line, springs, result=0):
    if springs == ():
        return "#" not in line
    current, remaining_springs = springs[0], springs[1:]
    for i in range(
        len(line) - sum(remaining_springs) - len(remaining_springs) - current + 1
    ):
        if "#" in line[:i]:
            break
        if (
            (nxt := i + current) <= len(line)
            and "." not in line[i:nxt]
            and line[nxt : nxt + 1] != "#"
        ):
            result += check_springs(line[nxt + 1 :], remaining_springs)
    return result


def part01(lines: list[str]):
    total = 0
    for line in [line.split() for line in lines]:
        check = check_springs(line[0], tuple(map(int, line[1].split(","))))
        total += check
    validate(total, 6935)


def part02(lines: list[str]):
    total = 0
    for line in [line.split() for line in lines]:
        check = check_springs(
            "?".join([line[0]] * 5), tuple(5 * list(map(int, line[1].split(","))))
        )
        total += check
    validate(total, 3920437278260)
