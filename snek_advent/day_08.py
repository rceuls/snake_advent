from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit


class TravelNode:
    def __init__(self, line, is_part_one):
        self.right = None
        self.left = None
        self.home_label = line[0:3]
        self.home_end_label = line[2:3]
        self.left_label = line[7:10]
        self.right_label = line[12:15]
        self.until_end = None
        if is_part_one:
            self.is_end_node = self.home_label == "ZZZ"
        else:
            self.is_end_node = self.home_end_label == "Z"

    def set_nodes(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.home_label} -> [{self.until_end}]"

    def __eq__(self, other):
        return other.home_label == self.home_label

    def __hash__(self):
        return hash(self.home_label)


def get_next_node(other_nodes, move, current_node):
    return other_nodes[
        (current_node.left_label if move == "L" else current_node.right_label)
    ]


def traverse(next_move, current_node):
    return current_node.right if next_move == "R" else current_node.left


def traverse_until_end(moves, current_node):
    current_node_traversing = current_node
    count = 0
    while True:
        for move in moves:
            current_node_traversing = traverse(move, current_node_traversing)
            count += 1
            if current_node_traversing.is_end_node:
                current_node.until_end = (count, current_node_traversing)
                return current_node_traversing


def calculate_lcm(arr):
    lcm = arr[0]
    for i in range(1, len(arr)):
        num1 = lcm
        num2 = arr[i]
        gcd = 1
        # Finding GCD using Euclidean algorithm
        while num2 != 0:
            temp = num2
            num2 = num1 % num2
            num1 = temp
        gcd = num1
        lcm = (lcm * arr[i]) // gcd
    return lcm


def part02(lines):
    nodes = [TravelNode(x, False) for x in lines[2:]]
    nodes_dict = {node.home_label: node for node in nodes}
    for node in nodes:
        node.set_nodes(nodes_dict[node.left_label], nodes_dict[node.right_label])

    for node in [n for n in nodes if n.home_end_label == "A"]:
        traverse_until_end(lines[0], node)

    return calculate_lcm([n.until_end[0] for n in nodes if n.home_end_label == "A"])


def part01(lines):
    nodes = [TravelNode(x, True) for x in lines[2:]]
    nodes_dict = {node.home_label: node for node in nodes}
    for node in nodes:
        node.set_nodes(nodes_dict[node.left_label], nodes_dict[node.right_label])
    traverse_until_end(lines[0], nodes_dict["AAA"])
    return nodes_dict["AAA"].until_end[0]


def do(iterations, lines, do_profile=False):
    if iterations > 0:
        total_time = timeit(lambda: part01(lines), number=iterations, globals=globals())
        print(
            f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        )

        total_time = timeit(lambda: part02(lines), number=iterations, globals=globals())
        print(
            f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
        )

    with Profile() as profile:
        print(f"{part01(lines) = } (should be 12169)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
    with Profile() as profile:
        print(f"{part02(lines) = } (should be 12030780859469)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
