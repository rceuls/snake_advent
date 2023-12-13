from snek_advent import validate


def get_fields(text):
    fields = list()
    for line in text.split("\n\n"):
        field = list()
        for subline in line.split("\n"):
            line = list(subline.strip())
            if line:
                field.append(line)
        fields.append(field)
    return fields


def transpose_field(field):
    return [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]


def find_vertical_mirror(field):
    width = len(field[0])
    height = len(field[0])
    for x in range(1, width):
        row_matches = height
        for row in field:
            to_compare_width = min(width - x, x)
            left = row[x - to_compare_width : x]
            right = row[x : to_compare_width + x][::-1]
            if left != right:
                row_matches -= 1
                break
        if row_matches == height:
            return x
    return 0


def calc_field(field):
    row = find_vertical_mirror(field)
    column = find_vertical_mirror(transpose_field(field))
    return (row, column)


def part01(text: str):
    fields = get_fields(text)
    total_columns = 0
    total_rows = 0
    rows_and_columns = map(calc_field, fields)

    for r in rows_and_columns:
        total_columns += r[1]
        total_rows += r[0]

    hits = total_columns * 100 + total_rows

    validate(hits, 43614)


def part02(lines: list[str]):
    validate(0, 0)
