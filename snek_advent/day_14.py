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


def get_stone_or_skip(start_index: int, line: [str]):
    substr = line[start_index:]
    for ix, char in zip(range(len(substr)), substr):
        if char == ROUNDED or char == CUBED:
            return ix + start_index, substr[ix]
    return -1, EOL


def update_line(line: [str], drop_to_the: LEFT or RIGHT):
    working_copy = line.copy()
    if drop_to_the == RIGHT:
        working_copy = list(line[::-1])
    for x in range(len(working_copy)):
        if working_copy[x] == EMPTY:
            (index, found_type) = get_stone_or_skip(x, working_copy)
            if found_type == ROUNDED:
                working_copy[index] = EMPTY
                working_copy[x] = ROUNDED
            elif found_type == CUBED:
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
            updated_line = update_line(line, RIGHT if direction == DIR_SOUTH else LEFT)
            for y1 in range(len(lines[0])):
                lines[y1][x] = updated_line[y1]
    elif direction == DIR_EAST or direction == DIR_WEST:
        for ix in range(len(lines)):
            updated_line = update_line(
                lines[ix], RIGHT if direction == DIR_EAST else LEFT
            )
            del lines[ix]
            lines.insert(ix, updated_line)
    return lines


def calculate_weight(lines):
    total_bearing_stones = 0
    line_weight = len(lines[0])
    for line in lines:
        total_bearing_stones += "".join(line).count(ROUNDED) * line_weight
        line_weight -= 1
    return total_bearing_stones


def part01(lines: list[str]):
    lines = [list(l) for l in lines]
    lines = shake_stones(lines, DIR_NORTH)
    validate(calculate_weight(lines), 109098)


def do_spin(lines):
    rollers = [DIR_NORTH, DIR_WEST, DIR_SOUTH, DIR_EAST]
    for r in rollers:
        lines = shake_stones(lines, r)
    return lines


def do_the_thing(number, lines):
    precache = {}
    for current_spin in range(number):
        lines_key = lines.__str__()
        if lines_key in precache:
            cycle_length = current_spin - cache[lines_key]
            remaining_cycles = (number - current_spin) % cycle_length
            for _ in range(remaining_cycles):
                lines = do_spin(lines)
            return lines

        precache[lines_key] = current_spin
        lines = do_spin(lines)


# N W S E LTR
def part02(lines: list[str]):
    lines = [list(l) for l in lines]
    print(calculate_weight(do_the_thing(1_000_000_000, lines)))
    validate(calculate_weight(lines), 100064)
