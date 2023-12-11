import importlib
from datetime import datetime
from timeit import timeit

dev_mode = True
iterations = 100
run_everything = True
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
    if dev_mode:
        iterations = 1
        run_everything = False

    module_names = [f"{x:02d}" for x in range(1 if dev_mode else day + 1)]
    print(module_names)

    for mod_name in module_names:
        module = importlib.import_module(f"snek_advent.day_{mod_name}")
        match mod_name:
            case "03":
                do(module.part01, module.part02, "03", strip_lines=False)
            case "05":
                do(module.part01, module.part01, "05", full_read=True)
            case "10":
                do(module.part01, module.part02, "10", iterations_override=10)
            case _:
                do(module.part01, module.part02, mod_name)
