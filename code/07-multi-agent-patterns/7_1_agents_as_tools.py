"""
7.1 Agents as Tools
Module 7 · Multi-Agent Patterns | Read first: md/07-multi-agent-patterns/7_1_agents_as_tools.md

What you'll learn:
  - How to wrap specialist Agents as tools for an orchestrator Agent.

Run (from the repo root):
  .venv\\Scripts\\python code\\07-multi-agent-patterns\\7_1_agents_as_tools.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent, tool
from common.config import get_model

model = get_model()

research_agent = Agent(
    model=model,
    system_prompt="You are a concise technical researcher. Return 3 key facts as bullet points.",
    callback_handler=None,
)

writer_agent = Agent(
    model=model,
    system_prompt="You are a crisp product copywriter. Turn facts into a 2-sentence announcement.",
    callback_handler=None,
)


@tool
def researcher(topic: str) -> str:
    """Gather 3 concise technical facts about a topic."""
    return str(research_agent(f"Summarize 3 key facts about: {topic}"))


@tool
def copywriter(facts: str) -> str:
    """Write a short, engaging 2-sentence announcement from research facts."""
    return str(writer_agent(f"Write a 2-sentence announcement using these facts:\n{facts}"))


orchestrator = Agent(
    model=model,
    tools=[researcher, copywriter],
    system_prompt=(
        "You coordinate content creation. First call `researcher` to gather facts, "
        "then pass those facts to `copywriter`, and return the final announcement."
    ),
)

result = orchestrator("Create a launch announcement for AWS Strands Agents SDK.")
print(f"\nFinal Output:\n{result}")

# ---------------------------------------------------------------
# Takeaways
#   - Wrapping specialist agents in @tool functions gives you clean hierarchical delegation.
# ---------------------------------------------------------------

