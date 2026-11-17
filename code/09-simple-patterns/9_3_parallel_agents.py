"""
9.3 Parallel Agents
Module 9 · Simple Patterns | Read first: md/09-simple-patterns/9_3_parallel_agents.md

Problem: Get 3 independent expert opinions in parallel, then synthesize a Go/No-Go verdict.

Run (from the repo root):
  .venv\\Scripts\\python code\\09-simple-patterns\\9_3_parallel_agents.py
"""

import asyncio
import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model


async def main() -> None:
    model = get_model()
    proposal = "Let customers upload CSVs up to 50MB and query them with natural language."

    security = Agent(model=model, system_prompt="Give 2 concise security risks/mitigations.", callback_handler=None)
    finops = Agent(model=model, system_prompt="Give 2 concise cost considerations.", callback_handler=None)
    ux = Agent(model=model, system_prompt="Give 2 concise UX benefits or friction points.", callback_handler=None)
    decider = Agent(model=model, system_prompt="Synthesize into a 3-sentence Go / No-Go verdict.", callback_handler=None)

    print("Running 3 reviewers in parallel...\n")
    sec_out, fin_out, ux_out = await asyncio.gather(
        security.invoke_async(proposal),
        finops.invoke_async(proposal),
        ux.invoke_async(proposal),
    )

    combined = f"Security:\n{sec_out}\n\nFinOps:\n{fin_out}\n\nUX:\n{ux_out}"
    print(decider(combined))


asyncio.run(main())

