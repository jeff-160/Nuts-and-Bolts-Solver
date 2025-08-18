import sys
sys.dont_write_bytecode = True

from solver import solve
from process import get_puzzle

import os

def get_solution(src):
    assert os.path.exists(src), f"Cannot locate image file: {src}"

    puzzle = get_puzzle(src)
    solution = solve(puzzle)

    return puzzle, solution

def main():
    assert len(sys.argv) > 1, "Puzzle image not supplied"

    puzzle, solution = get_solution(sys.argv[1])

    print("Puzzle:", puzzle)

    if solution:
        for step, (src, dst) in enumerate(solution, 1):
            print(f"Step {step}: Bolt {src + 1} -> Bolt {dst + 1}")
    else:
        print("No solution found!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)