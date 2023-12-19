from collections import namedtuple

from snek_advent import validate

Action = namedtuple("Action", "dir amount color")
Coordinate = namedtuple("Coordinate", "row column")

DO_STUFF = {
    "D": Coordinate(row=1, column=0),
    "U": Coordinate(row=-1, column=0),
    "L": Coordinate(row=0, column=-1),
    "R": Coordinate(row=0, column=1),
    "1": Coordinate(row=1, column=0),
    "3": Coordinate(row=-1, column=0),
    "2": Coordinate(row=0, column=-1),
    "0": Coordinate(row=0, column=1),
}


def part01(lines: list[str]):
    current_coordinate = Coordinate(row=0, column=0)
    vertices = []
    length = 0
    vertices.append(current_coordinate)
    for action in lines:
        (direction, amount, _) = action.split()
        amount = int(amount)
        length += amount
        new_point = Coordinate(
            row=current_coordinate.row + (amount * DO_STUFF[direction].row),
            column=current_coordinate.column + (amount * DO_STUFF[direction].column),
        )
        current_coordinate = new_point

        vertices.append(new_point)

    area_covered = int(
        abs(
            sum(
                (v1[0] + v2[0]) * (v1[1] - v2[1]) / 2
                for v1, v2 in zip(vertices, vertices[1:])
            )
        )
    )
    area = int(area_covered + length / 2 + 1)
    validate(area, 34329)


def part02(lines: list[str]):
    current_coordinate = Coordinate(row=0, column=0)
    vertices = []
    length = 0
    vertices.append(current_coordinate)
    for action in lines:
        (_, _, color) = action.split()
        # (#70c710)
        direction = color[7]
        amount = int(color[2:-2], 16)
        length += amount
        new_point = Coordinate(
            row=current_coordinate.row + (amount * DO_STUFF[direction].row),
            column=current_coordinate.column + (amount * DO_STUFF[direction].column),
        )
        current_coordinate = new_point

        vertices.append(new_point)

    area_covered = int(
        abs(
            sum(
                (v1[0] + v2[0]) * (v1[1] - v2[1]) / 2
                for v1, v2 in zip(vertices, vertices[1:])
            )
        )
    )
    area = int(area_covered + length / 2 + 1)
    validate(area, 42617947302920)
