import fileinput


def as_string():
    return "\n".join(as_lines())


def as_lines():
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    return lines
