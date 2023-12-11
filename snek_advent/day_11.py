from functools import reduce
from snek_advent import validate_and_return


def expand_universe(lines):
    universe = [list(l) for l in lines]
    universe_width = len(universe[0])
    universe_height = len(universe)
    empty_row = list(universe_width * ".")
    rows_to_insert = set()
    for x in range(universe_height):
        if universe[x] == empty_row:
            rows_to_insert.add(x)

    empty_column = list(universe_height * ".")
    columns_to_insert = set()

    for column in range(universe_width):
        under_review = list()
        for row in range(universe_height):
            under_review.append(universe[row][column])
        if under_review == empty_column:
            columns_to_insert.add(column)

    return universe, rows_to_insert, columns_to_insert, universe_height, universe_width


def send_taxi(pair):
    (p1, p2) = pair[0]
    (q1, q2) = pair[1]
    return abs(p1 - q1) + abs(p2 - q2)


def calculate_distance(empty_counts_for, lines):
    (
        universe,
        empty_rows,
        empty_cols,
        universe_height,
        universe_width,
    ) = expand_universe(lines)
    galaxy_coords = set()

    empty_rows_crossed = 0
    for row in range(universe_height):
        if row in empty_rows:
            empty_rows_crossed += 1
        empty_cols_crossed = 0

        for column in range(universe_width):
            if column in empty_cols:
                empty_cols_crossed += 1
            if universe[row][column] == "#":
                galaxy_coords.add(
                    (
                        row
                        - empty_rows_crossed
                        + (empty_rows_crossed * empty_counts_for),
                        column
                        - empty_cols_crossed
                        + (empty_cols_crossed * empty_counts_for),
                    )
                )
    galaxy_coords = list(galaxy_coords)
    total = 0
    for coord in range(len(galaxy_coords)):
        base_coord = galaxy_coords[coord]
        for next_coord in range(coord + 1, len(galaxy_coords)):
            total += send_taxi((base_coord, galaxy_coords[next_coord]))
    return total


def part01(lines):
    total = calculate_distance(2, lines)
    validate_and_return(9805264, total)


def part02(lines):
    total = calculate_distance(1_000_000, lines)
    validate_and_return(779032247216, total)
