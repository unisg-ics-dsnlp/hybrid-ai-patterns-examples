"""Pattern 2: Model as Author.

The model WRITES a new rule from a policy sentence. The rule is never
used unchecked: a checker loads it into a fresh copy of the car world
and runs test cases. Only a draft that passes every test is handed to
a person, who decides whether to adopt it.
"""

from framex.framex import FrameXError
from llm import ask, STRONG_MODEL
from world import car_world

policy = "A car is roadworthy if it has 4 wheels and its brakes are ok."

# 1. The model drafts the rule. We give it a template, not a blank page.
draft = ask(f"""Translate this policy into ONE FrameX rule:
"{policy}"

FrameX example rule:
  ?X:Mortal <- ?X:Human[age -> ?A] AND ?A > 0.

Use exactly this head: ?X:Roadworthy <- ...
Available: class Car, slots wheels (a number) and brakes (ok or broken).
Return only the rule, ending with a dot.""", model=STRONG_MODEL).strip("` \n")
print("Draft rule:", draft)

# 2. Test cases, written BEFORE the draft: car -> expected answer.
tests = {"golf": "true", "beetle": "false", "tesla": "false"}

# 3. The checker: add the draft to a fresh copy of the world and run every test.
with car_world() as framex:
    try:
        framex.add(source=draft)
    except FrameXError as error:
        print("The draft does not parse:", error)
        raise SystemExit

    passed = 0
    for car, expected in tests.items():
        result = framex.query(f"?- {car}:Roadworthy.")["status"]
        passed += result == expected
        print(f"  {car:7} expected {expected:5}  got {result:5}  {'PASS' if result == expected else 'FAIL'}")

# 4. Only a person adopts a rule. The checker only recommends.
if passed == len(tests):
    print("\nAll tests pass: recommend the draft to a person for adoption.")
else:
    print(f"\nOnly {passed} of {len(tests)} tests pass: the draft is NOT adoptable.")
