from collections import OrderedDict

from snek_advent import validate


def do_hash(txt):
    curr_val = 0
    for char in txt:
        curr_val += ord(char)
        curr_val *= 17
        curr_val %= 256
    return curr_val


def part01(lines: list[str]):
    data = "".join(lines).split(",")
    mapped = map(do_hash, data)
    final_sum = sum(mapped)
    validate(final_sum, 513643)


class BoxAction:
    def __init__(self, line):
        self.raw_line = line
        self.action = "REMOVE" if line.count("-") == 1 else "REPLACE"
        (box, value) = line.split("-") if self.action == "REMOVE" else line.split("=")
        self.box = do_hash(box)
        self.focal_length = int(value) if value != "" else None
        self.lens_label = box

    def __repr__(self):
        return f"{self.raw_line} -> {self.action}: {self.value} on {self.box}"


def part02(lines: list[str]):
    data = "".join(lines).split(",")
    actions = [BoxAction(x) for x in data]
    boxes = {k: OrderedDict() for k in range(0, 256)}
    for line in data:
        action = "REMOVE" if line.count("-") == 1 else "REPLACE"
        (box, value) = line.split("-") if action == "REMOVE" else line.split("=")
        box_index = hash(box)
        match action:
            case "REMOVE":
                if box_index in boxes[box]:
                    del boxes[box_index][box]
            case "REPLACE":
                if box in boxes[box_index]:
                    boxes[box_index][box] = int(value)
                else:
                    boxes[box_index][box] = int(value)

    curr_offset = 1
    total = 0
    for k in boxes.keys():
        slot_index = 1
        for slot_key in boxes[k]:
            total += curr_offset * slot_index * boxes[k][slot_key]
            slot_index += 1
        curr_offset += 1
    validate(total, 265345)
