from snek_advent import validate

ROUNDED = "O"
CUBED = "#"
EMPTY = "."
EOL = "EOL"


def transpose_field(field):
    return [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]


def get_stone_or_skip(start_index: int, line: str):
    substr = line[start_index:]
    for ix, char in zip(range(len(substr)), substr):
        if char == ROUNDED or char == CUBED:
            return (ix + start_index, substr[ix])
    return (-1, EOL)


DIR_NORTH = "N"
DIR_WEST = "W"
DIR_SOUTH = "S"
DIR_EAST = "E"


def cycle(lines: [str]):
    for _ in range(3):
        (shake_stones) = shake_stones(transpose_field(lines))
    for l in shake_stones:
        print("".join(l))


def shake_stones(
    lines: list[str],
    direction: DIR_NORTH or DIR_WEST or DIR_SOUTH or DIR_EAST = DIR_NORTH,
):
    height = len(lines)
    for line in lines:
        for x in range(height):
            if line[x] == EMPTY:
                (index, type) = get_stone_or_skip(x, line)
                if type == ROUNDED:
                    line[index] = EMPTY
                    line[x] = ROUNDED
                elif type == CUBED:
                    x = index
    return lines, height


def part01(lines: list[str]):
    field = transpose_field(lines)
    lines, line_weight = shake_stones(field, DIR_NORTH)
    total_bearing_stones = 0
    for line in transpose_field(lines):
        total_bearing_stones += "".join(line).count(ROUNDED) * line_weight
        line_weight -= 1
    # validate(total_bearing_stones, 109098)


# N W S E LTR
def part02(lines: list[str]):
    field = lines

    for f in field:
        print("".join(f))
    validate(0, 0)
