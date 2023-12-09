from functools import reduce

from snek_advent import validate_and_return


def create_lines(line):
    base_line = [int(x) for x in [hit for hit in line.split(" ")]]
    lines = list()
    lines.append(base_line)
    while True:
        sub_line = list()
        for j in range(len(base_line) - 1):
            sub_line.append(base_line[j + 1] - base_line[j])
        lines.append(sub_line)

        if len(set(sub_line)) == 1:
            break
        base_line = sub_line
    return lines


def calculate_line(line):
    lines = create_lines(line)
    while len(lines) > 1:
        popped = lines.pop()
        lines[-1].append(lines[-1][-1] + popped[-1])
    return lines[0][-1]


def part01(lines):
    return validate_and_return(
        1987402313, (reduce(lambda x, y: x + y, map(calculate_line, lines)))
    )


def calculate_line_part2(line):
    lines = create_lines(line)

    while len(lines) > 1:
        popped = lines.pop()
        lines[-1].insert(0, lines[-1][0] - popped[0])
    return lines[0][0]


def part02(lines):
    return validate_and_return(
        900, reduce(lambda x, y: x + y, map(calculate_line_part2, lines))
    )
