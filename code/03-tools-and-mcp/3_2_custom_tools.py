"""
3.2 Custom @tool Functions
Module 3 · Tools & MCP | Read first: md/03-tools-and-mcp/3_2_custom_tools.md

What you'll learn:
  - How to build custom @tool functions with type hints, docstrings, and validation.

Run (from the repo root):
  .venv\\Scripts\\python code\\03-tools-and-mcp\\3_2_custom_tools.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent, tool
from common.config import get_model

INVENTORY = {
    "WIDGET-01": {"stock": 15, "warehouse": "us-east"},
    "GADGET-99": {"stock": 0, "warehouse": "eu-west"},
}


@tool
def lookup_inventory(sku: str) -> dict:
    """Check stock count and warehouse location for a product SKU.

    Args:
        sku: Product SKU code, e.g. 'WIDGET-01'.
    """
    item = INVENTORY.get(sku.upper())
    if not item:
        return {"error": f"Unknown SKU: {sku}"}
    return {"sku": sku.upper(), **item}


@tool
def reserve_stock(sku: str, quantity: int) -> dict:
    """Reserve units of a SKU if enough stock is available.

    Args:
        sku: Product SKU code.
        quantity: Positive integer number of units to reserve.
    """
    key = sku.upper()
    if key not in INVENTORY:
        return {"status": "failed", "reason": f"Unknown SKU: {sku}"}
    if quantity <= 0:
        return {"status": "failed", "reason": "Quantity must be positive."}
    if INVENTORY[key]["stock"] < quantity:
        return {"status": "failed", "reason": f"Only {INVENTORY[key]['stock']} units available."}
    INVENTORY[key]["stock"] -= quantity
    return {"status": "reserved", "sku": key, "remaining_stock": INVENTORY[key]["stock"]}


agent = Agent(
    model=get_model(),
    tools=[lookup_inventory, reserve_stock],
    system_prompt="Always check inventory before reserving stock.",
)

print(agent("Check WIDGET-01 and reserve 3 units if available."))

# ---------------------------------------------------------------
# Takeaways
#   - @tool turns Python functions into LLM-callable tools using type hints + docstrings.
#   - Returning clear error dicts lets the agent explain failures instead of crashing.
# ---------------------------------------------------------------

