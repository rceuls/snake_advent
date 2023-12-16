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


field_pos_and_entries = {}


def add_to_beam_path_and_check_loop(pos, direction):
    if pos not in field_pos_and_entries:
        field_pos_and_entries[pos] = set()

    if direction in field_pos_and_entries[pos]:
        return True
    field_pos_and_entries[pos].add(direction)

    return False


def follow_beam(field, pos, direction):
    (x, y) = pos
    if x > len(field) - 1 or y > len(field[0]) - 1:
        return
    if x < 0 or y < 0:
        return
    if add_to_beam_path_and_check_loop(pos, direction):
        return
    curr_char = field[x][y]

    match curr_char:
        case ".":
            follow_beam(field, get_next_position(pos, direction), direction)
        case "-":
            if direction == "N" or direction == "S":
                (x1, y1) = get_next_position(pos, "W")
                follow_beam(field, (x1, y1), "W")

                (x2, y2) = get_next_position(pos, "E")
                follow_beam(field, (x2, y2), "E")
            else:
                follow_beam(
                    field,
                    get_next_position(pos, direction),
                    direction,
                )
        case "|":
            if direction == "E" or direction == "W":
                (x1, y1) = get_next_position(pos, "N")
                follow_beam(field, (x1, y1), "N")

                (x2, y2) = get_next_position(pos, "S")
                follow_beam(field, (x2, y2), "S")
            else:
                follow_beam(field, get_next_position(pos, direction), direction)
        case _:
            new_direction = direction_mirrors[curr_char][direction]
            follow_beam(
                field,
                get_next_position(pos, new_direction),
                new_direction,
            )


def part01(lines: list[str]):
    setrecursionlimit(int(1e6))
    field = [list(x) for x in lines]
    follow_beam(field, (0, 0), "E")
    validate(len(field_pos_and_entries), 7788)


def part02(lines: list[str]):
    setrecursionlimit(int(1e6))
    field = [list(x) for x in lines]

    max_found = 0
    height = len(field)
    width = len(field[0])

    for row in range(height):
        field_pos_and_entries.clear()
        follow_beam(field, (row, 0), "E")
        curr_max = len(field_pos_and_entries)
        max_found = max(curr_max, max_found)

    for row in range(height):
        field_pos_and_entries.clear()
        follow_beam(field, (row, width - 1), "W")
        curr_max = len(field_pos_and_entries)
        max_found = max(curr_max, max_found)

    for column in range(width):
        field_pos_and_entries.clear()
        follow_beam(field, (0, column - 1), "S")
        curr_max = len(field_pos_and_entries)
        max_found = max(curr_max, max_found)

    for column in range(width):
        field_pos_and_entries.clear()
        follow_beam(field, (height - 1, column), "N")
        curr_max = len(field_pos_and_entries)
        max_found = max(curr_max, max_found)

    validate(max_found, 7987)
