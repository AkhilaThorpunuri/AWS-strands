"""
9.2 Multi-Agent Relay
Module 9 · Simple Patterns | Read first: md/09-simple-patterns/9_2_multi_agent.md

Problem: Turn messy meeting notes into a clean team update email.

Run (from the repo root):
  .venv\\Scripts\\python code\\09-simple-patterns\\9_2_multi_agent.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model

model = get_model()

messy_notes = """
ok so api latency spiked tuesday, sam thinks it's the redis pool, will check by thursday.
also marketing wants launch moved to nov 25, priya to confirm with legal.
oh and we approved the $400/mo staging db upgrade.
"""

extractor = Agent(
    model=model,
    system_prompt="Extract only Decisions and Action Items (with owner and due date if mentioned) as bullets.",
    callback_handler=None,
)

email_writer = Agent(
    model=model,
    system_prompt="Turn the structured bullets into a crisp, friendly team update email with a Subject line.",
    callback_handler=None,
)

extracted = str(extractor(messy_notes))
email = email_writer(extracted)
print(email)

