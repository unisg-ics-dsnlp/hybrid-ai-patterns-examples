"""Pattern 7: Division by Competence.

The RULES decide every case they can (true or false). Only the cases
the rules leave open go to the model. The model's answer is an
assessment, not a fact, and a person makes the final decision.
"""

from llm import ask_json
from world import car_world

# What the owners told us (free text the rules cannot use).
notes = {
    "golf": "Runs great.",
    "beetle": "Brakes failed at the last inspection.",
    "tesla": "Yesterday the brakes made a loud grinding noise when I stopped.",
}

with car_world() as framex:
    for car, note in notes.items():
        # 1. The rules decide what they can.
        if framex.query(f"?- {car}:Drivable.")["status"] == "true":
            print(f"{car:7} RULES decide: drivable")
        elif framex.query(f"?- {car}:NotDrivable.")["status"] == "true":
            print(f"{car:7} RULES decide: not drivable")
        else:
            # 2. The rules cannot decide: hand the case to the model.
            assessment = ask_json(f"""The owner of a car says: "{note}"
Should this car be driven? Return JSON:
{{"assessment": "probably drivable" or "probably not drivable" or "unclear", "reason": "..."}}""")
            print(f"{car:7} rules cannot decide -> MODEL assesses: "
                  f"{assessment['assessment']} ({assessment['reason']})")
            # 3. The assessment is not a fact. A person decides.
            print(f"{'':7} -> sent to a mechanic for the final decision.")
