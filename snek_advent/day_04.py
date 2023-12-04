import re
from cProfile import Profile
from pstats import Stats, SortKey
from timeit import timeit


def calculate_win(card):
    card["total_win_count"] = 0
    card["total_win_count"] += len(card["won_cards"])
    for wc in card["won_cards"]:
        card["total_win_count"] += wc["total_win_count"]
    return card


def part02(lines):
    (_, parsed) = part01(lines)
    total = len(parsed.keys())
    all_cards = []
    for x in parsed.keys():
        target_card = parsed[x]
        target_card["won_cards"] = [
            parsed[wc + x + 1] for wc in range(0, target_card["w"])
        ]
        all_cards.append(target_card)

    for card in all_cards[::-1]:
        total += calculate_win(card)["total_win_count"]
    return total


def part01(lines):
    total = 0
    games = {}
    for ix in range(0, len(lines)):
        game_number = ix + 1
        games[game_number] = {"w": 0, "dbg": ix + 1}
        (_, game) = lines[ix].split(":")
        (winning_numbers_s, numbers_s) = game.split("|")
        winning_numbers = [
            int(x) for x in re.sub(r"\s+", " ", winning_numbers_s.strip()).split(" ")
        ]
        numbers = [int(x) for x in re.sub(r"\s+", " ", numbers_s.strip()).split(" ")]
        count = 0
        for n in numbers:
            if n in winning_numbers:
                games[game_number]["w"] += 1
                count += 1
        worth = 2 ** (count - 1) if count > 0 else 0

        total += worth
    return total, games


def part01_profiler(lines):
    return part01(lines)[0]


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
        print(f"{part01_profiler(lines) = } (should be 23941)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 5571760)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
