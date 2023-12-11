from snek_advent import validate


def calculate_lcm(arr):
    lcm = arr[0]
    for i in range(1, len(arr)):
        num1 = lcm
        num2 = arr[i]
        gcd = 1
        while num2 != 0:
            temp = num2
            num2 = num1 % num2
            num1 = temp
        gcd = num1
        lcm = (lcm * arr[i]) // gcd
    return lcm


def traverse_dictionary(moves, lookups, label):
    count = 0
    while True:
        for move in moves:
            label = (
                lookups[label]["right_label"]
                if move == "R"
                else lookups[label]["left_label"]
            )
            count += 1
            if lookups[label]["is_end_node"]:
                return count


def convert_to_node(line, is_part_one):
    is_end = line[0:3] == "ZZZ" if is_part_one else line[2:3] == "Z"
    is_start = line[0:3] == "AAA" if is_part_one else line[2:3] == "A"
    return {
        "home_label": line[0:3],
        "left_label": line[7:10],
        "right_label": line[12:15],
        "is_end_node": is_end,
        "is_start_node": is_start,
    }


def part02(lines):
    nodes = [convert_to_node(x, False) for x in lines[2:]]
    nodes_dict = {node["home_label"]: node for node in nodes}

    target_labels = [n for n in nodes if n["is_start_node"]]
    distances = []

    for node in target_labels:
        distances.append(traverse_dictionary(lines[0], nodes_dict, node["home_label"]))

    validate(12030780859469, calculate_lcm(distances))


def part01(lines):
    nodes = [convert_to_node(x, True) for x in lines[2:]]
    nodes_dict = {node["home_label"]: node for node in nodes}
    validate(12169, traverse_dictionary(lines[0], nodes_dict, "AAA"))
