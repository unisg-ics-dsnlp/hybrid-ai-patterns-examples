"""Pattern 6: Critique and Repair.

The model writes a FrameX fact. A checker tests it. If it fails, the
checker says WHAT is wrong and the model tries again, with its faulty
answer and the problem in the prompt. At most 3 attempts, and we stop
when the model repeats itself.
"""

from framex.framex import FrameXError
from llm import ask
from world import car_world

task = "Add my bicycle: its name is bike, it is a Vehicle and it has 2 wheels."
prompt = f"Write one FrameX (F-Logic) fact for this: {task}\nReturn only the code."
feedback = ""
previous = None

for attempt in range(1, 4):
    code = ask(prompt + feedback).strip("` \n")
    print(f"Attempt {attempt}: {code}")

    if code == previous:
        print("Same answer as before: the repair is stuck. Stop.")
        break
    previous = code

    # 1. The checker classifies the problem.
    with car_world() as framex:
        try:
            framex.add(source=code)
            if framex.query("?- bike:Vehicle.")["status"] != "true":
                problem = "The fact does not make bike a Vehicle."
            elif framex.query("?- bike[wheels -> 2].")["status"] != "true":
                problem = "bike has no slot wheels with the number 2. Use exactly: wheels -> 2"
            else:
                problem = None
        except FrameXError as error:
            problem = f"Syntax error: {error.error['message']} (column {error.error['column']})."

    if problem is None:
        print("ACCEPTED: the fact passes every check.")
        break

    # 2. Name the problem AND the fix, then ask again.
    print(f"REJECTED: {problem}\n")
    feedback = (f"\n\nYour previous answer was:\n{code}\nIt was rejected: {problem}\n"
                "Hint: a FrameX fact looks like  object:Class[slot -> value; slot -> value].\n"
                "Slots are separated by ; and the fact ends with a dot.")
else:
    print("Stopped after 3 attempts.")
