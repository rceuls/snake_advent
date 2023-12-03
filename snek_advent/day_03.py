import re
from cProfile import Profile
from functools import reduce
from pstats import Stats, SortKey
from timeit import timeit


compiled_sterreke_regex = re.compile(r"(\*)")
compiled_int_regex = re.compile(r"(\d+)")


def check_overlap(start, end, match):
    (n_start, n_end) = match.span()
    if n_start <= start + 1 and n_end >= end - 1:
        return int(match.group(1))
    else:
        return None


def part02(lines):
    actual_lines = do_fluff(lines)
    total = 0
    for ix in range(1, len(actual_lines) - 1):
        previous_line = actual_lines[ix - 1]
        current_line = actual_lines[ix]
        next_line = actual_lines[ix + 1]

        for hit in compiled_sterreke_regex.finditer(
            current_line,
        ):
            numbers_previous_line = compiled_int_regex.finditer(previous_line)
            numbers_current_line = compiled_int_regex.finditer(current_line)
            numbers_next_line = compiled_int_regex.finditer(next_line)
            (x, y) = hit.span()
            numbers = []
            for n in numbers_previous_line:
                iv = check_overlap(x, y, n)
                if iv is not None:
                    numbers.append(iv)
            for n in numbers_next_line:
                iv = check_overlap(x, y, n)
                if iv is not None:
                    numbers.append(iv)
            for n in numbers_current_line:
                iv = check_overlap(x, y, n)
                if iv is not None:
                    numbers.append(iv)
            if len(numbers) == 2:
                total += reduce(lambda a, b: a * b, numbers, 1)
    return total  # example 467835


def do_fluff(lines):
    len_line = 1 + len(lines[0])
    buffer = len_line * "."
    fluffed = [buffer]
    for line in lines:
        fluffed.append("." + line.replace("\n", "") + ".")
    fluffed.append(buffer)
    return fluffed


def part01(lines):
    actual_lines = do_fluff(lines)
    total = 0
    for ix in range(1, len(actual_lines) - 1):
        previous_line = actual_lines[ix - 1]
        current_line = actual_lines[ix]
        next_line = actual_lines[ix + 1]
        for hit in compiled_int_regex.finditer(
            current_line,
        ):
            full = hit.group(1)
            current_line_prev_and_next = (
                current_line[hit.span()[0] - 1] + current_line[hit.span()[1]]
            )
            if current_line_prev_and_next != "..":
                total += int(full)
            else:
                next_line_negated = next_line[hit.span()[0] - 1 : hit.span()[1] + 1]
                previous_line_negated = previous_line[
                    hit.span()[0] - 1 : hit.span()[1] + 1
                ]
                for iy in range(0, len(next_line_negated)):
                    c_n = next_line_negated[iy]
                    c_p = previous_line_negated[iy]
                    if c_n != "." and not c_n.isdigit():
                        total += int(full)
                        break
                    elif c_p != "." and not c_p.isdigit():
                        total += int(full)
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
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 84159075)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
