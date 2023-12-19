import heapq

from snek_advent import validate


def do_stuff(min_steps, max_steps, field):
    q = [(field[(1, 0)], (1, 0), (1, 0), 0), (field[(0, 1)], (0, 1), (0, 1), 0)]
    visited, end = set(), max(field)
    while q:
        heat, (x, y), (dx, dy), steps = heapq.heappop(q)
        if (x, y) == end and min_steps <= steps:
            return heat
        if ((x, y), (dx, dy), steps) in visited:
            continue
        visited.add(((x, y), (dx, dy), steps))
        if steps < (max_steps - 1) and (x + dx, y + dy) in field:
            s_pos = (x + dx, y + dy)
            heapq.heappush(q, (heat + field[s_pos], s_pos, (dx, dy), steps + 1))
        if min_steps <= steps:
            lx, ly, rx, ry = dy, -dx, -dy, dx
            l_pos, r_pos = (x + lx, y + ly), (x + rx, y + ry)
            for xx, yy, pos in zip((lx, rx), (ly, ry), (l_pos, r_pos)):
                if pos in field:
                    heapq.heappush(q, (heat + field[pos], pos, (xx, yy), 0))


def part01(lines: list[str]):
    field = {(x, y): int(n) for y, line in enumerate(lines) for x, n in enumerate(line)}
    validate(do_stuff(0, 3, field), 1023)


def part02(lines: list[str]):
    field = {(x, y): int(n) for y, line in enumerate(lines) for x, n in enumerate(line)}
    validate(do_stuff(3, 10, field), 0)
