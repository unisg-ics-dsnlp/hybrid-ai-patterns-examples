"""Pattern 5: Rules Steer the Model.

A pre-drive checklist. The RULES decide which check comes next and when
we are done. The model only phrases the question and judges the answer.
The model never decides the next step.
"""

from llm import ask
from world import car_world

with car_world() as framex:
    while True:
        # 1. The rules decide the next step (rule "Next" in car_world.fx).
        step = framex.query("?- ?C:Next[topic -> ?T].")
        if step["status"] != "bindings":
            break  # no next check: the rules say we are done
        check, topic = step["bindings"][0]["C"], step["bindings"][0]["T"]

        # 2. The model only phrases the question.
        question = ask(f"Ask a driver one short, friendly yes/no question about: {topic}. "
                       "Return only the question.")
        answer = input(f"\n{question}\n> ")

        # 3. The model as judge: what does the answer mean?
        verdict = ask(f"""Question: "{question}"
Answer: "{answer}"
Does the answer mean yes or no? Reply with one word: YES, NO or UNCLEAR.""").upper()
        print(f"Judge: {verdict}")

        # 4. The rules decide what happens with the answer.
        if verdict == "YES":
            framex.add(source=f"{check}[answer -> yes].")
        elif verdict == "NO":
            framex.add(source=f"{check}[answer -> no].")
        else:
            print("The answer is unclear, so the rules ask the same check again.")

    # 5. The rules decide the outcome.
    failed = framex.query("?- ?C:Failed.")
    if failed["status"] == "bindings":
        print("\nDo NOT drive. Failed check:", failed["bindings"][0]["C"])
    else:
        print("\nAll checks passed. Drive safely!")
