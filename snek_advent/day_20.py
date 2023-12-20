from collections import namedtuple
from math import prod

from snek_advent import validate


class Node:
    def __init__(self, raw):
        self.raw = raw
        (label, targets) = raw.split(" -> ")
        self.node_type = (
            "FLIP_FLOP"
            if label[0] == "%"
            else "CONJUNCTION"
            if label[0] == "&"
            else "NULL"
            if label[0] == "_"
            else "START"
        )
        self.label = label[1:] if label != "broadcaster" else "broadcaster"
        self.children = targets.split(", ")
        self.current_state = 0
        self.parents = []

    def set_family(self, nodes):
        missing_nodes = []
        for node in nodes.values():
            for tgt in node.children:
                if tgt == self.label:
                    self.parents.append(tgt)
        for child in self.children:
            if child not in nodes:
                nodes[child] = Node("_" + child + " -> ")
                missing_nodes.append(nodes[child])
        return missing_nodes

    def __repr__(self):
        return f"Node({self.label} - {self.node_type})"

    def __str__(self):
        return f"Node({self.label} - {self.node_type})"


Action = namedtuple("Action", "node_label pulse")


def pulse(nodes, pulses):
    q = [Action("broadcaster", 0)]
    while q:
        node_label, state = q.pop()
        pulses[state] += 1
        node = nodes[node_label]
        if node.node_type == "FLIP_FLOP" and state == 0:
            node.current_state = 0 if node.current_state == 1 else 1
            for child in node.children:
                q.append(Action(child, node.current_state))
        elif node.node_type == "CONJUNCTION":
            to_send = 0
            for x in node.parents:
                if nodes[x].current_state == 0:
                    to_send = 1
                    break
            for child in node.children:
                q.append((child, to_send))
        elif node.node_type == "START":
            for child in node.children:
                q.append(Action(child, state))
        else:
            pass


def format_state(nodes):
    line = ""
    for node in nodes:
        line += str(node.current_state)
    return line


def part01(lines: list[str]):
    nodes_list = [Node(x) for x in lines]
    nodes = {k.label: k for k in nodes_list}
    pulses = {1: 0, 0: 0}
    full_states = set()
    for node in nodes_list:
        nodes_list += node.set_family(nodes)
    prev_pulses = pulses.copy()
    loops = 1000
    for _ in range(0, loops):
        pulse(nodes, pulses)
        state = format_state(nodes_list)
        if state in full_states:
            break
        full_states.add(state)
        prev_pulses = pulses.copy()

    division_bell = int(loops / len(full_states))
    print(
        prod(
            [
                prev_pulses[0] * division_bell,
                prev_pulses[1] * division_bell,
            ]
        )
    )
    # low : 659508123 657110090
    # high: 65711009000
    validate(0, 0)


def part02(lines: list[str]):
    validate(0, 0)
