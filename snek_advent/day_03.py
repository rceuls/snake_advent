import re

from snek_advent import validate

compiled_sterreke_regex = re.compile(r"(\*)")
compiled_int_regex = re.compile(r"(\d+)")


def check_overlap(start, end, n_start, n_end, match):
    if n_start <= start + 1 and n_end >= end - 1:
        return match
    else:
        return None


def part02(lines: list[str]):
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

    validate(total, 84159075)


def do_fluff(lines):
    len_line = 1 + len(lines[0])
    buffer = len_line * "."
    fluffed = [buffer]
    for line in lines:
        fluffed.append("." + line[:-1] + ".")
    fluffed.append(buffer)
    return fluffed


def part01(lines: list[str]):
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
    validate(total, 539713)
