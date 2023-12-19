from functools import partial

from snek_advent import validate


def smaller(wf_item, label, outcome, value):
    return outcome if wf_item > value[label] else None


def bigger(wf_item, label, outcome, value):
    return outcome if wf_item < value[label] else None
g

class Workflow:
    def __init__(self, raw):
        self.raw = raw
        self.label = raw.split("{")[0]
        raw_predicates = raw[len(self.label) : -1].split(",")
        predicates = []
        for p in raw_predicates[0:-1]:
            (predicate, outcome) = p.replace("{", "}").replace("}", "").split(":")
            op = "<" if "<" in predicate else ">"
            (target, value) = predicate.split(op)
            if op == "<":
                predicates.append(partial(smaller, int(value), target, outcome))
            else:
                predicates.append(partial(bigger, int(value), target, outcome))
        self.predicates = predicates
        self.default = raw_predicates[-1]

    def apply(self, part):
        for predicate in self.predicates:
            res = predicate(part)
            if res is not None:
                return res
        return self.default


def to_machine_part(line):
    relevant = line[1:-1]
    (x, m, a, s) = relevant.split(",")
    return {
        "x": int(x.split("=")[1]),
        "m": int(m.split("=")[1]),
        "a": int(a.split("=")[1]),
        "s": int(s.split("=")[1]),
    }


def handle(machine_part, workflows, starter):
    new_flow = starter.apply(machine_part)
    while True:
        if new_flow == "A":
            return (
                machine_part["x"]
                + machine_part["m"]
                + machine_part["a"]
                + machine_part["s"]
            )
        elif new_flow == "R":
            return 0
        target_flow = workflows[new_flow]
        new_flow = target_flow.apply(machine_part)


def get_lines_and_workflows(lines):
    workflows = []
    parts = []
    in_workflows = True
    for line in lines:
        if line.strip() == "":
            in_workflows = False
        elif in_workflows:
            workflows.append(Workflow(line))
        else:
            parts.append(to_machine_part(line))

    wfd = {k.label: k for k in workflows}
    return wfd, parts


def part01(lines: list[str]):
    total = 0
    (wfd, parts) = get_lines_and_workflows(lines)
    for p in parts:
        total += handle(p, wfd, wfd["in"])

    validate(total, 263678)


def part02(lines: list[str]):
    (wfd, _) = get_lines_and_workflows(lines)

    validate(0, 0)
