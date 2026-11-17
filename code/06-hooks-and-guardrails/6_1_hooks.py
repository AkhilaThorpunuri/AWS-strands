"""
6.1 Lifecycle Hooks
Module 6 · Hooks, Guardrails & Observability | Read first: md/06-hooks-and-guardrails/6_1_hooks.md

What you'll learn:
  - How to implement HookProvider to audit tool calls before and after execution.

Run (from the repo root):
  .venv\\Scripts\\python code\\06-hooks-and-guardrails\\6_1_hooks.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent, tool
from strands.hooks import HookProvider, HookRegistry
from strands.hooks.events import AfterToolCallEvent, BeforeToolCallEvent
from common.config import get_model


class ToolAuditHook(HookProvider):
    """Logs every tool invocation before and after it executes."""

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeToolCallEvent, self.on_before_tool)
        registry.add_callback(AfterToolCallEvent, self.on_after_tool)

    def on_before_tool(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use.get("name")
        args = event.tool_use.get("input")
        print(f"[HOOK before] tool={name} input={args}")

    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        name = event.tool_use.get("name")
        print(f"[HOOK after]  tool={name} completed")


@tool
def get_account_balance(account_id: str) -> str:
    """Return the current balance for a bank account ID."""
    balances = {"ACC-100": "$1,250.00", "ACC-200": "$430.50"}
    return balances.get(account_id, "Account not found")


agent = Agent(
    model=get_model(),
    tools=[get_account_balance],
    hooks=[ToolAuditHook()],
    callback_handler=None,
)

print(agent("What is the balance for account ACC-100?"))

# ---------------------------------------------------------------
# Takeaways
#   - HookProvider lets you observe or intercept agent execution cleanly.
# ---------------------------------------------------------------

