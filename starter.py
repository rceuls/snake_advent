from datetime import datetime
from timeit import timeit

import snek_advent.day_02 as day02
import snek_advent.day_03 as day03
import snek_advent.day_04 as day04
import snek_advent.day_05 as day05
import snek_advent.day_06 as day06
import snek_advent.day_07 as day07
import snek_advent.day_08 as day08
import snek_advent.day_09 as day09
import snek_advent.day_11 as day11

iterations = 100
run_everything = False
day = datetime.now().day


def do(
    part01,
    part02,
    friendly_day,
    strip_lines=True,
    full_read=False,
    iterations_override=None,
):
    print("**" * 5 + " running day " + friendly_day + " " + "**" * 5)
    with open(f"./resx/day{friendly_day}.txt", "r") as f:
        lines = None
        if not full_read:
            lines = [x.strip() for x in f.readlines()] if strip_lines else f.readlines()
        else:
            lines = f.read()

        if iterations > 0:
            total_time = timeit(
                lambda: part01(lines),
                number=iterations
                if iterations_override is None
                else iterations_override,
                globals=globals(),
            )
            print(
                f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
            )

            total_time = timeit(
                lambda: part02(lines),
                number=iterations
                if iterations_override is None
                else iterations_override,
                globals=globals(),
            )
            print(
                f"Average time is {total_time / iterations:.10f} seconds ({iterations} iterations)"
            )


if __name__ == "__main__":
    if run_everything or day == 1:
        import snek_advent.day_01 as day01

        do(day01.part01, day01.part02, "01")
    if run_everything or day == 2:
        do(day02.part01, day02.part02, "02")
    if run_everything or day == 3:
        do(day03.part01, day03.part02, "03", strip_lines=False)
    if run_everything or day == 4:
        do(day04.part01, day04.part02, "04")
    if run_everything or day == 5:
        print("sadly, part one executes two times as part two as it takes half an hour")
        do(day05.part01, day05.part01, "05", full_read=True)
    if run_everything or day == 6:
        do(day06.part01, day06.part02, "06")
    if run_everything or day == 7:
        do(day07.part01, day07.part02, "07")
    if run_everything or day == 8:
        do(day08.part01, day08.part02, "08")
    if run_everything or day == 9:
        do(day09.part01, day09.part02, "09")
    if run_everything or day == 10:
        import snek_advent.day_10 as day10

        do(day10.part01, day10.part02, "10", iterations_override=1)
    if run_everything or day == 11:
        do(day11.part01, day11.part02, "11")
