"""
4.1 Structured Output with Pydantic
Module 4 · Structured Outputs & Streaming | Read first: md/04-structured-outputs-and-streaming/4_1_structured_output.md

What you'll learn:
  - How to enforce a typed Pydantic schema using structured_output_model.

Run (from the repo root):
  .venv\\Scripts\\python code\\04-structured-outputs-and-streaming\\4_1_structured_output.py
"""

import io
import sys
from pathlib import Path
from typing import Literal

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pydantic import BaseModel, Field
from strands import Agent
from common.config import get_model


class TicketTriage(BaseModel):
    """Structured triage decision for a customer support message."""

    category: Literal["billing", "bug", "account", "other"] = Field(
        description="Support queue that should handle this ticket."
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="High if the customer is blocked or experiencing billing errors."
    )
    summary: str = Field(description="One-sentence summary of the issue.")


agent = Agent(model=get_model(), callback_handler=None)

ticket = "I was charged twice on my invoice #9921 today and need a refund!"
result = agent(ticket, structured_output_model=TicketTriage)

assert isinstance(result.structured_output, TicketTriage)
triage: TicketTriage = result.structured_output
print(f"Category : {triage.category}")
print(f"Priority : {triage.priority}")
print(f"Summary  : {triage.summary}")

# ---------------------------------------------------------------
# Takeaways
#   - structured_output_model guarantees a validated Pydantic instance.
#   - No brittle json.loads() or regex parsing needed.
# ---------------------------------------------------------------

