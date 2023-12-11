import re
from functools import reduce

from snek_advent import validate

written_out = {
    1: ["one", "1", "one"[::-1]],
    2: ["two", "2", "two"[::-1]],
    3: ["three", "3", "three"[::-1]],
    4: ["four", "4", "four"[::-1]],
    5: ["five", "5", "five"[::-1]],
    6: ["six", "6", "six"[::-1]],
    7: ["seven", "7", "seven"[::-1]],
    8: ["eight", "8", "eight"[::-1]],
    9: ["nine", "9", "nine"[::-1]],
}

compiled_regex = re.compile(r"\d")


def part01(lines):
    value = reduce(
        (lambda p, n: p + int(f"{n[0]}{n[-1]}")),
        map((lambda x: compiled_regex.findall(x)), lines),
        0,
    )
    validate(54597, value)


def part02_parse_line(line, reversed_line):
    first_number_found, last_number_found, first_item_index, last_item_index = (
        -1,
        -1,
        10_000,
        10_000,
    )

    for wo in written_out:
        for val in written_out[wo][0:2]:
            ff_index = line.index(val) if val in line else -1
            if ff_index != -1 and ff_index < first_item_index:
                first_item_index = ff_index
                first_number_found = wo

        for val in written_out[wo][1:]:
            fl_index = reversed_line.index(val) if val in reversed_line else -1
            if fl_index != -1 and fl_index < last_item_index:
                last_item_index = fl_index
                last_number_found = wo

    return last_number_found + (10 * first_number_found)


def part02(lines):
    value = reduce(
        lambda x, y: x + y, map(lambda l: part02_parse_line(l, l[::-1]), lines)
    )
    validate(54504, value)
