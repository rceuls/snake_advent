from collections import namedtuple
from functools import partial
from math import prod

from snek_advent import validate


def smaller(wf_item, label, outcome, value):
    return outcome if wf_item > value[label] else None


def bigger(wf_item, label, outcome, value):
    return outcome if wf_item < value[label] else None


Rule = namedtuple("Rule", "category valid_range target_wf")


class Workflow:
    def __init__(self, raw):
        self.raw = raw
        self.label = raw.split("{")[0]
        raw_predicates = raw[len(self.label) : -1].split(",")
        predicates = []
        self.ranges = []
        for p in raw_predicates[0:-1]:
            (predicate, outcome) = p.replace("{", "}").replace("}", "").split(":")
            op = "<" if "<" in predicate else ">"
            (target, value) = predicate.split(op)
            if op == "<":
                predicates.append(partial(smaller, int(value), target, outcome))
                self.ranges.append(
                    Rule(
                        valid_range=range(1, int(value)),
                        target_wf=outcome,
                        category=target,
                    )
                )
            else:
                predicates.append(partial(bigger, int(value), target, outcome))
                self.ranges.append(
                    Rule(
                        valid_range=range(int(value) + 1, 4001),
                        target_wf=outcome,
                        category=target,
                    )
                )
        # for l in "xmas":
        #     if l not in self.ranges:
        #         self.ranges[l] = range(0, 4001)
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

    # validate(total, 263678)


def update_range(d, key, value):
    new = dict()
    for k, v in d.items():
        new[k] = value if k == key else v
    return new


def part02(lines: list[str]):
    (wfd, _) = get_lines_and_workflows(lines)
    q = [("in", {c: range(1, 4001) for c in "xmas"})]
    result = 0
    while q:
        workflow_id, ranges = q.pop()
        if workflow_id == "A":
            result += prod(len(r) for r in ranges.values())
        elif workflow_id in wfd:
            workflow = wfd[workflow_id]
            for category, valid_range, target_workflow in workflow.ranges:
                new_range = range(
                    max(valid_range.start, ranges[category].start),
                    min(valid_range.stop, ranges[category].stop),
                )
                if new_range:
                    q.append(
                        (
                            target_workflow,
                            update_range(ranges, category, new_range),
                        )
                    )
                old_range_inv = (
                    range(valid_range.stop, 4001)
                    if valid_range.start <= 1
                    else range(1, valid_range.start)
                )

                old_range = range(
                    max(old_range_inv.start, ranges[category].start),
                    min(old_range_inv.stop, ranges[category].stop),
                )
                if not old_range:
                    break
                ranges[category] = old_range
            else:
                q.append((workflow.default, ranges))
    print(result)
    validate(0, 0)
