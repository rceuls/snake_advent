import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit


compiled_sterreke_regex = re.compile(r"(\*)")
compiled_int_regex = re.compile(r"(\d+)")


def check_overlap(start, end, n_start, n_end, match):
    if n_start <= start + 1 and n_end >= end - 1:
        return match
    else:
        return None


def part02(lines):
    actual_lines = do_fluff(lines)
    total = 0
    matches_per_line = {}
    sterrekes_per_line = {}

    for ix in range(1, len(actual_lines) - 1):
        if ix not in matches_per_line:
            matches_per_line[ix] = [
                {
                    "start": match.span()[0],
                    "end": match.span()[1],
                    "match": int(match.group(1)),
                }
                for match in compiled_int_regex.finditer(actual_lines[ix])
            ]
        if ix + 1 not in matches_per_line:
            next_line = actual_lines[ix + 1]
            matches_per_line[ix + 1] = [
                {
                    "start": match.span()[0],
                    "end": match.span()[1],
                    "match": int(match.group(1)),
                }
                for match in compiled_int_regex.finditer(next_line)
            ]
        if ix not in sterrekes_per_line:
            sterrekes_per_line[ix] = list(
                compiled_sterreke_regex.finditer(actual_lines[ix])
            )

        for hit in sterrekes_per_line[ix]:
            numbers_previous_line = matches_per_line[ix - 1]
            numbers_current_line = matches_per_line[ix]
            numbers_next_line = matches_per_line[ix + 1]
            (x, y) = hit.span()
            numbers = []

            for n in numbers_previous_line:
                if len(numbers) == 2:
                    break
                iv = check_overlap(x, y, n["start"], n["end"], n["match"])
                if iv is not None:
                    numbers.append(iv)

            for n in numbers_next_line:
                if len(numbers) == 2:
                    break
                iv = check_overlap(x, y, n["start"], n["end"], n["match"])
                if iv is not None:
                    numbers.append(iv)

            for n in numbers_current_line:
                if len(numbers) == 2:
                    break
                iv = check_overlap(x, y, n["start"], n["end"], n["match"])
                if iv is not None:
                    numbers.append(iv)

            if len(numbers) == 2:
                total += numbers[0] * numbers[1]

    return total


def do_fluff(lines):
    len_line = 1 + len(lines[0])
    buffer = len_line * "."
    fluffed = [buffer]
    for line in lines:
        fluffed.append("." + line[:-1] + ".")
    fluffed.append(buffer)
    return fluffed


def part01(lines):
    actual_lines = do_fluff(lines)
    total = 0
    valid_neighbour = ".012345789"
    for ix in range(1, len(actual_lines) - 1):
        matches_per_line = [
            {
                "start": match.span()[0],
                "end": match.span()[1],
                "match": int(match.group(1)),
            }
            for match in compiled_int_regex.finditer(actual_lines[ix])
        ]

        for hit in matches_per_line:
            if (
                actual_lines[ix][hit["start"] - 1] != "."
                or actual_lines[ix][hit["end"]] != "."
            ):
                total += hit["match"]
            else:
                next_line_negated = actual_lines[ix + 1][
                    hit["start"] - 1 : hit["end"] + 1
                ]
                previous_line_negated = actual_lines[ix - 1][
                    hit["start"] - 1 : hit["end"] + 1
                ]
                for iy in range(0, len(next_line_negated)):
                    c_n = next_line_negated[iy]
                    c_p = previous_line_negated[iy]
                    if c_n not in valid_neighbour or c_p not in valid_neighbour:
                        total += hit["match"]
                        break
    return total  # 4361


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
        print(f"{part01(lines) = } (should be 539713)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 84159075)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats())
