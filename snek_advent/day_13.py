from snek_advent import validate


def get_fields(text):
    fields = []
    field = []
    ix = 0
    for line in text.split("\n\n"):
        ix += 1
        for subline in line.split("\n"):
            fields.append(subline.strip())
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


def part01(lines: list):
    fields = get_fields(lines)
    total_columns = 0
    total_rows = 0
    for field in fields:
        print("\n".join(field))
        row = find_vertical_mirror(field)
        column = find_vertical_mirror(transpose_field(field))
        total_rows += row
        total_columns += column

        print(row, column)

    print(total_columns * 100 + total_rows)

    ## 42214 too low
    ## high: 90328

    validate(0, 0)


def part02(lines: list[str]):
    validate(0, 0)