from snek_advent import validate


def get_fields(text):
    fields = list()
    for line in text.split("\n\n"):
        field = list()
        for sub_line in line.split("\n"):
            line = sub_line.strip()
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


def find_mirror_smudged(field):
    width = len(field[0])
    height = len(field[0])
    for x in range(1, width):
        row_matches = height
        smudge_found = False
        for row in field:
            to_compare_width = min(width - x, x)
            left = row[x - to_compare_width : x]
            right = row[x : to_compare_width + x][::-1]
            for y in range(0, len(left)):
                if left[y] != right[y]:
                    row_matches -= 1
                    if not smudge_found:
                        smudge_found = True
                    break

        if smudge_found and row_matches == height - 1:
            return x
    return 0


def calc_field(field):
    row = find_vertical_mirror(field)
    if row:
        return row, 0
    else:
        column = find_vertical_mirror(transpose_field(field))
        return 0, column


def calc_field_smudged(field):
    row = find_mirror_smudged(field)
    if row:
        return row, 0
    else:
        column = find_mirror_smudged(transpose_field(field))
        return 0, column


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


def part02(text: str):
    fields = get_fields(text)
    total_columns = 0
    total_rows = 0
    rows_and_columns = map(calc_field_smudged, fields)

    for r in rows_and_columns:
        total_rows += r[0]
        total_columns += r[1]

    hits = total_columns * 100 + total_rows
    validate(hits, 36771)
