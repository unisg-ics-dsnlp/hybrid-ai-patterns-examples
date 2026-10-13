"""Pattern 4: Model Proposes, Rules Dispose.

The model PROPOSES an action (here: a driving speed for the golf).
A rule ADMITS it or REFUSES it with a reason.
Only admitted actions are executed. A refusal goes back to the model.
"""

from llm import ask_json
from world import car_world, reason_why_not

situation = "I am in my Golf and late for my exam! The road is empty. There is a school on the left."
feedback = ""

for attempt in range(1, 4):  # at most 3 proposals
    # 1. The model proposes.
    proposal = ask_json(f"""You help a driver. Situation: "{situation}"
{feedback}
Propose a driving speed. Return JSON: {{"speed": <km/h as a number>, "reason": "..."}}""")
    speed = proposal["speed"]
    print(f"Attempt {attempt}: model proposes {speed} km/h ({proposal['reason']})")

    # 2. The rules dispose (rule "Admitted" in car_world.fx).
    with car_world() as framex:
        framex.add(source=f"p:Proposal[car -> golf; speed -> {speed}; zone -> schoolZone].")
        admitted = framex.query("?- p:Admitted.")["status"] == "true"
        reason = reason_why_not(framex, "p:Admitted")

    # 3. The host executes only what the rules admit.
    if admitted:
        print(f"ADMITTED: the Golf drives at {speed} km/h.\n")
        break
    print(f"REFUSED: this condition is not met: {reason}\n")
    feedback = f"Your proposal of {speed} km/h was REFUSED by the rules. Failed condition: {reason}"
else:
    print("Stopped: no admissible proposal after 3 attempts.")
