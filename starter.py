from cProfile import Profile
from pstats import Stats

from snek_advent.day_01 import do as day01_do
from snek_advent.day_02 import do as day02_do
from snek_advent.day_03 import do as day03_do

iterations = 0
run_everything = True
do_profile = False

with Profile() as profile:
    if run_everything:
        with open("./resx/day01.txt", "r") as f:
            print("🧝‍♀️🧝‍♀️🧝‍♀️ day 01 🧝‍♀️🧝‍♀️🧝‍♀️")
            day01_do(iterations, f.readlines(), do_profile)
    if run_everything:
        print("🎅🎅🎅 day 02 🎅🎅🎅")
        with open("./resx/day02.txt", "r") as f:
            day02_do(iterations, f.readlines(), do_profile)
    if run_everything:
        print("☃️☃️☃️ day 03 ☃️☃️☃️")
        with open("./resx/day03.txt", "r") as f:
            day03_do(iterations, f.readlines(), do_profile)

    print(f"\nTotal runtime {Stats(profile).get_stats_profile().total_tt} seconds")
