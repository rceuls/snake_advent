import fileinput


def as_string():
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    return "\n".join(lines)
