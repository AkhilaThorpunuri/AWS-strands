"""
3.1 Built-in (Vended) Tools
Module 3 · Tools & MCP | Read first: md/03-tools-and-mcp/3_1_builtin_tools.md

What you'll learn:
  - How to equip an agent with ready-made vended tools from strands.vended_tools.

Run (from the repo root):
  .venv\\Scripts\\python code\\03-tools-and-mcp\\3_1_builtin_tools.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.vended_tools import http_request, python_repl, read
from common.config import get_model

agent = Agent(
    model=get_model(),
    tools=[read, python_repl, http_request],
    system_prompt="Use the read tool to inspect files and python_repl for exact math. Keep replies brief.",
)

response = agent("Read requirements.txt, count how many packages are listed, and compute 84.60 * 1.15 using python_repl.")
print(f"\nResponse:\n{response}")

# ---------------------------------------------------------------
# Takeaways
#   - strands.vended_tools provides battle-tested utilities out of the box.
# ---------------------------------------------------------------

