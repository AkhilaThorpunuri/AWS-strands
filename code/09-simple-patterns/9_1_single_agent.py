"""
9.1 Single Agent
Module 9 · Simple Patterns | Read first: md/09-simple-patterns/9_1_single_agent.md

Problem: Reply politely to an angry customer review.

Run (from the repo root):
  .venv\\Scripts\\python code\\09-simple-patterns\\9_1_single_agent.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model

review = "1 star! My coffee maker arrived 4 days late and the carafe was cracked. Terrible service!"

agent = Agent(
    model=get_model(),
    system_prompt=(
        "You are a calm, empathetic customer support lead. "
        "Write a polite 3-sentence reply: acknowledge the issue, apologize without excuses, "
        "and offer a free replacement or full refund."
    ),
    callback_handler=None,
)

print(agent(f"Reply to this review:\n{review}"))

