from collections import namedtuple
from math import prod, lcm

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
        self.memory = {}

    def set_family(self, nodes):
        missing_nodes = []
        for node in nodes.values():
            for tgt in node.children:
                if tgt == self.label:
                    self.memory[node.label] = 0
        for child in self.children:
            if child not in nodes:
                nodes[child] = Node("_" + child + " -> ")
                missing_nodes.append(nodes[child])
        return missing_nodes

    def __repr__(self):
        return f"Node({self.label} - {self.node_type})"

    def __str__(self):
        return f"Node({self.label} - {self.node_type})"


Action = namedtuple("Action", "target pulse sender")


def pulse(nodes, pulses):
    q = [Action("broadcaster", 0, "")]
    historic_pulses = []
    while q:
        target, state, sender = q.pop(0)
        historic_pulses.append(Action(target, state, sender))
        pulses[state] += 1
        node = nodes[target]

        if node.node_type == "FLIP_FLOP" and state == 0:
            node.current_state = 0 if node.current_state == 1 else 1
            for child in node.children:
                q.append(Action(child, node.current_state, target))
        elif node.node_type == "CONJUNCTION":
            node.memory[sender] = state
            to_send = 0 if all(node.memory.values()) else 1
            for child in node.children:
                q.append((child, to_send, target))
        elif node.node_type == "START":
            for child in node.children:
                q.append(Action(child, state, target))
        else:
            pass
    return historic_pulses


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
        prev_pulses = pulses.copy()
        pulse(nodes, pulses)
        state = format_state(nodes_list)
        if state in full_states:
            break
        full_states.add(state)
        prev_pulses = pulses.copy()

    division_bell = int(loops / len(full_states))
    validate(
        prod(
            [
                prev_pulses[0] * division_bell,
                prev_pulses[1] * division_bell,
            ]
        ),
        883726240,
    )


def part02(lines: list[str]):
    nodes_list = [Node(x) for x in lines]
    nodes = {k.label: k for k in nodes_list}
    pulses = {1: 0, 0: 0}
    loops = 0
    first_high_pulse = {}
    for node in nodes_list:
        nodes_list += node.set_family(nodes)
        for ch in node.children:
            if ch == "bb":
                first_high_pulse[node.label] = 0

    while not all(first_high_pulse.values()):
        loops += 1
        loop_pulses = pulse(nodes, pulses)
        for p in loop_pulses:
            if (
                p.pulse == 1
                and p.sender in first_high_pulse
                and not first_high_pulse[p.sender]
            ):
                first_high_pulse[p.sender] = loops
    validate(lcm(*first_high_pulse.values()), 211712400442661)
