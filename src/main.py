"""Run one of the ten Hybrid AI pattern examples.

    uv run src/main.py       shows a menu
    uv run src/main.py 4     runs pattern 4 directly
"""

import runpy
import sys
from pathlib import Path

SRC = Path(__file__).parent
patterns = sorted(SRC.glob("[0-9][0-9]_*/pattern_*.py"))

if len(sys.argv) > 1:
    choice = sys.argv[1]
else:
    print("Hybrid AI patterns on one car world:\n")
    for number, path in enumerate(patterns, start=1):
        print(f"  {number:2}  {path.parent.name[3:].replace('_', ' ')}")
    choice = input("\nWhich pattern? ")

path = patterns[int(choice) - 1]
print(f"\n=== Pattern {choice}: {path.parent.name[3:].replace('_', ' ')} ===\n")
runpy.run_path(str(path), run_name="__main__")
