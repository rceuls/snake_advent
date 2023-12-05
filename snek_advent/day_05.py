import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit

digit_regex = re.compile("\d+")


def parse_input(full_text):
    mapper = {"seeds": [], "converters": []}
    splitted_by_converter = full_text.split("\n\n")
    for seed in digit_regex.finditer(splitted_by_converter[0]):
        mapper["seeds"].append(int(seed.group(0)))

    for conv_ix in range(1, len(splitted_by_converter)):
        conv = splitted_by_converter[conv_ix]
        splitted_converter = conv.split("\n")
        (source, _, target) = splitted_converter[0].split(" ")[0].split("-")
        converters = {}
        for i in range(1, len(splitted_converter)):
            (dest, src, length) = [
                int(x) for x in digit_regex.findall(splitted_converter[i])
            ]
            converters[(src, src + length)] = (dest, dest + length)

        mapper["converters"].append(converters)
    return mapper


def parse_input_inverse(full_text):
    mapper = {"seeds": [], "converters": []}
    splitted_by_converter = full_text.split("\n\n")
    for seed in digit_regex.finditer(splitted_by_converter[0]):
        mapper["seeds"].append(int(seed.group(0)))

    for conv_ix in range(1, len(splitted_by_converter)):
        conv = splitted_by_converter[conv_ix]
        splitted_converter = conv.split("\n")
        (source, _, target) = splitted_converter[0].split(" ")[0].split("-")
        converter = {}
        for i in range(1, len(splitted_converter)):
            (dest, src, length) = [
                int(x) for x in digit_regex.findall(splitted_converter[i])
            ]
            converter[(dest, dest + length)] = (src, src + length)

        mapper["converters"].append(converter)
    return mapper


def parse_target(mapper, up_next):
    for key in mapper.keys():
        mapped = mapper[key]
        if key[0] <= up_next <= key[1]:
            offset = up_next - key[0]
            return mapped[0] + offset
    return up_next


def part02(lines):
    mapper = parse_input_inverse(lines)
    inversed = mapper["converters"][::-1]
    old_seeds = mapper["seeds"]
    seeds = []
    for x in range(0, len(old_seeds) - 1):
        if x % 2 == 0:
            seeds.append((old_seeds[x], old_seeds[x] + old_seeds[x + 1]))

    found = False
    ix = 0
    while not found:
        tgt = ix
        for inv in inversed:
            tgt = parse_target(inv, tgt)
        for s in seeds:
            if s[0] <= tgt <= s[1]:
                return ix
        ix += 1

    return -1


def part01(lines):
    mapper = parse_input(lines)
    lowest = 2**31
    for seed in mapper["seeds"]:
        tgt = seed
        for line in mapper["converters"]:
            tgt = parse_target(line, tgt)
        if tgt < lowest:
            lowest = tgt
    return lowest


def do(iterations, lines, do_profile=False):
    if iterations > 0:
        total_time = timeit(lambda: part01(lines), number=iterations, globals=globals())
        print(
            f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        )
        #
        # total_time = timeit(lambda: part02(lines), number=iterations, globals=globals())
        # print(
        #     f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        # )

    with Profile() as profile:
        print(f"{part01(lines) = } (should be 26273516)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    # takes half an hour :sweat:
    # with Profile() as profile:
    #     print(f"{part02(lines) = } (should be 34039469)")
    #     if do_profile:
    #         (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
