from cProfile import Profile
from enum import IntEnum
from functools import total_ordering
from itertools import groupby
from multiprocessing import Pool
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


#
# def group_cards(raw_hand):
#     hand = sorted(raw_hand)
#     amounts = [{x: len(list(y))} for x, y in groupby(hand)]
#     base = {}
#     for l in amounts:
#         base.update(l)
#     return base
def group_cards(target):
    return {key: len(list(value)) for key, value in groupby(sorted(target))}


@total_ordering
class Draw:
    def __init__(self, hand, wager, resolver, orig_hand):
        self.hand = hand
        self.wager = int(wager)
        self.sub_score = [resolver[x] for x in orig_hand]
        self.main_score = self.get_main_score()

    def get_main_score(self):
        counts = group_cards(self.hand).values()
        if len(counts) == 5:
            return MainScoreWeight.HIGH_CARD
        elif 5 in counts:
            return MainScoreWeight.FIVE_OF_A_KIND
        elif 4 in counts:
            return MainScoreWeight.FOUR_OF_A_KIND
        elif 3 in counts and 2 in counts:
            return MainScoreWeight.FULL_HOUSE
        elif 3 in counts:
            return MainScoreWeight.THREE_OF_A_KIND
        elif len([x for x in counts if x == 2]) == 2:
            return MainScoreWeight.TWO_PAIR
        elif 2 in counts:
            return MainScoreWeight.ONE_PAIR
        else:
            return MainScoreWeight.OTHER

    def __str__(self) -> str:
        return f"{''.join(self.hand)} ({self.wager})\t{self.main_score.name}\t{self.sub_score}"

    def __eq__(self, other):
        return self.main_score == other.main_score and self.sub_score == other.sub_score

    def __lt__(self, other):
        if self.main_score > other.main_score:
            return False
        elif self.main_score < other.main_score:
            return True
        else:
            for ix in range(0, 5):
                if self.sub_score[ix] > other.sub_score[ix]:
                    return False
                if self.sub_score[ix] < other.sub_score[ix]:
                    return True
        return True


def parse(draw):
    raw_hand = draw[0:5]
    wager = draw[6:]
    return Draw(raw_hand, wager, key_resolver, raw_hand)


def parse_joker(draw):
    raw_hand = draw[0:5]
    wager = draw[6:]
    joker_count = raw_hand.count("J")
    if joker_count == 5:
        return Draw(
            raw_hand,
            wager,
            key_resolver_joker,
            raw_hand,
        )
    elif joker_count != 0:
        other_vals = group_cards(raw_hand.replace("J", "")).copy()

        maximum_count = max(other_vals.values())

        inverse_map = {v: k for k, v in other_vals.items()}

        updated_hand = raw_hand.replace("J", inverse_map[maximum_count])
        return Draw(
            updated_hand,
            wager,
            key_resolver_joker,
            raw_hand,
        )

    else:
        return Draw(raw_hand, wager, key_resolver_joker, raw_hand)


def part01(lines):
    with Pool() as pool:
        draws = pool.map(parse, lines)
        sorted_draws = sorted(draws)
        total = 0
        for ix in range(0, 1000):
            total += (ix + 1) * sorted_draws[ix].wager
        return total


def part02(lines):
    with Pool() as pool:
        draws = pool.map(parse_joker, lines)
        sorted_draws = sorted(draws)
        total = 0
        for ix in range(0, 1000):
            total += (ix + 1) * sorted_draws[ix].wager
        return total


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

    if iterations == 0:
        with Profile() as profile:
            print(f"{part01(lines) = } (should be 250370104)")
            if do_profile:
                (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

        with Profile() as profile:
            print(f"{part02(lines) = } (should be 251735672)")
            if do_profile:
                (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
