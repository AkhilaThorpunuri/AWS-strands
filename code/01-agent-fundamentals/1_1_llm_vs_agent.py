"""
1.1 LLM vs Agent
Module 1 · Agent Fundamentals | Read first: md/01-agent-fundamentals/1_1_llm_vs_agent.md

What you'll learn:
  - The difference between an LLM with no tools and a Strands Agent with tools.

Run (from the repo root):
  .venv\\Scripts\\python code\\01-agent-fundamentals\\1_1_llm_vs_agent.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from datetime import datetime, timezone
from strands import Agent, tool
from strands.vended_tools import python_repl
from common.config import get_model


@tool
def get_utc_time() -> str:
    """Return the current UTC date and time."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


model = get_model()
question = "What is the current UTC time, and what is 1847 * 29?"

# 1. Plain LLM behavior: an Agent with NO tools can only rely on static weights
plain_llm = Agent(model=model, callback_handler=None)
print("--- 1. Plain LLM (no tools) ---")
print(plain_llm(question))

# 2. Tool-equipped Agent: can check the clock and run exact math in Python
agent = Agent(
    model=model,
    tools=[get_utc_time, python_repl],
    system_prompt="Use tools whenever a question asks for live time or math.",
)
print("\n--- 2. Strands Agent (with get_utc_time + python_repl) ---")
print(agent(question))

# ---------------------------------------------------------------
# Takeaways
#   - Without tools, an LLM cannot know live state (time, DBs, APIs).
#   - Giving an Agent tools turns it from a text predictor into a problem solver.
# ---------------------------------------------------------------

