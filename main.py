import sys
sys.dont_write_bytecode = True

from solver import solve
from process import get_puzzle

import os

def main():
    src = input("> ")

    assert os.path.exists(src), f"Cannot locate image file: {src}"

    puzzle = get_puzzle(src)

    solution = solve(puzzle)
    
    for step, (src, dst) in enumerate(solution, 1):
        print(f"Step {step}: Bolt {src + 1} -> Bolt {dst + 1}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)