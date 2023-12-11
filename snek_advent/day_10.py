from matplotlib.path import Path
from termcolor import colored

from snek_advent import validate


def get_animal_starting_position(field):
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column] == "S":
                return row, column
    raise Exception("No starting position found")


def get_field_symbol(row_and_column, field):
    return field[row_and_column[0]][row_and_column[1]]


def assign_or_skip(viable_position, previous_positions, previous_position_checker):
    if viable_position not in previous_position_checker:
        previous_positions.append(viable_position)
        previous_position_checker.add(viable_position)
        return viable_position
    return None


def get_next_field_position(
    viable_position, field, previous_positions, previous_position_checker
):
    while viable_position is not None:
        current_symbol = get_field_symbol(viable_position, field)
        (row, column) = viable_position
        if current_symbol == "│":
            viable_position = assign_or_skip(
                (row + 1, column), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row - 1, column), previous_positions, previous_position_checker
                )
        elif current_symbol == "─":
            viable_position = assign_or_skip(
                (row, column + 1), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row, column - 1), previous_positions, previous_position_checker
                )
        elif current_symbol == "└":
            viable_position = assign_or_skip(
                (row, column + 1), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row - 1, column), previous_positions, previous_position_checker
                )
        elif current_symbol == "┘":
            viable_position = assign_or_skip(
                (row - 1, column), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row, column - 1), previous_positions, previous_position_checker
                )
        elif current_symbol == "┐":
            viable_position = assign_or_skip(
                (row, column - 1), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row + 1, column), previous_positions, previous_position_checker
                )
        elif current_symbol == "┌":
            viable_position = assign_or_skip(
                (row + 1, column), previous_positions, previous_position_checker
            )
            if viable_position is None:
                viable_position = assign_or_skip(
                    (row, column + 1), previous_positions, previous_position_checker
                )


def do_fluff(lines):
    len_line = 1 + len(lines[0])
    buffer = len_line * "W"
    fluffed = [buffer]
    for line in lines:
        fluffed.append("W" + line + "W")
    fluffed.append(buffer)
    return fluffed


def get_loop(lines):
    lines = do_fluff(lines)
    field = [
        list(line.translate(str.maketrans("-|F7LJ.", "─│┌┐└┘."))) for line in lines
    ]
    starting_position = get_animal_starting_position(field)
    loop_starts = {
        "south": (starting_position[0] + 1, starting_position[1]),
        "north": (starting_position[0] - 1, starting_position[1]),
        "west": (starting_position[0], starting_position[1] - 1),
        "east": (starting_position[0], starting_position[1] + 1),
    }
    starter_position = None
    if get_field_symbol(loop_starts["south"], field) in ["│", "└", "┘"]:
        starter_position = loop_starts["south"]

    if starter_position is None and get_field_symbol(loop_starts["north"], field) in [
        "│",
        "┐",
        "┌",
    ]:
        starter_position = loop_starts["north"]

    if starter_position is None and get_field_symbol(loop_starts["east"], field) in [
        "─",
        "J",
        "┐",
    ]:
        starter_position = loop_starts["east"]

    if starter_position is None and get_field_symbol(loop_starts["west"], field) in [
        "─",
        "└",
        "┌",
    ]:
        starter_position = loop_starts["west"]

    steps = list()
    steps.append(starting_position)
    steps.append(starter_position)

    previous_position_checker = set()
    previous_position_checker.add(starting_position)
    previous_position_checker.add(starting_position)
    get_next_field_position(starter_position, field, steps, previous_position_checker)
    return steps, field, starting_position


def part01(lines: list[str]):
    (steps, field, _) = get_loop(lines)
    validate(int(len(steps) / 2), 6828)


def part02(lines: list[str]):
    (steps, field, start_coords) = get_loop(lines)
    polygon = Path(list(steps))
    contained = 0
    visualisation = False
    for x in range(0, len(field)):
        for y in range(0, len(field[x])):
            if (x, y) not in steps:
                field[x][y] = "M" if polygon.contains_point((x, y)) else "~"
                if field[x][y] == "M":
                    contained += 1
    if visualisation:
        for x in range(0, len(field)):
            print("\n", end="")
            for y in range(0, len(field[x])):
                if get_field_symbol((x, y), field) == "S":
                    print(colored(field[x][y], "blue", attrs=["bold"]), end="")
                elif (x, y) in steps:
                    print(colored(field[x][y], "red"), end="")
                elif get_field_symbol((x, y), field) == "~":
                    print(colored("~", "blue", attrs=["bold"]), end="")
                elif get_field_symbol((x, y), field) == "M":
                    print(colored("M", color="magenta", attrs=["blink"]), end="")
                else:
                    print(colored(" "), end="")
        print("\n")
    validate(contained, 459)
