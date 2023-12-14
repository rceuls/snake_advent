from functools import cache
import pprint as p
from snek_advent import validate

ROUNDED = "O"
CUBED = "#"
EMPTY = "."
EOL = "EOL"

DIR_NORTH = "N"
DIR_WEST = "W"
DIR_SOUTH = "S"
DIR_EAST = "E"

LEFT = "L"
RIGHT = "R"


def get_stone_or_skip(start_index: int, line: str):
    substr = line[start_index:]
    for ix, char in zip(range(len(substr)), substr):
        if char == ROUNDED or char == CUBED:
            return (ix + start_index, substr[ix])
    return (-1, EOL)


def update_line(line: str, drop_to_the: LEFT or RIGHT):
    working_copy = list(line)
    if drop_to_the == RIGHT:
        working_copy = list(line[::-1])
    for x in range(len(working_copy)):
        if working_copy[x] == EMPTY:
            (index, type) = get_stone_or_skip(x, working_copy)
            if type == ROUNDED:
                working_copy[index] = EMPTY
                working_copy[x] = ROUNDED
            elif type == CUBED:
                x = index
    if drop_to_the == RIGHT:
        return working_copy[::-1]
    return working_copy


transposed_stones = {}


def get_cache_key(lines):
    to_hash = ""
    for line in lines:
        to_hash += "".join(line)
    return hash(to_hash)


def cache(key, result):
    transposed_stones[key] = result


def shake_stones(
    lines,
    direction: DIR_NORTH or DIR_WEST or DIR_SOUTH or DIR_EAST = DIR_NORTH,
):
    if direction == DIR_NORTH or direction == DIR_SOUTH:
        for x in range(len(lines)):
            line = list()
            for y in range(len(lines[0])):
                line.append(lines[y][x])
            updated_line = update_line(
                "".join(line), RIGHT if direction == DIR_SOUTH else LEFT
            )
            for y1 in range(len(lines[0])):
                lines[y1][x] = updated_line[y1]
    elif direction == DIR_EAST or direction == DIR_WEST:
        for ix in range(len(lines)):
            updated_line = update_line(
                "".join(lines[ix]), RIGHT if direction == DIR_EAST else DIR_WEST
            )
            del lines[ix]
            lines.insert(ix, updated_line)
    return lines


def part01(lines: list[str]):
    lines = [list(l) for l in lines]
    lines = shake_stones(lines, DIR_NORTH)
    line_weight = len(lines)
    total_bearing_stones = 0
    for line in lines:
        total_bearing_stones += "".join(line).count(ROUNDED) * line_weight
        line_weight -= 1
    mapped = ""
    for f in lines:
        mapped += ("".join(f)) + "\n"


def calculate_weight(lines):
    total_bearing_stones = 0
    line_weight = len(lines[0])
    for line in lines:
        total_bearing_stones += "".join(line).count(ROUNDED) * line_weight
        line_weight -= 1
    return total_bearing_stones


hash_and_result = {}


# N W S E LTR
def part02(lines: list[str]):
    lines = [list(l) for l in lines]
    rollers = [DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_EAST]
    baseline = 1_000_000_000
    divider = 17
    remainder = (baseline % divider) - 1
    for i in range(remainder):
        for r in rollers:
            lines = shake_stones(lines, r)
    print(calculate_weight(lines))

    #     key = get_cache_key(lines)
    #     if key not in indices:
    #         indices[key] = [i]
    #         hash_and_result[key] = calculate_weight(lines)
    #     else:
    #         indices[key].append(i)
    # print(calculate_weight(lines))
    # p.pprint(hash_and_result)
    # print(len(hash_and_result))
    # p.pprint(indices)
    # for key in indices.keys():
    #     values = indices[key]
    #     if values[0] == remainder - 1:
    #         print(key)
    #         print(hash_and_result[key])

    # for f in field:
    #     print("".join(f))
    validate(0, 0)

    # 99397, 99380, 99402, 99441 = low
    # 101063 not correct
