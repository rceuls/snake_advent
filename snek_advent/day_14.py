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


def transpose_field(field):
    return [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]


def get_stone_or_skip(start_index: int, line: str):
    substr = line[start_index:]
    for ix, char in zip(range(len(substr)), substr):
        if char == ROUNDED or char == CUBED:
            return (ix + start_index, substr[ix])
    return (-1, EOL)


def cycle(lines: [str]):
    for _ in range(3):
        (shake_stones) = shake_stones(transpose_field(lines))
    for l in shake_stones:
        print("".join(l))


def update_line(line: [str], look_to_the: LEFT or RIGHT):
    working_copy = line.copy()
    if look_to_the == DIR_WEST:
        working_copy = line[::-1]
    for x in range(len(working_copy)):
        if working_copy[x] == EMPTY:
            (index, type) = get_stone_or_skip(x, working_copy)
            if type == ROUNDED:
                working_copy[index] = EMPTY
                working_copy[x] = ROUNDED
            elif type == CUBED:
                x = index
    if look_to_the == DIR_WEST:
        return working_copy[::-1]
    return working_copy


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
        return lines
    if direction == DIR_EAST or direction == DIR_WEST:
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
    print(mapped)
    print(total_bearing_stones)


# N W S E LTR
def part02(lines: list[str]):
    field = lines

    # for f in field:
    #     print("".join(f))
    validate(0, 0)
