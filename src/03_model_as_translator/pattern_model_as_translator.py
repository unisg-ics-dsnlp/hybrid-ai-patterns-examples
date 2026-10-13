"""Pattern 3: Model as Translator.

The model stands between a person and the rules, in both directions:
  question in words -> FrameX query -> answer + proof -> answer in words.
The RULES decide. The model only translates.
"""

from llm import ask
from world import car_world

question = "Hey, can I take my Beetle for a drive today?"
print("Person asks:", question)

# 1. Words -> query. The model only gets the vocabulary, not the decision.
query = ask(f"""Translate the question into ONE FrameX query.
Known cars: golf, beetle, tesla. Known class: Drivable.
Example query: ?- golf:Drivable.
Question: "{question}"
Return only the query.""").strip("` \n")
print("Model's query:", query)

# 2. The rules answer, with a proof.
with car_world() as framex:
    verdict = framex.query(query)["status"]
    car = query.removeprefix("?-").split(":")[0].strip()
    if verdict == "true":
        proof = framex.explain(f"{car}:Drivable")
    else:  # the proof of the opposite, if the rules have one
        proof = framex.explain(f"{car}:NotDrivable")
print("Rules say:", verdict)

# 3. Answer + proof -> words for the person.
reply = ask(f"""A person asked: "{question}"
The rule engine answered: {verdict}
The proof: {proof}
Answer the person in one or two friendly sentences.
Start with YES or NO, matching the rule engine. Give only the reason from the proof.""")
print("\nModel replies:", reply)

# 4. The host checks that the reply uses the decision word of the rules.
expected_word = "YES" if verdict == "true" else "NO"
print("Reply matches the rules?", reply.upper().startswith(expected_word))
