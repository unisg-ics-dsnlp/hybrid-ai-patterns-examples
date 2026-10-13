"""Pattern 10: Rules Teach the Model.

The RULES label example cars (with the reason from the proof). These
labelled examples go into the model's prompt. Then the model answers
new cases, and the rules grade its answers. The rules stay the check.
"""

from llm import ask
from world import car_world, reason_why_not

examples = {
    "carA": "wheels -> 4; hasSteeringWheel -> true; brakes -> ok",
    "carB": "wheels -> 4; hasSteeringWheel -> true; brakes -> broken",
    "carC": "wheels -> 3; hasSteeringWheel -> true; brakes -> ok",
    "carD": "wheels -> 4; hasSteeringWheel -> false; brakes -> ok",
}
new_cases = {
    "carE": "wheels -> 6; hasSteeringWheel -> true; brakes -> ok",
    "carF": "wheels -> 4; hasSteeringWheel -> true; brakes -> ok",
    "carG": "wheels -> 4; hasSteeringWheel -> false; brakes -> broken",
}

with car_world() as framex:
    for car, slots in {**examples, **new_cases}.items():
        framex.add(source=f"{car}:Car[{slots}].")

    def label(car):
        return framex.query(f"?- {car}:Drivable.")["status"]

    # 1. The rules label the examples, with the reason from the proof.
    lesson = ""
    for car, slots in examples.items():
        if label(car) == "true":
            reason = "all conditions met"
        else:
            reason = f"missing: {reason_why_not(framex, f'{car}:Drivable')}"
        lesson += f"Car [{slots}] -> drivable: {label(car)} ({reason})\n"
    print("Lesson written by the rules:\n" + lesson)

    # 2. The model answers new cases, with the lesson in its prompt.
    # 3. The rules grade every answer.
    score = 0
    for car, slots in new_cases.items():
        answer = ask(f"""Examples labelled by our rules:
{lesson}
Car [{slots}] -> drivable? Answer only true or false.""").lower()
        correct = label(car)
        score += answer == correct
        print(f"{car}: model says {answer:5}  rules say {correct:5}  {'RIGHT' if answer == correct else 'WRONG'}")
    print(f"\nScore: {score} of {len(new_cases)}")
