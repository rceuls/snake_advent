import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit


digit_regex = re.compile("\d+")


def parse_input(full_text):
    mapper = {"seeds": [], "converters": {}}
    splitted_by_converter = full_text.split("\n\n")
    for seed in digit_regex.finditer(splitted_by_converter[0]):
        mapper["seeds"].append(int(seed.group(0)))
    for conv_ix in range(1, len(splitted_by_converter)):
        conv = splitted_by_converter[conv_ix]
        splitted_converter = conv.split("\n")
        (source, _, target) = splitted_converter[0].split(" ")[0].split("-")
        converters = {"target": target, "ranges": {}}
        for i in range(1, len(splitted_converter)):
            (dest, src, length) = [
                int(x) for x in digit_regex.findall(splitted_converter[i])
            ]
            converters["ranges"][(src, src + length)] = {
                "length": length,
                "dest": dest,
            }

        mapper["converters"][source] = converters
    print(mapper)
    return mapper


def parse_target(mapper, medium, origin):
    if medium in mapper:
        for key in mapper[medium]["ranges"].keys():
            if key[0] <= origin and key[1] >= origin:
                dest = mapper[medium]["ranges"][key]["dest"]
                offset = origin - key[0]
                print(
                    medium,
                    "->",
                    new_medium,
                    origin,
                    key,
                    dest,
                    "+",
                    offset,
                    "=",
                    dest + offset,
                )
                new_medium = mapper[medium]["target"]
                return parse_target(mapper, new_medium, dest + offset)
        return parse_target(mapper, new_medium, origin)
    return origin


def part02(lines):
    pass


def part01(lines):
    mapper = parse_input(lines)
    lowest = 2**31
    for seed in mapper["seeds"]:
        tgt = parse_target(mapper["converters"], "seed", seed)
        exit(0)
        if tgt < lowest:
            lowest = tgt

    # too high: 30069991
    return lowest


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
        print(f"{part01(lines) = } (should be 23941)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 5571760)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
