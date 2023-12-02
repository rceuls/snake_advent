import re
from cProfile import Profile
from functools import reduce
from pstats import Stats, SortKey
from timeit import timeit

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
    return reduce(
        (lambda p, n: p + int(f"{n[0]}{n[-1]}")),
        map((lambda x: compiled_regex.findall(x)), lines),
        0,
    )


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
    return reduce(
        lambda x, y: x + y, map(lambda l: part02_parse_line(l, l[::-1]), lines)
    )


def do(iterations, lines, do_profile=False):
    if iterations > 0:
        total_time = timeit(lambda: part01(lines), number=iterations, globals=globals())
        print(
            f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        )

        total_time = timeit(lambda: part02(lines), number=iterations, globals=globals())
        print(
            f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        )

    with Profile() as profile:
        print(f"{part01(lines) = } (should be 54597)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 54504)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
