import re

from snek_advent import validate

regex_green = re.compile(r"(\d+) (green,?;?)")
regex_red = re.compile(r"(\d+) (red,?;?)")
regex_blue = re.compile(r"(\d+) (blue,?;?)")


def part02(lines: list[str]):
    pwr_total = 0
    for super_line in lines:
        line = super_line.split(":")
        max_values = {"blue": 0, "red": 0, "green": 0}
        for _, game in enumerate(line[1].split(";")):
            for color in [x.strip() for x in game.split(",")]:
                tgt_count = int(color.split(" ")[0])
                if "blue" in color and tgt_count > max_values["blue"]:
                    max_values["blue"] = tgt_count
                elif "red" in color and tgt_count > max_values["red"]:
                    max_values["red"] = tgt_count
                elif "green" in color and tgt_count > max_values["green"]:
                    max_values["green"] = tgt_count
        pwr_total += max_values["blue"] * max_values["green"] * max_values["red"]
    validate(66681, pwr_total)


def part01_calc(line, ix):
    if (
        next((m for m in regex_red.finditer(line) if int(m.group(1)) > 12), False)
        or next((m for m in regex_green.finditer(line) if int(m.group(1)) > 13), False)
        or next(
            (m for m in regex_blue.finditer(line) if int(m.group(1)) > 14),
            False,
        )
    ):
        return ix
    return 0


def part01(lines: list[str]):
    game_count = len(lines)
    gauss_total = int(1 / 2 * (game_count * (game_count + 1)))
    ix = 0
    while ix < game_count:
        line = lines[ix]
        ix += 1
        gauss_total -= part01_calc(line, ix)

    validate(2237, gauss_total)
