"""
7.2 Swarm (Autonomous Handoffs)
Module 7 · Multi-Agent Patterns | Read first: md/07-multi-agent-patterns/7_2_swarm.md

What you'll learn:
  - How to build a peer-to-peer Swarm where agents hand off work dynamically.

Run (from the repo root):
  .venv\\Scripts\\python code\\07-multi-agent-patterns\\7_2_swarm.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.multiagent import Swarm
from common.config import get_model

model = get_model()

triage = Agent(
    name="triage",
    model=model,
    system_prompt=(
        "You are the front-desk triage agent. Never solve the issue yourself; "
        "always hand off to `billing_specialist` for invoices/refunds or `tech_support` for errors/bugs."
    ),
)

billing_specialist = Agent(
    name="billing_specialist",
    model=model,
    system_prompt="You handle invoices, refunds, and subscription charges concisely.",
)

tech_support = Agent(
    name="tech_support",
    model=model,
    system_prompt="You diagnose application errors and give concise troubleshooting steps.",
)

swarm = Swarm(
    [triage, billing_specialist, tech_support],
    entry_point=triage,
    max_handoffs=5,
    max_iterations=10,
)

result = swarm("Our checkout API is returning 502 Bad Gateway errors after deployment.")
print(f"\nSwarm status: {result.status}")
print(f"Final result:\n{result.results[result.node_history[-1].node_id].result}")

# ---------------------------------------------------------------
# Takeaways
#   - Swarm enables emergent, peer-to-peer handoffs between named agents.
#   - Always set max_handoffs / max_iterations as safety bounds.
# ---------------------------------------------------------------

