import re
from functools import reduce

written_out = {
    "1": ["one", "1"],
    "2": ["two", "2"],
    "3": ["three", "3"],
    "4": ["four", "4"],
    "5": ["five", "5"],
    "6": ["six", "6"],
    "7": ["seven", "7"],
    "8": ["eight", "8"],
    "9": ["nine", "9"],
}

written_out_reversed = {
    "1": ["one"[::-1], "1"],
    "2": ["two"[::-1], "2"],
    "3": ["three"[::-1], "3"],
    "4": ["four"[::-1], "4"],
    "5": ["five"[::-1], "5"],
    "6": ["six"[::-1], "6"],
    "7": ["seven"[::-1], "7"],
    "8": ["eight"[::-1], "8"],
    "9": ["nine"[::-1], "9"],
}

compiled_regex = re.compile(r"\d")


def part01(lines):
    print(
        reduce(
            (lambda p, n: p + (int("".join([n[0], n[-1]])))),
            list(map((lambda x: compiled_regex.findall(x)), lines)),
            0,
        )
    )


def get_index(line, tgt):
    return line.index(tgt) if tgt in line else -1


def part02_parse_line(line, reversed_line):
    first_number_found, last_number_found, first_item_index, last_item_index = (
        "-1",
        "-1",
        10_000,
        10_000,
    )
    for wo in written_out:
        for val in written_out[wo]:
            ff_index = get_index(line, val)
            if ff_index != -1 and ff_index < first_item_index:
                first_item_index = ff_index
                first_number_found = wo

        for val_rev in written_out_reversed[wo]:
            fl_index = get_index(reversed_line, val_rev)
            if fl_index != -1 and fl_index < last_item_index:
                last_item_index = fl_index
                last_number_found = wo

    return int("".join([first_number_found, last_number_found]))


def part02(lines):
    print(
        reduce(
            lambda x, y: x + y, (map(lambda l: part02_parse_line(l, l[::-1]), lines))
        )
    )
