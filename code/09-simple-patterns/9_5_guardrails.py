"""
9.5 Guardrails
Module 9 · Simple Patterns | Read first: md/09-simple-patterns/9_5_guardrails.md

Problem: Ensure a product description is under 35 words and includes the exact price '$49'.

Run (from the repo root):
  .venv\\Scripts\\python code\\09-simple-patterns\\9_5_guardrails.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model


def validate_blurb(text: str, price: str = "$49", max_words: int = 35) -> list[str]:
    errors = []
    words = text.split()
    if len(words) > max_words:
        errors.append(f"Too long ({len(words)} words; max {max_words}).")
    if price not in text:
        errors.append(f"Missing required price '{price}'.")
    return errors


agent = Agent(
    model=get_model(),
    system_prompt="You write punchy product descriptions.",
    callback_handler=None,
)

prompt = "Write a product blurb for a compact USB-C travel charger priced at $49. Keep it under 35 words."
for attempt in range(1, 4):
    blurb = str(agent(prompt)).strip()
    issues = validate_blurb(blurb)
    if not issues:
        print(f"Attempt {attempt}: Passed! ({len(blurb.split())} words)\n")
        print(blurb)
        break
    print(f"Attempt {attempt} failed: {issues}")
    prompt = f"Fix these issues in your previous draft: {' '.join(issues)}"

