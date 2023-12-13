from snek_advent import validate


def get_fields(lines: list[str]):
    fields = []
    field = []
    ix = 0
    for line in lines:
        ix += 1
        if line == "" or ix == len(lines):
            fields.append(field)
            field = []
        else:
            field.append(line)
    return fields


def transpose_field(field):
    data = [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]
    as_string = []
    for d in data:
        as_string.insert(0, "".join(d))
    return as_string


def find_row_mirror(field):
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
    return -1


def part01(lines: list[str]):
    fields = get_fields(lines)
    total_columns = 0
    total_rows = 0
    ix = 0
    for field in fields:
        ix += 1
        row = find_row_mirror(field)
        column = find_row_mirror(transpose_field(field))
        total_rows += row if row != -1 else 0
        total_columns += column if column != -1 else 0
        if row == column == -1:
            print(ix, field[0], row, column)
            print("\n".join(field))
            print("-" * 80)
            row = find_row_mirror(field)
            print("\n".join(transpose_field(field)))

            column = find_row_mirror(transpose_field(field))

    print(total_columns * 100 + total_rows)

    ## 42214 too low

    validate(0, 0)


def part02(lines: list[str]):
    validate(0, 0)
