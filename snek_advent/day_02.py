import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit


regex_green = re.compile(r"(\d+) (green,?;?)")
regex_red = re.compile(r"(\d+) (red,?;?)")
regex_blue = re.compile(r"(\d+) (blue,?;?)")


def part02(lines):
    pwr_total = 0
    for super_line in lines:
        line = super_line.split(":")
        max_values = {"blue": 0, "red": 0, "green": 0}
        for _, game in enumerate(line[1].split(";")):
            for color in [x.strip() for x in game.split(",")]:
                tgt_count = int(color.split(" ")[0])
                if "blue" in color and tgt_count > max_values["blue"]:
                    max_values["blue"] = tgt_count
                elif "red" in color and tgt_count > max_values["red"]:
                    max_values["red"] = tgt_count
                elif "green" in color and tgt_count > max_values["green"]:
                    max_values["green"] = tgt_count
        pwr_total += max_values["blue"] * max_values["green"] * max_values["red"]
    return pwr_total


def part01_calc(line, ix):
    if (
        next((m for m in regex_red.finditer(line) if int(m.group(1)) > 12), False)
        or next((m for m in regex_green.finditer(line) if int(m.group(1)) > 13), False)
        or next(
            (m for m in regex_blue.finditer(line) if int(m.group(1)) > 14),
            False,
        )
    ):
        return ix
    return 0


def part01(lines):
    game_count = len(lines)
    gauss_total = int(1 / 2 * (game_count * (game_count + 1)))
    ix = 0
    while ix < game_count:
        line = lines[ix]
        ix += 1
        gauss_total -= part01_calc(line, ix)

    return gauss_total


def do(iterations, lines, do_profile=False):
    total_time = timeit(lambda: part01(lines), number=iterations, globals=globals())
    print(
        f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
    )

    total_time = timeit(lambda: part02(lines), number=iterations, globals=globals())
    print(
        f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
    )

    if do_profile:
        with Profile() as profile:
            print(f"{part01(lines) = } (should be 2237)")
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

        with Profile() as profile:
            print(f"{part02(lines) = } (should be 66681)")
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
