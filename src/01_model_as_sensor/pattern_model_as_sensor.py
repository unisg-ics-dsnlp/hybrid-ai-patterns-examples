"""Pattern 1: Model as Sensor.

The model READS a text that the rules cannot read and proposes facts.
Each proposal must come with a verbatim quote. The rules accept a
proposal only if its quote really occurs in the text.
"""

from llm import ask_json
from world import car_world

# 1. Free text: the rules cannot read this, the model can.
text = "Workshop report: We checked the Tesla today. The brakes work fine."

# 2. The model acts as a sensor: it turns the text into proposed facts.
readings = ask_json(f"""Read this text about a car:
"{text}"

Return JSON with exactly these two keys:
  "brakes": "ok" or "broken"
  "wheels": a number
For each key give {{"value": ..., "quote": "<the exact words from the text>"}}.
If the text does not say it, use {{"value": "unknown", "quote": ""}}.
Return only the JSON.""")
print("The model proposes:", readings)

with car_world() as framex:
    print("\nBefore: is the tesla drivable?", framex.query("?- tesla:Drivable.")["status"])

    # 3. The host only MEASURES: does the quote really occur in the text?
    for slot, reading in readings.items():
        value = str(reading["value"]).lower()
        if value == "unknown":
            continue  # the text does not say it, so there is nothing to propose
        quote_found = "true" if reading["quote"] and reading["quote"] in text else "false"
        framex.add(source=f"r_{slot}:Reading[car -> tesla; slot -> {slot}; "
                          f"value -> {value}; quoteFound -> {quote_found}].")

    # 4. The RULES decide which readings become facts (see car_world.fx).
    print("Accepted readings:", framex.query("?- ?R:Accepted.").get("bindings"))
    print("After:  is the tesla drivable?", framex.query("?- tesla:Drivable.")["status"])
    print("\nWhy?\n" + framex.explain("tesla:Drivable"))
