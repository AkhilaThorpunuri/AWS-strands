"""
9.4 Human in the Loop (HITL)
Module 9 · Simple Patterns | Read first: md/09-simple-patterns/9_4_human_in_the_loop.md

Problem: Draft a customer email with an agent, but require human approval before sending.

Run (from the repo root):
  .venv\\Scripts\\python code\\09-simple-patterns\\9_4_human_in_the_loop.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model

drafter = Agent(
    model=get_model(),
    system_prompt="Draft a short, polite 3-sentence customer email offering a $25 credit for a delayed shipment.",
    callback_handler=None,
)

draft = str(drafter("Customer: Alex Rivera, Order #7712 delayed by 3 days."))
print("--- DRAFT EMAIL ---\n")
print(draft)

choice = input("\nApprove sending this email? [y/n]: ").strip().lower()
if choice == "y":
    print("✅ Email sent!")
else:
    print("🛑 Cancelled — email was not sent.")

