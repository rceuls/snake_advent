import snek_advent.day_01 as day01
from snek_advent.input import as_lines
from datetime import datetime

lines = as_lines()
start=datetime.now()
day01.part01(lines) #54597
print("part1:\t", datetime.now() - start)

start=datetime.now()
day01.part02(lines) #54504
print("part2:\t", datetime.now() - start)
