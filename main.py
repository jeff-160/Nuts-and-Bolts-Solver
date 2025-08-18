import sys
sys.dont_write_bytecode = True

from solver import solve
from process import get_puzzle

import os

def get_solution(src):
    assert os.path.exists(src), f"Cannot locate image file: {src}"

    puzzle = get_puzzle(src)

    solution = solve(puzzle)
    
    steps = [f"Step {step}: Bolt {src + 1} -> Bolt {dst + 1}" for step, (src, dst) in enumerate(solution, 1)]

    return puzzle, steps

def main():
    src = input("> ")

    puzzle, steps = get_solution(src)

    print("Puzzle:", puzzle)
    print("\n".join(steps))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)