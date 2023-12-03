from cProfile import Profile
from datetime import datetime
from pstats import Stats

from snek_advent.day_01 import do as day01_do
from snek_advent.day_02 import do as day02_do
from snek_advent.day_03 import do as day03_do
from snek_advent.day_04 import do as day04_do

iterations = 100
run_everything = False
day = datetime.now().day
do_profile = False

with Profile() as profile:
    if run_everything or day == 1:
        print("☃️☃️☃️ day 01 ☃️☃️☃️")
        with open("./resx/day01.txt", "r") as f:
            day01_do(iterations, f.readlines(), do_profile)
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
        with open("./resx/day4.txt", "r") as f:
            day04_do(iterations, f.readlines(), do_profile)

    print(f"\nTotal runtime {Stats(profile).get_stats_profile().total_tt} seconds")
