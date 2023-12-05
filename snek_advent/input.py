import fileinput


def as_lines():
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    return lines
