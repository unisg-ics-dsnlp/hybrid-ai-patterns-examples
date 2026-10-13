"""Open the shared car world (car_world.fx) in a fresh FrameX session."""

from pathlib import Path

from framex.framex import Client

WORLD_FILE = Path(__file__).parent / "car_world.fx"


def car_world():
    """Start FrameX and load the car world. Use it as: with car_world() as framex: ..."""
    framex = Client()
    framex.load(WORLD_FILE.read_text())
    return framex


def reason_why_not(framex, fact):
    """Return the first condition that blocks `fact`, e.g. '30 <= 20'."""
    # max_nodes: let the engine look a bit further than its small default.
    for node in framex.request("why_not", fact=fact, max_nodes=200)["nodes"]:
        for rule in node["rules"]:
            for blocker in rule["blockers"]:
                return blocker["condition"]
    return "no derivation found"
