"""Pattern 9: Model as Critic of the Rules.

The model REVIEWS our rules against the policy text they should implement.
A remark counts only if it quotes the policy exactly. A finding opens a
review for a person. The model never changes a rule.
"""

from llm import ask_json, STRONG_MODEL
from world import car_world, WORLD_FILE

policy = ("A car may be driven if it has 4 wheels, a steering wheel and working brakes. "
          "It also needs a valid inspection sticker.")

# The rules under review: the "Drivable" rule from car_world.fx.
rules = [line for line in WORLD_FILE.read_text().splitlines() if line.startswith("?C:Drivable")]
print("Rule under review:", rules[0])

# 1. The model criticises the rules.
remarks = ask_json(f"""Policy text: "{policy}"
FrameX rule: {rules[0]}

Does the rule implement the policy correctly? List every problem.
Return JSON: [{{"quote": "<exact words from the policy>", "remark": "..."}}]
Return [] if the rule is correct.""", model=STRONG_MODEL)

with car_world() as framex:
    # 2. The host measures: is the quote really in the policy?
    for i, r in enumerate(remarks):
        found = "true" if r["quote"] in policy else "false"
        framex.add(source=f"remark{i}:Remark[quoteFound -> {found}].")

    # 3. The rules decide which remarks become findings for a person.
    for i, r in enumerate(remarks):
        is_finding = framex.query(f"?- remark{i}:Finding.")["status"] == "true"
        label = "FINDING for the reviewer" if is_finding else "DROPPED (quote not in policy)"
        print(f"\n{label}\n  quote:  {r['quote']}\n  remark: {r['remark']}")

    # 4. The rules themselves are unchanged.
    print("\nRules unchanged. Is the golf still drivable?",
          framex.query("?- golf:Drivable.")["status"])
