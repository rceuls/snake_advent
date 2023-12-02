import re
from cProfile import Profile
from timeit import timeit


def part02(lines):
    pwr_total = 0
    for super_line in map(lambda x: x.replace("Game ", ""), lines):
        line = super_line.split(":")
        max_blue = 0
        max_red = 0
        max_green = 0
        for game in line[1].split(";"):
            for color in map(lambda x: x.strip(), game.split(",")):
                tgt_color = color.split(" ")[1]
                tgt_count = int(color.split(" ")[0])
                if tgt_color == "blue" and tgt_count > max_blue:
                    max_blue = tgt_count
                if tgt_color == "red" and tgt_count > max_red:
                    max_red = tgt_count
                if tgt_color == "green" and tgt_count > max_green:
                    max_green = tgt_count
        pwr_total += max_blue * max_green * max_red
    return pwr_total


regex_green = re.compile(r"(\d+) (green,?;?)")
regex_red = re.compile(r"(\d+) (red,?;?)")
regex_blue = re.compile(r"(\d+) (blue,?;?)")


def part01(lines):
    maxes = {"red": 12, "green": 13, "blue": 14}
    game_count = len(lines)
    gauss_total = int(1 / 2 * (game_count * (game_count + 1)))
    ix = 1
    for super_line in lines:
        line = super_line.split(":")
        is_valid = True
        for m in regex_red.findall(line[1]):
            if int(m[0]) > 12:
                gauss_total -= ix
                is_valid = False
                break
        for m in regex_green.findall(line[1]):
            if int(m[0]) > 13:
                gauss_total -= ix
                is_valid = False
                break
        for m in regex_blue.findall(line[1]):
            if int(m[0]) > 14:
                gauss_total -= ix
                is_valid = False

                break

        ix += 1

        if not is_valid:
            break

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
            # (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

        with Profile() as profile:
            print(f"{part02(lines) = } (should be 66681)")
            # (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
