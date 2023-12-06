import cmath
import math
import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit

digit_regex = re.compile("\d+")


def c_distance(time_held, race_time):
    travel_time_left = race_time - time_held
    return travel_time_left * time_held


def parse_lines(lines):
    time = [int(x) for x in digit_regex.findall(lines[0])]
    distance = [int(x) for x in digit_regex.findall(lines[1])]
    races = zip(time, distance)
    return races


def quadratic(race_time, distance):
    a = -1
    d = (race_time**2) - (4 * a * -distance)
    uno = (-race_time - cmath.sqrt(d)) / (2 * a)
    duo = (-race_time + cmath.sqrt(d)) / (2 * a)
    tres = sorted([uno.real, duo.real])
    return math.ceil(tres[0]), math.floor(tres[1])


def part02(lines):
    races = list(parse_lines([x.replace(" ", "") for x in lines]))

    return math.prod(
        [
            len(range(a, b + 1))
            for a, b in [
                quadratic(race_time, distance) for race_time, distance in races
            ]
        ]
    )


def part01(lines):
    races = parse_lines(lines)
    return math.prod(
        [
            len(range(a, b + 1))
            for a, b in [
                quadratic(race_time, distance) for race_time, distance in races
            ]
        ]
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
        print(f"{part01(lines) = } (should be 608902)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 46173809)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
