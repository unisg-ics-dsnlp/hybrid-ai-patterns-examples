"""A tiny helper to ask a language model via OpenRouter.

Every example imports `ask` from here, so the pattern code stays short.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Fast and free: used for most patterns.
FAST_MODEL = "nvidia/nemotron-3.5-lightning:free"
# Stronger and still free: used where the model must think harder
# (writing rules, proposing hypotheses, criticising rules).
STRONG_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

load_dotenv(Path(__file__).parent.parent / ".env")
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OEPNROUTER_API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def ask(prompt, model=FAST_MODEL):
    """Send one prompt to the model and return its answer as text."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    answer = (response.choices[0].message.content or "").strip()
    # Invariant 2 of the paper: every model answer is a dated observation.
    print(f"  [LLM receipt] {datetime.now():%H:%M:%S}  model={model}")
    return answer


def ask_json(prompt, model=FAST_MODEL):
    """Ask the model and parse its answer as JSON (code fences are removed)."""
    answer = ask(prompt, model)
    answer = answer.removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(answer)
