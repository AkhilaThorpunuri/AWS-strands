"""
1.3 System Prompts & Personas
Module 1 · Agent Fundamentals | Read first: md/01-agent-fundamentals/1_3_system_prompts.md

What you'll learn:
  - How system_prompt changes tone, focus, and output structure for the same prompt.

Run (from the repo root):
  .venv\\Scripts\\python code\\01-agent-fundamentals\\1_3_system_prompts.py
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
question = "Explain AWS Lambda."

teacher = Agent(
    model=model,
    system_prompt="You are a friendly teacher for beginners. Use one everyday analogy and 3 short bullets.",
    callback_handler=None,
)

auditor = Agent(
    model=model,
    system_prompt="You are a strict cloud security auditor. List only the top 3 security risks and mitigations.",
    callback_handler=None,
)

print("--- Teacher Persona ---")
print(teacher(question))

print("\n--- Security Auditor Persona ---")
print(auditor(question))

# ---------------------------------------------------------------
# Takeaways
#   - system_prompt is the agent's standing job description and output contract.
# ---------------------------------------------------------------

