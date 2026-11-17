"""
4.2 Streaming & Async Execution
Module 4 · Structured Outputs & Streaming | Read first: md/04-structured-outputs-and-streaming/4_2_streaming_and_async.md

What you'll learn:
  - How to stream tokens and lifecycle events asynchronously with agent.stream_async().

Run (from the repo root):
  .venv\\Scripts\\python code\\04-structured-outputs-and-streaming\\4_2_streaming_and_async.py
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
    # Disable default stdout callback so we control printing from the stream
    agent = Agent(model=get_model(), callback_handler=None)

    print("Streaming response:\n")
    chunks = 0
    async for event in agent.stream_async("Write a 2-sentence haiku-inspired intro to cloud agents."):
        if "data" in event:
            print(event["data"], end="", flush=True)
            chunks += 1
        elif "current_tool_use" in event and event["current_tool_use"].get("name"):
            print(f"\n[Tool] {event['current_tool_use']['name']}", flush=True)

    print(f"\n\n[Done] Received {chunks} text chunks.")


asyncio.run(main())

# ---------------------------------------------------------------
# Takeaways
#   - stream_async() yields live token chunks ('data') and tool events.
#   - Pair with callback_handler=None when rendering the stream yourself.
# ---------------------------------------------------------------

