import pathlib
import numpy as np
import scipy.optimize as opt

# Day 10 part 2 - did in python so I could use scipy to solve it
# I'm getting tired so I'm probably not cleaning this up, you'll be ok.
def main():
    base = pathlib.Path(__file__).parent.parent
    #filename = base / "inputs" / "day10" / "sample.txt"
    filename = base / "inputs" / "day10" / "input.txt"

    with open(filename, "r") as f:
        lines = f.readlines()
    machines = []
    pushes = 0
    for line in lines:
        p = line.strip().split(" ")
        *buttons, joltage_goal = p[1:-1], p[-1]
        #print(buttons, joltage_goal)
        parsed_buttons = [list(map(int, s.strip("()").split(","))) for s in buttons[0]]
        #print(parsed_buttons)
        parsed_joltage_goal = list(map(int, joltage_goal.strip("{}").split(",")))
        #print(parsed_joltage_goal)
        num_buttons = len(parsed_buttons)
        num_jolts = len(parsed_joltage_goal)
        a = np.zeros((num_jolts, num_buttons))
        # need to put 1s in the a matrix for the buttons that are used to get to the next joltage
        for idx, parsed_button in enumerate(parsed_buttons):
            for idx2 in parsed_button:
                a[idx2, idx] = 1
        
        b = np.zeros(num_jolts)
        for idx, joltage in enumerate(parsed_joltage_goal):
            b[idx] = joltage
        #print(a)
        #print(b)
        x = np.ones(num_buttons)
        const = opt.LinearConstraint(a, b, b)
        bounds = opt.Bounds(0, np.inf)
        ints = np.ones(num_buttons)
        result = opt.milp(c=x, constraints=const, bounds=bounds, integrality=ints)
        #print(result.x)
        pushes += sum(result.x)
    print("Part 2: ", int(pushes))


if __name__ == "__main__":
    main()
