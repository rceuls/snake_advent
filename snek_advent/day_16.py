from functools import partial
from multiprocessing import Pool
from sys import setrecursionlimit

from snek_advent import validate


def get_next_position(current_position, direction):
    (x, y) = current_position
    match direction:
        case "N":
            return x - 1, y
        case "S":
            return x + 1, y
        case "E":
            return x, y + 1
        case "W":
            return x, y - 1


direction_mirrors = {
    "/": {"N": "E", "E": "N", "S": "W", "W": "S"},
    "\\": {"N": "W", "E": "S", "S": "E", "W": "N"},
}


def add_to_beam_path_and_check_loop(pos, direction, field_pos_and_entries):
    if pos not in field_pos_and_entries:
        field_pos_and_entries[pos] = set()

    if direction in field_pos_and_entries[pos]:
        return True
    field_pos_and_entries[pos].add(direction)

    return False


def follow_beam(field, pos, direction, field_pos_and_entries):
    (x, y) = pos
    if x > len(field) - 1 or y > len(field[0]) - 1:
        return
    if x < 0 or y < 0:
        return
    if add_to_beam_path_and_check_loop(pos, direction, field_pos_and_entries):
        return
    curr_char = field[x][y]

    match curr_char:
        case ".":
            follow_beam(
                field,
                get_next_position(pos, direction),
                direction,
                field_pos_and_entries,
            )
        case "-":
            if direction == "N" or direction == "S":
                (x1, y1) = get_next_position(pos, "W")
                follow_beam(field, (x1, y1), "W", field_pos_and_entries)

                (x2, y2) = get_next_position(pos, "E")
                follow_beam(field, (x2, y2), "E", field_pos_and_entries)
            else:
                follow_beam(
                    field,
                    get_next_position(pos, direction),
                    direction,
                    field_pos_and_entries,
                )
        case "|":
            if direction == "E" or direction == "W":
                (x1, y1) = get_next_position(pos, "N")
                follow_beam(field, (x1, y1), "N", field_pos_and_entries)

                (x2, y2) = get_next_position(pos, "S")
                follow_beam(field, (x2, y2), "S", field_pos_and_entries)
            else:
                follow_beam(
                    field,
                    get_next_position(pos, direction),
                    direction,
                    field_pos_and_entries,
                )
        case _:
            new_direction = direction_mirrors[curr_char][direction]
            follow_beam(
                field,
                get_next_position(pos, new_direction),
                new_direction,
                field_pos_and_entries,
            )


def part01(lines: list[str]):
    setrecursionlimit(int(1e6))
    field = [list(x) for x in lines]
    pos = {}
    follow_beam(field, (0, 0), "E", pos)
    validate(len(pos), 7788)


def calc_highlights(field, starter):
    pos = {}
    (x, y, direction) = starter
    follow_beam(field, (x, y), direction, pos)
    return len(pos)


def part02(lines: list[str]):
    field = [list(x) for x in lines]
    setrecursionlimit(int(1e6))

    height = len(field)
    width = len(field[0])

    to_east = [(row, 0, "E") for row in range(height)]
    to_west = [(row, width - 1, "W") for row in range(height)]
    to_south = [(0, column, "S") for column in range(width)]
    to_north = [(height - 1, column, "N") for column in range(width)]
    all_directions = to_east + to_west + to_south + to_north
    calc_found = partial(calc_highlights, field)
    with Pool() as p:
        max_found = max(p.map(calc_found, all_directions))

    validate(max_found, 7987)
