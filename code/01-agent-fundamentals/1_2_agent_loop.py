"""
1.2 The Model-Driven Agent Loop
Module 1 · Agent Fundamentals | Read first: md/01-agent-fundamentals/1_2_agent_loop.md

What you'll learn:
  - How Strands executes multiple tool calls automatically in a think -> act -> observe loop.

Run (from the repo root):
  .venv\\Scripts\\python code\\01-agent-fundamentals\\1_2_agent_loop.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent, tool
from common.config import get_model


@tool
def get_order_status(order_id: str) -> dict:
    """Look up the delivery status and age in days of an order.

    Args:
        order_id: The order identifier, e.g. A102.
    """
    orders = {
        "A102": {"status": "delivered", "days_since_delivery": 5},
        "B205": {"status": "delivered", "days_since_delivery": 45},
    }
    return orders.get(order_id, {"status": "not_found"})


@tool
def get_refund_policy() -> str:
    """Return the store's current refund eligibility rule."""
    return "Orders delivered within 30 days are eligible for a full refund."


agent = Agent(
    model=get_model(),
    tools=[get_order_status, get_refund_policy],
    system_prompt="Check both the order status and refund policy before answering.",
)

result = agent("Can I get a refund for order A102?")
print(f"\nFinal Answer:\n{result}")
print(f"\n--- Loop Trace ---\nTotal messages in conversation: {len(agent.messages)}")

# ---------------------------------------------------------------
# Takeaways
#   - The model decides which tools to call and when to stop looping.
#   - Each tool call + result is appended to agent.messages automatically.
# ---------------------------------------------------------------

