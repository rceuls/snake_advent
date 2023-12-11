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
    rows_to_insert = sorted(rows_to_insert)[::-1]
    for row in rows_to_insert:
        universe.insert(row, list(universe_width * "."))

    columns_to_insert = sorted(columns_to_insert)[::-1]
    universe_height = len(universe[0]) + len(rows_to_insert)
    for column in columns_to_insert:
        for row in range(universe_height):
            universe[row].insert(column, ".")
    return universe


def part01(lines):
    universe = expand_universe(lines)
    galaxy_coords = set()
    galaxy_paths = set()
    for row in range(len(universe)):
        for column in range(len(universe[row])):
            if universe[row][column] == "#":
                galaxy_coords.add((row, column))
    galaxy_coords = list(galaxy_coords)
    for coord in range(len(galaxy_coords)):
        base_coord = galaxy_coords[coord]
        for next_coord in range(coord + 1, len(galaxy_coords)):
            galaxy_paths.add((base_coord, galaxy_coords[next_coord]))
    print(len(galaxy_paths))
    total = 0
    for pair in galaxy_paths:
        (p1, p2) = pair[0]
        (q1, q2) = pair[1]
        taxi_distance = abs(p1 - q1) + abs(p2 - q2)
        total += taxi_distance
    return validate_and_return(9805264, total)


def part02(lines):
    return validate_and_return(0, 0)
