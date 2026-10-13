"""Pattern 8: Model as Hypothesis Generator.

Observation: the Beetle does not start. The model PROPOSES possible
causes. The RULES test each cause in a fresh copy of the world:
does it explain the observation, and does it contradict nothing we know?
For the surviving causes, the rules name the question that decides.
A hypothesis never becomes a fact.
"""

from framex.framex import FrameXError
from llm import ask_json, STRONG_MODEL
from world import car_world

observation = "My Beetle does not start."

# 1. The model proposes possible causes.
hypotheses = ask_json(f"""A driver says: "{observation}"
Propose the 4 most likely causes.
Describe each cause with a slot and a value, for example {{"slot": "battery", "value": "empty"}}.
Slots the rules know: battery, fuel, starter, immobilizer.
Values the rules know: empty, broken, active.
Return JSON: [{{"slot": "...", "value": "..."}}, ...]""", model=STRONG_MODEL)

# 2. The rules test every hypothesis in a fresh copy of the world.
for h in hypotheses:
    guess = f"beetle[{h['slot']} -> {h['value']}]"
    with car_world() as framex:
        try:
            framex.add(source=guess + ".")  # assumed only inside this copy
        except FrameXError:
            print(f"{guess:35} DROPPED: not valid FrameX, the rules cannot test it")
            continue
        explains = framex.query("?- beetle:WontStart.")["status"] == "true"
        contradicts = framex.query("?- beetle:Contradiction.")["status"] == "true"
        question = framex.query("?- beetle[askNext -> ?Q].").get("bindings", [{}])[0].get("Q")

    if not explains:
        print(f"{guess:35} DROPPED: the rules cannot explain the observation with it")
    elif contradicts:
        print(f"{guess:35} DROPPED: contradicts what we see (fuel gauge full, lights on)")
    else:
        print(f"{guess:35} POSSIBLE -> ask: {question}")
