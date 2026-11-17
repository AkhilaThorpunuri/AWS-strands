"""
0.2 Words You Need to Know
Module 0 · Getting Started | Read first: md/00-getting-started/0_2_words_you_need_to_know.md

What you'll learn:
  - How Agent, Model, System Prompt, @tool, and agent.messages fit together in 20 lines.

Run (from the repo root):
  .venv\\Scripts\\python code\\00-getting-started\\0_2_glossary_in_code.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent, tool
from common.config import get_model


# 1. TOOL: any Python function decorated with @tool
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First number.
        b: Second number.
    """
    return a * b


# 2. MODEL: the LLM brain
model = get_model()

# 3. AGENT + SYSTEM PROMPT + TOOLS
agent = Agent(
    model=model,
    system_prompt="You are a concise math helper. Always use tools for arithmetic.",
    tools=[multiply],
)

print("===== 10 STRANDS TERMS IN ACTION =====\n")

# 4. AGENT LOOP: agent() runs think -> tool -> observe -> answer automatically
result = agent("What is the total for 3 items at $14.50 each?")

print("\nAgent response:")
print(result)

# 5. MESSAGES: inspect the conversation history recorded during the loop
print(f"\nMessages recorded in agent.messages: {len(agent.messages)}")
print(f"Tools available to agent: {agent.tool_names}")

# ---------------------------------------------------------------
# Takeaways
#   - Agent = Model + System Prompt + Tools.
#   - Calling agent("...") runs the full tool-calling loop and updates agent.messages.
# ---------------------------------------------------------------

