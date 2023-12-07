from cProfile import Profile
from enum import Enum, IntEnum
from functools import cmp_to_key, reduce, total_ordering
from itertools import groupby
from pstats import Stats, SortKey
from timeit import timeit


key_resolver = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


key_resolver_joker = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class MainScoreWeight(IntEnum):
    FIVE_OF_A_KIND = 8
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 6
    THREE_OF_A_KIND = 5
    TWO_PAIR = 4
    ONE_PAIR = 3
    HIGH_CARD = 2
    OTHER = 1


class Draw:
    def __init__(self, hand, wager, main_score, resolver):
        self.hand = hand
        self.wager = int(wager)
        self.main_score = main_score
        self.sub_score = [resolver[x] for x in hand]
        if "J" in hand:
            print(str(self))

    def __str__(self) -> str:
        return f"{''.join(self.hand)} ({self.wager})\t{self.main_score.name}\t{self.sub_score}"


def compare_draws(first, second):
    if first.main_score < second.main_score:
        return -1
    elif first.main_score > second.main_score:
        return 1
    else:
        for ix in range(len(first.sub_score)):
            if first.sub_score[ix] < second.sub_score[ix]:
                return -1
            elif first.sub_score[ix] > second.sub_score[ix]:
                return 1
    return 0


def as_draw(counts, raw_hand, wager, resolver):
    if 5 in counts:
        return Draw(raw_hand, wager, MainScoreWeight.FIVE_OF_A_KIND, resolver)
    elif 4 in counts:
        return Draw(raw_hand, wager, MainScoreWeight.FOUR_OF_A_KIND, resolver)
    elif 3 in counts and 2 in counts:
        return Draw(raw_hand, wager, MainScoreWeight.FULL_HOUSE, resolver)
    elif 3 in counts:
        return Draw(raw_hand, wager, MainScoreWeight.THREE_OF_A_KIND, resolver)
    elif len([x for x in counts if x == 2]) == 2:
        return Draw(raw_hand, wager, MainScoreWeight.TWO_PAIR, resolver)
    elif 2 in counts:
        return Draw(raw_hand, wager, MainScoreWeight.ONE_PAIR, resolver)
    elif len(counts) == 5:
        return Draw(raw_hand, wager, MainScoreWeight.HIGH_CARD, resolver)
    else:
        return Draw(raw_hand, wager, MainScoreWeight.OTHER, resolver)


def group_cards(raw_hand):
    hand = sorted(raw_hand)
    amounts = [{x: len(list(y))} for x, y in groupby(hand)]
    base = {}
    for l in amounts:
        base.update(l)
    return base


def parse(draw):
    (raw_hand, wager) = draw.strip().split(" ")
    grouped = group_cards(raw_hand)
    counts = grouped.values()
    resolver = key_resolver
    return as_draw(counts, raw_hand, wager, resolver)


def parse_joker(draw):
    (raw_hand, wager) = draw.strip().split(" ")
    grouped = group_cards(raw_hand)
    counts = grouped.values()
    resolver = key_resolver_joker
    joker_count = grouped["J"] if "J" in grouped else 0
    if joker_count != 0:
        other_vals = []
        for l in grouped.keys():
            if l != "J":
                other_vals.append((l, grouped[l]))

        if joker_count == 5:
            return Draw(raw_hand, wager, MainScoreWeight.FIVE_OF_A_KIND, resolver)
        maximum_count = max(grouped.values())

        # print(raw_hand, "->", other_vals, " (", joker_count, ")")
        for key in grouped.keys():
            if maximum_count == grouped[key]:
                updated_hand = raw_hand.replace("J", key)
                updated_grouped = group_cards(updated_hand)
                return as_draw(
                    updated_grouped.values(),
                    raw_hand,
                    wager,
                    resolver,
                )

    else:
        return as_draw(counts, raw_hand, wager, resolver)


def part01(lines):
    draws = [parse(l) for l in lines]
    sorted_draws = sorted(draws, key=cmp_to_key(compare_draws))
    total = 0
    for ix in range(0, len(sorted_draws)):
        total += (ix + 1) * sorted_draws[ix].wager
    return total


def part02(lines):
    draws = [parse_joker(l) for l in lines]
    sorted_draws = sorted(draws, key=cmp_to_key(compare_draws))
    total = 0
    for ix in range(0, len(sorted_draws)):
        total += (ix + 1) * sorted_draws[ix].wager
    return total
    # 251971761
    # 251855847
    # 252366738 too high


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

    # with Profile() as profile:
    #     print(f"{part01(lines) = } (should be 250370104)")
    #     if do_profile:
    #         (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

    with Profile() as profile:
        print(f"{part02(lines) = } (should be 46173809)")
        if do_profile:
            (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
