from cProfile import Profile
from datetime import datetime
from pstats import Stats, SortKey
from timeit import timeit

import snek_advent.day_01 as day01
import snek_advent.day_06 as day06
import snek_advent.day_07 as day07
import snek_advent.day_08 as day08
from snek_advent.day_02 import do as day02_do
from snek_advent.day_03 import do as day03_do
from snek_advent.day_04 import do as day04_do
from snek_advent.day_05 import do as day05_do

iterations = 100
run_everything = True
day = datetime.now().day
do_profile = False


def do(part01, part02, friendly_day):
    with open(f"./resx/day{friendly_day}.txt", "r") as f:
        lines = [x.strip() for x in f.readlines()]

        if iterations > 0:
            total_time = timeit(
                lambda: part01(lines), number=iterations, globals=globals()
            )
            print(
                f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
            )

            total_time = timeit(
                lambda: part02(lines), number=iterations, globals=globals()
            )
            print(
                f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
            )

        if do_profile:
            with Profile() as profile:
                print(f"{part01(lines) = }")
                (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())

            with Profile() as profile:
                print(f"{part02(lines) = }")
                (Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())


if __name__ == "__main__":
    with Profile() as profile:
        if run_everything or day == 1:
            print("☃️☃️☃️ day 01 ☃️☃️☃️")
            do(day01.part01, day01.part02, "01")
        if run_everything or day == 2:
            print("🎅🎅🎅 day 02 🎅🎅🎅")
            with open("./resx/day02.txt", "r") as f:
                day02_do(iterations, f.readlines(), do_profile)
        if run_everything or day == 3:
            print("☃️☃️☃️ day 03 ☃️☃️☃️")
            with open("./resx/day03.txt", "r") as f:
                day03_do(iterations, f.readlines(), do_profile)
        if run_everything or day == 4:
            print("🎅🎅🎅 day 04 🎅🎅🎅")
            with open("./resx/day04.txt", "r") as f:
                day04_do(iterations, f.readlines(), do_profile)
        if run_everything or day == 5:
            print("☃️☃️☃️ day 05 ☃️☃️☃️ (sadly, no part two as it takes half an  hour)")
            with open("./resx/day05.txt", "r") as f:
                day05_do(iterations, f.read(), do_profile)
        if run_everything or day == 6:
            print("🎅🎅🎅 day 06 🎅🎅🎅")
            do(day06.part01, day06.part02, "06")
        if run_everything or day == 7:
            print("☃️☃️☃️ day 07 ☃️☃️☃️")
            do(day07.part01, day07.part02, "07")
        if run_everything or day == 8:
            print("🎅🎅🎅 day 08 🎅🎅🎅")
            do(day08.part01, day08.part02, "08")
        print(f"\nTotal runtime {Stats(profile).get_stats_profile().total_tt} seconds")
